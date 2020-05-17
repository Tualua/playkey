#!/usr/bin/python

import json, time, sys, subprocess, numpy as np, operator
import geoip2.database
import xml.etree.ElementTree as ET

def exec_shell_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = proc.communicate()
    return stdout.split('\n')


def get_session_ipaddress(data_raw):
    for line in data_raw:
        if 'r: New client address' in line:
            return line.split(' ')[-1].split(':')[0]
    return ''

def get_session_log(start, end, domainName):
    return exec_shell_command("journalctl --since=\"{}\" --until=\"{}\" --no-pager -tgameserver/{} -r ".format(start, end, domainName))

def get_fps_stats(data_raw):
    data = []
    for line in data_raw:
        if 'FPS (for last 5 sec)' in line:
            data.append(int(line.split(' | ')[-1].split(' ')[0]))
    if len(data)>0:
        fps = np.array([int(val) for val in data])
        p99 = np.percentile(fps, 99)
        return int(p99)
    else:
        return 0


def get_latency_stats(data_raw):
    data = []
    for line in data_raw:
        if 'Ping (for last 5 sec)' in line:
            data.append(int(line.split(': ')[-1].split(' ')[0]))
    if len(data)>0:
        ping = np.array([int(val) for val in data])
        p99 = np.percentile(ping, 99)
        return int(p99)
    else:
        return 9999


def get_resolution(data_raw):
    for line in data_raw:
        if 'CreateProcessSync: "python.exe" c:/temp/sc.py' in line:
            return line.split(' ')[-3:]

def time_difference(time0, time1):
    seconds = (time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(time0, "%Y-%m-%d %H:%M:%S")))
    return int(seconds/60)

def get_location(ipaddress):
    reader = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-City.mmdb')
    readerasn = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-ASN.mmdb')
    result = [''] * 8
    try:
        location = reader.city(ipaddress)
        result[0] = location.continent.name.encode('ascii', 'replace')
        result[1] = location.country.name.encode('ascii', 'replace')
        result[2] = location.subdivisions.most_specific.name.encode('ascii', 'replace')
        result[3] = location.city.name.encode('ascii', 'replace')
        result[4] = location.location.latitude
        result[5] = location.location.longitude
        asn = readerasn.asn(ipaddress)
        result[6] = asn.autonomous_system_number
        result[7] = asn.autonomous_system_organization.encode('ascii', 'replace')
    except geoip2.errors.AddressNotFoundError:
        pass
    except AttributeError:
        pass
    reader.close()
    readerasn.close()
    return result

def get_servers(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = []
    for server in root.iter('Server'):
        vms.append(server.get('name'))
    return vms

def get_sessions(domainName):
    sessions = {}

    data = exec_shell_command('journalctl -o short-iso --since=yesterday --no-pager -tgameserver/{} -r ' \
                                '|grep -B1 -E \"driveName\"|grep -v -e \"windows\" -e \"launchers\"'.format(domainName))[:-1]
    started_sessions = len(data)

    for i in xrange(0, started_sessions, 3):
        session_id = data[i].rsplit(' ')[-4][:-1].strip()
        session_start = data[i].split(' ')[0][:-5].replace('T',' ')
        session_game = data[i+1].split("/")[-1]
        sessions[session_id] = [session_start, '', domainName, session_game]

    data = exec_shell_command('journalctl -o short-iso --since=yesterday --no-pager -tgameserver/{} -r ' \
                                '|grep -E \"StopGameSession\"'.format(domainName))[:-1]

    for session in data:
        session_id = session.rsplit(' ')[-1].strip()
        session_end_time = session.split(' ')[0][:-5].replace('T',' ')
        sessions[session_id][1] = session_end_time

    for session_id,session_data in sessions.items():
        session_start = session_data[0]
        session_end = session_data[1]
        if session_end:
            session_log = get_session_log(session_start, session_end, domainName)
            ipaddress = get_session_ipaddress(session_log)
            if ipaddress:
                location = get_location(ipaddress)
            minutes = time_difference(session_start,session_end)
            fps_stats = get_fps_stats(session_log)
            latency_stats = get_latency_stats(session_log)
            resolution = get_resolution(session_log)
            sessions[session_id].extend([ipaddress])
            sessions[session_id].extend(location)
            sessions[session_id].extend([minutes, fps_stats, latency_stats])
            sessions[session_id].extend(resolution)
        else:
            sessions[session_id].extend(['', '', '', '', '', 0, 0, 0,'','',''])
    return sessions

def get_session_data():
    return None

sessions={}
vms = get_servers()
for vm in vms:
    sessions[vm] = get_sessions(vm)

for vm in sessions:
    print("---------------------{}---------------------".format(vm))
    for k,v in sorted(sessions[vm].items(), key=operator.itemgetter(0)):
        print(k, v)
