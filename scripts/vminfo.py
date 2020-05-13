import libvirt, libvirt_qemu
from contextlib import contextmanager
import json, time, base64

def guest_exec(domain, cmd, args=[], timeout=6, flags=0):
    command = {
        "execute":"guest-exec",
        "arguments": {
            "path" : cmd,
            "arg" : args,
            "capture-output" : True
        }
    }
    command_json = json.dumps(command, sort_keys=False)    
    pid = json.loads(libvirt_qemu.qemuAgentCommand(domain, command_json, timeout, flags))["return"]["pid"]
    return pid

def guest_exec_get_response(domain, pid, timeout=6, flags=0):
    command = json.dumps({
        "execute": "guest-exec-status",
        "arguments": {
            "pid" : pid
        }
    })
    response = json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))
    while (not response["return"]["exited"]):
        time.sleep(0.1)
        response = json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))
    result = base64.decodestring(response["return"]["out-data"])    
    print(result)

def get_gpu_info(domain):
    pid = guest_exec(domain, 
            "C:/Program Files/NVIDIA Corporation/NVSMI/nvidia-smi.exe", 
            ["--query-gpu=temperature.gpu,utilization.gpu,utilization.memory,power.draw","--format=csv,nounits,noheader"])
    guest_exec_get_response(domain, pid)

conn = libvirt.open('qemu:///system')
if conn == None:
    print('Failed to open connection to qemu:///system')
    exit(1)

domainNames = conn.listDefinedDomains()
domainIDs = conn.listDomainsID()
if domainIDs == None:
    print('Failed to get a list of domain IDs')
if len(domainIDs) != 0:
    for domainID in domainIDs:
        domain = conn.lookupByID(domainID)
        name = domain.name()        
        get_gpu_info(domain)

conn.close()
