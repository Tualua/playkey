#!/usr/bin/python

import json, time, sys, subprocess, numpy as np, operator
import geoip2.database
import xml.etree.ElementTree as ET

def exec_shell_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = proc.communicate()
    return stdout.split('\n')


def get_session_ipaddress(start, end, domainName):
    data = exec_shell_command("journalctl --since=\"{}\" --until=\"{}\" --no-pager -tgameserver/{} -r "\
                                "|grep -E \"r: New client address\"".format(start, end, domainName))
    return data[0].split(' ')[-1].split(':')[0]


def get_fps_stats(start, end, domainName):
    data = exec_shell_command("journalctl --since=\"{}\" --until=\"{}\" --no-pager -tgameserver/{} -r "\
                                "|grep -e \"FPS (for last 5 sec)\"| awk '{{print $12}}'".format(start, end, domainName))[:-1]
    if len(data)>0:
        fps = np.array([int(val) for val in data])
        p99 = np.percentile(fps, 99)
        return int(p99)
    else:
        return 0


def get_latency_stats(start, end, domainName):
    data = exec_shell_command("journalctl --since=\"{}\" --until=\"{}\" --no-pager -tgameserver/{} -r "\
                                "|grep -e \"Ping (for last 5 sec)\"| awk '{{print $11}}'".format(start, end, domainName))[:-1]
    if len(data)>0:
        ping = np.array([int(val) for val in data])
        p99 = np.percentile(ping, 99)
        return int(p99)
    else:
        return 9999


def time_difference(time0, time1):
    seconds = (time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(time0, "%Y-%m-%d %H:%M:%S")))
    return int(seconds/60)

def get_location(ipaddress):
    reader = geoip2.database.Reader('/usr/share/GeoIP/GeoLite2-City.mmdb')
    country, city = '', ''
    try:
        location = reader.city(ipaddress)
        country_u = location.country.name
        country = country_u.encode('ascii', 'replace')
        city_u = location.city.name
        if city_u:
            city = city_u.encode('ascii', 'replace').replace('?','')
    except geoip2.errors.AddressNotFoundError:
        pass
    reader.close()
    return country, city

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
        sessions[session_id] = [session_start,'',session_game]

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
            ipaddress = get_session_ipaddress(session_start, session_end, domainName)
            country,city = '',''
            if ipaddress:
                country, city = get_location(ipaddress)
            minutes = time_difference(session_start,session_end)
            fps_stats = get_fps_stats(session_start, session_end, domainName)
            latency_stats = get_latency_stats(session_start, session_end, domainName)
            sessions[session_id].extend([ipaddress, country, city, minutes, fps_stats, latency_stats])
        else:
            sessions[session_id].extend(['', '', '', 0, 0, 0])
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
