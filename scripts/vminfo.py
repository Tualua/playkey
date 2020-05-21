#!/usr/bin/python

import libvirt, libvirt_qemu
import json, time, sys, subprocess
import xml.etree.ElementTree as ET

def get_servers(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = []
    for server in root.iter('Server'):
        vms.append(server.get('name'))
    return vms

def get_last_session(domainName):
    command = subprocess.Popen('journalctl -o short-iso --since=yesterday --no-pager -tgameserver/{} -r ' \
                                '|grep -B1 -m 1 -E \"driveName\"|grep -v -e \"windows\" -e \"launchers\"'.format(domainName),
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = command.communicate()
    data = stdout.split('\n')    
    last_session_id = data[0].rsplit(' ')[-4][:-1].strip()
    last_session_time = time.strptime(data[0].split(' ')[0][:-5], "%Y-%m-%dT%H:%M:%S")
    last_game = data[1].split("/")[-1]

    command = subprocess.Popen('journalctl -o short-iso --since=yesterday --no-pager -tgameserver/{} -r ' \
                                '|grep -m 1 -E \"UserSessionEnd:.*\"'.format(domainName),
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = command.communicate()
    last_session_end = stdout.rsplit(' ')[-1].strip()

    if last_session_id == last_session_end:
        last_session_status = 'Finished'
    else:
        last_session_status = 'Active'
    
    session = [last_game, last_session_id, last_session_status]
    return session

def guest_exec(domain, cmd, args=[], timeout=6, flags=0):
    command = json.dumps({
        "execute":"guest-exec",
        "arguments": {
            "path" : cmd,
            "arg" : args,
            "capture-output" : True
        }
    })    
    result = None
    try:
        result = libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags)
    except libvirt.libvirtError as e:
        pass
    if result:
        return json.loads(result)["return"]["pid"]
    else:
        return None


def guest_exec_get_response(domain, pid, timeout=6, flags=0):
    command = json.dumps({
        "execute": "guest-exec-status",
        "arguments": {
            "pid" : pid
        }
    })
    try:
        response = libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags)
    except libvirt.libvirtError as e:
        pass    
    if response:        
        response_json = json.loads(response)
        while (not response_json["return"]["exited"]):
            time.sleep(0.12)
            response_json = json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))
        result = str(response_json["return"]["out-data"]).decode('base64','strict')
        return result


def get_gpu_info(domain):
    result = {}
    pid = guest_exec(domain, 
            "C:/Program Files/NVIDIA Corporation/NVSMI/nvidia-smi.exe", 
            ["--query-gpu=name,pcie.link.gen.current,temperature.gpu,utilization.gpu,utilization.memory,power.draw","--format=csv,nounits,noheader"])    
    if pid:
        response = guest_exec_get_response(domain, pid)
        result = response.splitlines()[0].split(", ")        
    else:
        result = ['',0,0,0,0,0,0]
    return result

vmsinfo = {}
vmsinfo["values"] = {}
vmsinfo["lld"] = []


conn = libvirt.open('qemu:///system')
if conn == None:
    print json.dumps(vmsinfo, sort_keys=True, indent=4)
    sys.exit(1)

defined_servers = get_servers()
active_servers = []
if defined_servers:
    for server in defined_servers:
        vmsinfo["lld"].append({'{#VMNAME}' : server})
        vmsinfo["values"].update({server:[]})
        dom = conn.lookupByName(server)
        if dom != None:
            vmsinfo["values"][server].append("up")
            active_servers.append(dom)
        else:
            vmsinfo["values"][server].append("down")
            vmsinfo["values"][server].extend(['',0,0,0,0,0,0])
            vmsinfo["values"][server].extend(get_last_session(server.name()))
if active_servers:
    for server in active_servers:
        vmsinfo["values"][server.name()].extend(get_gpu_info(server))
        vmsinfo["values"][server.name()].extend(get_last_session(server.name()))

print json.dumps(vmsinfo, sort_keys=True, indent=4)

conn.close()
