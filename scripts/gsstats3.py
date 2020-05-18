#!/usr/bin/python

import json, time, sys, subprocess, numpy as np, operator
import hashlib, platform, geoip2.database, pygsheets, pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime as dt 
from datetime import timedelta

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
def get_log(domainName, start, end, reverse=False):
    if not reverse:
        data = exec_shell_command('journalctl -o short-iso -b --since=\"{}\" --until=\"{}\" --no-pager -tgameserver/{} '.format(start, end, domainName))
    else:
        data = exec_shell_command('journalctl -o short-iso -b --since=\"{}\" --until=\"{}\" --no-pager -tgameserver/{} -r '.format(start, end, domainName))
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
        p99 = np.percentile(fps, 99)
        return int(p99)
    else:
        return 0

#Calculate latency statistics
def get_latency_stats(data):
    if len(data)>0:
        ping = np.array(data)
        p99 = np.percentile(ping, 99)
        return int(p99)
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
                result[session_id]["FPS"] = []
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
            #FPS
            elif 'FPS (for last 5 sec)' in value:
                result[session_id]["FPS"].extend([int(value.split(' U: ')[1].split(' ')[0])])
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

sessions={}

vms = get_servers()

now_time = dt.now()

now_time = dt.now()-timedelta(days=2)

start_time = (now_time-timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
end_time = (now_time-timedelta(days=1)).strftime('%Y-%m-%d 23:59:59')

print("Exporting data from {} to {}".format(start_time, end_time))

for vm in vms:
    log = get_log(vm, start_time, end_time)
    s = get_sessions(log)
    #Check for yesterday session
    if "yesterday" in s.keys():
        #Find that session start time
        y_log = get_log(vm, (dt.now()-timedelta(days=2)).strftime('%Y-%m-%d 00:00:00'), (dt.now()-timedelta(days=2)).strftime('%Y-%m-%d 23:59:59'), reverse=True)
        for value in y_log:
            if ' CreateSession: session_id' in value:
                y_session_start_time = value.split(' ')[0][:-5].replace('T',' ')
                break
        y_log = get_log(vm, y_session_start_time, (dt.now()-timedelta(days=2)).strftime('%Y-%m-%d 23:59:59'))
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
            FPS = get_fps_stats(v["FPS"])
            s[k]["FPS"] = FPS
            #Check if there will be unfinished session today and drop it from sessions dict
            if not "End Time" in v.keys():
                s.pop(k)
            else:
                s[k]["Duration"] = time_difference(v["Start Time"], v["End Time"])
    sessions.update(s)

df_cols = ['Start Time', 'End Time', 'Host', 'VM', 'Game', 'ID', 'Continent', 'Country', 'Region', 'City', 'Latitude', 
            'Longitude', 'ASN', 'ASN Provider', 'Duration', 'FPS', 'Latency', 'Resolution']
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
for v in sorted(sessions_export.items(), key=operator.itemgetter(0)):
    print(v)

df = pd.DataFrame.from_dict(data=sessions_export, orient='index', columns=df_cols)
df.sort_index(inplace=True)
df_row_count = len(df.index)

#Connect to Google Sheets
client = pygsheets.authorize(service_file='/root/api/playkey.json')
sheet = client.open('PlayKey-Data')
try:
    wks = sheet.worksheet_by_title('Test')
except pygsheets.exceptions.WorksheetNotFound:
    wks = sheet.add_worksheet('Test')
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
