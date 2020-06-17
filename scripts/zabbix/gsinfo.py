#!/usr/bin/python -u
import select
from systemd import journal
from prometheus_client import start_http_server, Gauge, Info, Histogram
from prometheus_client.utils import INF
import random
import time
import xml.etree.ElementTree as ET

#Read VM names from GameServer config
def get_servers(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = []
    for server in root.iter('Server'):
        vms.append(server.get('name'))
    return vms


vms = get_servers()
session = {}
j = journal.Reader()
j.log_level(journal.LOG_INFO)
j.add_match(
    _SYSTEMD_UNIT=u'gameserver.service')
j.add_match(
    _SYSTEMD_UNIT=u'voloder.service')

j.seek_tail()
j.get_previous()
p = select.poll()
p.register(j, j.get_events())

fps_buckets = (0,10,20,30,40,50,60,70,80,90,100,120,INF)
ping_buckets = (0,5,10,15,20,25,30,35,40,45,50,60,70,80,90,100,120,150,200,INF)
gauge_fps_present = Gauge('gs_fps_present', 'FPS rendered by game',['vm'])
gauge_fps_customer = Gauge('gs_fps_customer', 'FPS got by customer',['vm'])
gauge_latency = Gauge('latency', 'Customer latency',['vm'])
'''
hist_fps_present = Histogram('hist_fps_present', 'Histogram FPS rendered by game', buckets=fps_buckets)
hist_fps_customer = Histogram('hist_fps_customer', 'Histogram FPS got by customer',buckets=fps_buckets)
hist_latency = Histogram('hist_latency', 'Latency Histogram',buckets=ping_buckets)
'''
session['id'],session['game'] = '',''
fps_present, fps_customer, latency = 0,0,0
info_session = Info('session', 'GameServer Session Data',['vm'])
start_http_server(8000)
while p.poll():
    if j.process() != journal.APPEND:
        continue
    for entry in j:
        log_message = entry['MESSAGE']
        if log_message != "":
            vm = entry['SYSLOG_IDENTIFIER'].split('/')[-1]
            if ' CreateSession: session_id' in log_message:
                session['id'] = log_message.split(' = ')[-1].split(' ')[-1]
                info_session.labels(vm=vm).info(session)
                gauge_fps_customer.labels(vm=vm).set(0)
                gauge_fps_present.labels(vm=vm).set(0)
                gauge_latency.labels(vm=vm).set(0)
                print("Session started at {}: {}".format(vm, session['id']))
            elif ' CreateSession: driveName ' in log_message:
                session['game'] = log_message.split('/')[-1]
                info_session.labels(vm=vm).info(session)
                print("VM: {} ID: {} G: {} GF: {} CF: {} L: {}".format(vm, session['id'], session['game'], fps_present, fps_customer, latency))
                #print("Session game: {}".format(session['game']))
            elif 'FPS (for last 5 sec)' in log_message:
                fps_customer = int(log_message.split(' U: ')[1].split(' ')[0])
                gauge_fps_customer.labels(vm=vm).set(fps_customer)
                #hist_fps_customer.observe(fps_customer)
                print("VM: {} ID: {} G: {} GF: {} CF: {} L: {}".format(vm, session['id'], session['game'], fps_present, fps_customer, latency))
                #print("Customer FPS: {}".format(fps_customer))
            elif 'Present (FPS' in log_message:
                fps_present = int(log_message.split('FPS = ')[1].split(')')[0])
                gauge_fps_present.labels(vm=vm).set(fps_present)
                #hist_fps_present.observe(fps_present)
                print("VM: {} ID: {} G: {} GF: {} CF: {} L: {}".format(vm, session['id'], session['game'], fps_present, fps_customer, latency))
                #print("Current FPS: {}".format(fps_present))
            elif 'Check session: session_id' in log_message:
                session['id'] = log_message.split(' ')[-1]
                print("VM: {} ID: {} G: {} GF: {} CF: {} L: {}".format(vm, session['id'], session['game'], fps_present, fps_customer, latency))
                info_session.labels(vm=vm).info(session)
            elif 'Ping (for last 5 sec)' in log_message:
                latency = int(log_message.split(': ')[-1].split(' ')[0])
                gauge_latency.labels(vm=vm).set(latency)
                #hist_latency.observe(latency)
                print("VM: {} ID: {} G: {} GF: {} CF: {} L: {}".format(vm, session['id'], session['game'], fps_present, fps_customer, latency))
            elif 'StopGameSession' in log_message:
                print("VM: {} ID: {} G: {} GF: {} CF: {} L: {}".format(vm, session['id'], session['game'], fps_present, fps_customer, latency))
                print("Session finished at {}: {}".format(vm, session['id']))
                session['id'],session['game'] = '',''
                fps_present, fps_customer, latency = 0,0,0
