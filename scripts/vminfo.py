import libvirt, libvirt_qemu
from contextlib import contextmanager
import json, time, sys
import xml.etree.ElementTree as ET

def get_servers(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = []
    for server in root.iter('Server'):
        vms.append(server.get('name'))
    return vms

def guest_exec(domain, cmd, args=[], timeout=6, flags=0):
    command = json.dumps({
        "execute":"guest-exec",
        "arguments": {
            "path" : cmd,
            "arg" : args,
            "capture-output" : True
        }
    })
    try:
        return json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))["return"]["pid"]
    except libvirt.libvirtError as e:
        return None


def guest_exec_get_response(domain, pid, timeout=6, flags=0):
    command = json.dumps({
        "execute": "guest-exec-status",
        "arguments": {
            "pid" : pid
        }
    })
    response = json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))
    while (not response["return"]["exited"]):
        time.sleep(0.12)
        response = json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))
    result = str(response["return"]["out-data"]).decode('base64','strict').splitlines()[0].split(", ")
    result.insert(0, domain.name())
    print result

def get_gpu_info(domain):
    pid = guest_exec(domain, 
            "C:/Program Files/NVIDIA Corporation/NVSMI/nvidia-smi.exe", 
            ["--query-gpu=name,pcie.link.gen.current,temperature.gpu,utilization.gpu,utilization.memory,power.draw","--format=csv,nounits,noheader"])
    guest_exec_get_response(domain, pid)

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system')
    sys.exit(1)

domainIDs = conn.listDomainsID()
if domainIDs == None:
    print('Failed to get a list of domain IDs')
    conn.close()
    sys.exit(1)
if len(domainIDs) != 0:
    for domainID in domainIDs:
        domain = conn.lookupByID(domainID)
        get_gpu_info(domain)

conn.close()
