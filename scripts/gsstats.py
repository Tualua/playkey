#!/usr/bin/python

import json, time, sys, subprocess, numpy as np, operator
import xml.etree.ElementTree as ET

def get_servers(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = []
    for server in root.iter('Server'):
        vms.append(server.get('name'))
    return vms

def get_sessions(domainName):
    sessions = {}
    command = subprocess.Popen('journalctl -o short-iso --since=yesterday --no-pager -tgameserver/{} -r ' \
                                '|grep -B1 -E \"driveName\"|grep -v -e \"windows\" -e \"launchers\"'.format(domainName),
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    
    stdout,stderr = command.communicate()
    data = stdout.split('\n')[:-1]
    started_sessions = len(data)
    for i in xrange(0, started_sessions, 3):
        session_id = data[i].rsplit(' ')[-4][:-1].strip()
        session_start = data[i].split(' ')[0][:-5].replace('T',' ')
        session_game = data[i+1].split("/")[-1]
        sessions[session_id] = [session_start,'',session_game]
    
    command = subprocess.Popen('journalctl -o short-iso --since=yesterday --no-pager -tgameserver/{} -r ' \
                                '|grep -E \"StopGameSession\"'.format(domainName),
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = command.communicate()
    data = stdout.split('\n')[:-1]
    
    for session in data:
        session_id = session.rsplit(' ')[-1].strip()
        session_end_time = session.split(' ')[0][:-5].replace('T',' ')
        sessions[session_id][1] = session_end_time
    

    for session_id,session_data in sessions.items():        
        if session_data[1]:
            command = subprocess.Popen("journalctl --since=\"{}\" --until=\"{}\" --no-pager -tgameserver/{} -r "\
                                    "|grep -e \"FPS (for last 5 sec)\"| awk '{{print $12}}'".format(session_data[0], session_data[1], domainName),
                shell=True,
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT)
            stdout,stderr = command.communicate()
            minutes = (time.mktime(time.strptime(session_data[1], "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(session_data[0], "%Y-%m-%d %H:%M:%S")))/60
            data = np.array([int(val) for val in stdout.split('\n')[:-1]])
            if len(data)>0:
                sessions[session_id].extend([int(minutes), int(np.percentile(data, 99)),])
            else:
                sessions[session_id].extend([int(minutes), 0])


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
