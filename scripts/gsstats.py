#!/usr/bin/python
# Script to analyze FPS data from PlayKey GameServer
# Requires pygsheets, numpy and pandas installed
# Default Google API key location is /home/games/api/playkey.json
# Default log folder is /var/log/gsstats
# Copyright by Dmitry Popovich

import json, time, sys, argparse, subprocess, pygsheets, numpy as np, operator
import hashlib, platform, geoip2.database, pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime as dt 
from datetime import timedelta
from csv import QUOTE_NONNUMERIC

#Read VM names from GameServer config
def get_servers(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = []
    for server in root.iter('Server'):
        vms.append(server.get('name'))
    return vms

#Wrapper for shell command excecution
def exec_shell_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = proc.communicate()
    return stdout.split('\n')

#Read GameServer log for <vm> for <start>-<end> timeframe. 
def get_log(domainName, start, end, reverse=False, debug=False, logdir=''):
    jctl_options = ["-o short-iso"]
    jctl_options.append("--no-pager -tgameserver/{}".format(domainName))
    
    if start:
        jctl_options.append("--since=\"{}\"".format(start))
    if end:
        jctl_options.append("--until=\"{}\"".format(end))
    if reverse:
        jctl_options.append("-r")
    if logdir:
        jctl_options.append("--directory {}".format(logdir))
    
    jctl = "journalctl {}".format(" ".join(jctl_options))
    if debug:
        print('Get journal: {}'.format(jctl))
    data = exec_shell_command(jctl)

    return data


#Calculate difference in minutes between two dates
def time_difference(time0, time1):
    seconds = (time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(time0, "%Y-%m-%d %H:%M:%S")))
    return int(seconds/60)


#Get IP address location info using MaxMind databases
def get_location(ipaddress):
    reader = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-City.mmdb')
    readerasn = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-ASN.mmdb')
    result = {}
    try:
        location = reader.city(ipaddress)
        result["Continent"] = location.continent.name.encode('ascii', 'replace')
        result["Country"] = location.country.name.encode('ascii', 'replace')
        result["Region"] = location.subdivisions.most_specific.name.encode('ascii', 'replace')
        result["City"] = location.city.name.encode('ascii', 'replace')
        result["Latitude"] = float(location.location.latitude)
        result["Longitude"] = float(location.location.longitude)
        asn = readerasn.asn(ipaddress)
        result["ASN"] = "AS{}".format(asn.autonomous_system_number)
        result["ASN Provider"] = asn.autonomous_system_organization.encode('ascii', 'replace')
    except geoip2.errors.AddressNotFoundError:
        pass
    except AttributeError:
        pass
    reader.close()
    readerasn.close()
    return result

#Calculate FPS statistics
def get_fps_stats(data):
    if len(data)>0:
        fps = np.array(data)
        p = np.percentile(fps, 25)
        return int(p)
    else:
        return 0

#Calculate latency statistics
def get_latency_stats(data):
    if len(data)>0:
        ping = np.array(data)
        p = np.percentile(ping, 25)
        return int(p)
    else:
        return 9999


#Get sessions information from day log
def get_sessions(data):
    result={}
    for i, value in enumerate(data):
        try:
            #Session creation time
            if ' CreateSession: session_id' in value:
                session_id = value.split(' = ')[-1].split(' ')[-1]
                session_start_time = value.split(' ')[0][:-5].replace('T',' ')
                result[session_id] = {"Start Time":session_start_time}
                result[session_id]["FPS Game"] = []
                result[session_id]["FPS Customer"] = []
                result[session_id]["Latency"] = []
            #Game name
            elif ' CreateSession: driveName ' in value:
                result[session_id]["Game"] = value.split('/')[-1]
            #Client display resolution
            elif 'CreateProcessSync: "python.exe" c:/temp/sc.py' in value:
                result[session_id]["Resolution"] = "x".join([x for x in value.split(' ')[-3:]])
            #Client IP address
            elif 'r: New client address' in value:
                ipaddress = value.split(' ')[-1].split(':')[0]
                result[session_id]["ID"] = hashlib.md5(ipaddress.encode()).hexdigest()[:16]
                result[session_id].update(get_location(ipaddress))
            #FPS sent to customer
            elif 'FPS (for last 5 sec)' in value:
                result[session_id]["FPS Customer"].extend([int(value.split(' U: ')[1].split(' ')[0])])
            #Game FPS
            elif 'Present (FPS' in value:
                result[session_id]["FPS Game"].extend([int(value.split('FPS = ')[1].split(')')[0])])
            #Latency
            elif 'Ping (for last 5 sec)' in value:
                result[session_id]["Latency"].extend([int(value.split(': ')[-1].split(' ')[0])])
            #Session end time
            elif 'StopGameSession' in value:
                session_end_time = value.split(' ')[0][:-5].replace('T',' ')
                result[session_id]["End Time"] = session_end_time
        #Catch exception in case there is a session began yesterday
        except UnboundLocalError as e:
            session_id = "yesterday"
            result["yesterday"] = {}
            pass
        #Create keys for yesterday session
        except KeyError as e:
            result["yesterday"][e.args[0]] = []
    return result

def main(args):
    now_time = dt.now()
    #Parse arguments
    if args.all:
        start_time = 0
        end_time = 0
        td = 0
        csv_export = "/var/log/gsstats/pk_sessions-all-{}.csv".format(now_time.strftime('%Y-%m-%d-%H-%M-%S'))
        print("Analyze all sessions")
    else:
        td = args.day
        start_time = (now_time-timedelta(days=td)).strftime('%Y-%m-%d 00:00:00')
        end_time = (now_time-timedelta(days=td)).strftime('%Y-%m-%d 23:59:59')
        csv_export = "/var/log/gsstats/pk_sessions-{}.csv".format(now_time.strftime('%Y-%m-%d-%H-%M-%S'))
        print("Analyze session data from {} to {}".format(start_time, end_time))

    logdir=''
    if args.logdir:
        logdir = args.logdir

    sessions={}
    vms = get_servers()

    for vm in vms:
        log = get_log(vm, start_time, end_time, debug=args.debug, logdir=logdir)
        s = get_sessions(log)
        #Check for yesterday session
        if "yesterday" in s.keys():
            #Find that session start time
            y_log = get_log(vm, (now_time-timedelta(days=td+1)).strftime('%Y-%m-%d 00:00:00'), (now_time-timedelta(days=td+1)).strftime('%Y-%m-%d 23:59:59'), reverse=True, debug=args.debug, logdir=logdir)
            for value in y_log:
                if ' CreateSession: session_id' in value:
                    y_session_start_time = value.split(' ')[0][:-5].replace('T',' ')
                    break
            y_log = get_log(vm, y_session_start_time, (now_time-timedelta(days=td+1)).strftime('%Y-%m-%d 23:59:59'), logdir=logdir)
            #Get yesterday session data
            y_s = get_sessions(y_log)
            #Add that session to session dict
            s.update(y_s)
            #Save that session ID
            y_s_id = y_s.items()[0][0]
            #Save incomplete session data and remove it from sessions dict
            y_s = s.pop("yesterday")
            #Add missing data for yesterday session to sessions dict
            for k in y_s.keys():
                if k in s[y_s_id].keys() and isinstance(y_s[k], list):
                    s[y_s_id][k].extend(y_s[k])
                else:
                    s[y_s_id][k] = y_s[k]

        #Calculate FPS and latency stats and add info about VM and host
        for k,v in s.items():
                s[k]["Host"] = platform.node().split('.', 1)[0]
                s[k]["VM"] = vm
                ping = get_latency_stats(v["Latency"])
                s[k]["Latency"] = ping
                FPS_Customer = get_fps_stats(v["FPS Customer"])
                s[k]["FPS Customer"] = FPS_Customer
                #print(v["FPS Game"])
                FPS_Game = get_fps_stats(v["FPS Game"])
                s[k]["FPS Game"] = FPS_Game
                #Check if there will be unfinished session today and drop it from sessions dict
                if not "End Time" in v.keys():
                    s.pop(k)
                else:
                    s[k]["Duration"] = time_difference(v["Start Time"], v["End Time"])
        sessions.update(s)

    df_cols = ['Start Time', 'End Time', 'Host', 'VM', 'Game', 'ID', 'Continent', 'Country', 'Region', 'City', 'Latitude', 
                'Longitude', 'ASN', 'ASN Provider', 'Duration', 'FPS Customer', 'FPS Game', 'Latency', 'Resolution']
    
    #Dict for exporting data to pandas DataFrame
    sessions_export = {}
    for k,v in sessions.items():
        session = []
        for col in df_cols:
            try:
                session.append(v[col])
            except KeyError:
                session.append('')
        sessions_export[k] = session

    #Debug info
    if args.debug:
        for v in sorted(sessions_export.items(), key=operator.itemgetter(0)):
            print(v)

    df = pd.DataFrame.from_dict(data=sessions_export, orient='index', columns=df_cols)
    df.sort_index(inplace=True)
    try:
        df.to_csv(csv_export, index_label="Session", quoting=QUOTE_NONNUMERIC)
    except Exception as e:
        print('Unable to save exported data!')
    else:
        print('Session data is saved to: {}'.format(csv_export))
    
    df_row_count = len(df.index)

    if not args.offline:
        #Connect to Google Sheets
        print('Exporting data to Google Sheets')
        wks_name = 'PlayKey Session Data'
        client = pygsheets.authorize(service_file=args.key_path)
        sheet = client.open('PlayKey-Data')
        try:
            wks = sheet.worksheet_by_title(wks_name)
        except pygsheets.exceptions.WorksheetNotFound:
            wks = sheet.add_worksheet(wks_name)
            header = df_cols
            header.insert(0, 'Session')
            wks.update_row(1,values=header)

        wks.insert_rows(1,df_row_count)

        #Format columns
        cell_date = pygsheets.Cell('A1')
        cell_date.set_number_format(pygsheets.FormatType.DATE_TIME)
        pygsheets.datarange.DataRange(start='B', end=None, worksheet=wks).apply_format(cell_date)
        pygsheets.datarange.DataRange(start='C', end=None, worksheet=wks).apply_format(cell_date)

        cell_number = pygsheets.Cell('K1')
        cell_number.set_number_format(pygsheets.FormatType.NUMBER)
        pygsheets.datarange.DataRange(start='K', end=None, worksheet=wks).apply_format(cell_number)
        pygsheets.datarange.DataRange(start='L', end=None, worksheet=wks).apply_format(cell_number)

        #Export data
        wks.set_dataframe(df, (2,1),copy_index=True, copy_head=False, extend=False)
    else:
        print('Offline mode: no data will be exported to Google Sheets')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PlayKey GameServer session data anayzer')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--day', type=int, action='store', dest='day', help='Day to analyze for sessions. 0 - today, 1 - yesterday etc.')
    group.add_argument('--all', action='store_true', help='Analyze all sessions')
    parser.add_argument('--offline', help='Do not publish data to Google Sheets', action='store_true', default=False)
    parser.add_argument('--debug', help='Print additional info during run', action='store_true', default=False)
    parser.add_argument('--key', type=str, action='store', dest="key_path", help='Path to Google API key', default="/home/gamer/api/playkey.json")
    parser.add_argument('--logdir', type=str, action='store', dest="logdir", help='Path to journal log dir')
    args = parser.parse_args()
    main(args)
