#!/usr/bin/python

import libvirt
import libvirt_qemu
import json
import time
import sys
import argparse
import xml.etree.ElementTree as ET

NVIDIA_SMI_PATH = "C:/Windows/System32/DriverStore/FileRepository/nv_dispi.inf_amd64_5dcb5bbf5c3edcf2/nvidia-smi.exe"


def get_servers(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = []
    for server in root.iter('Server'):
        vms.append(server.get('name'))
    return vms


def guest_exec(domain, cmd, args=[], timeout=6, flags=0):
    command = json.dumps({
        "execute": "guest-exec",
        "arguments": {
            "path": cmd,
            "arg": args,
            "capture-output": True
        }
    })
    result = None
    try:
        result = libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags)
    except libvirt.libvirtError:
        pass
    if result:
        return json.loads(result)["return"]["pid"]
    else:
        return None


def guest_exec_get_response(domain, pid, timeout=6, flags=0):
    command = json.dumps({
        "execute": "guest-exec-status",
        "arguments": {
            "pid": pid
        }
    })
    try:
        response = libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags)
    except libvirt.libvirtError:
        pass
    if response:
        response_json = json.loads(response)
        while (not response_json["return"]["exited"]):
            time.sleep(0.12)
            response_json = json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))
        try:
            result = str(response_json["return"]["out-data"]).decode('base64', 'strict')
        except KeyError:
            result = ''
            print >> sys.stderr, "VM: {}, CPU: {}".format(domain.name(), response_json)
        return result


def get_gpu_info(domain):
    result = {
        'name': '',
        'memory': 0,
        'pciegen': 0,
        'temp': 0,
        'util': 0,
        'memutil': 0,
        'power': 0,
        'fans': 0
    }
    pid = guest_exec(domain, NVIDIA_SMI_PATH, ["-q", "-x"])
    if pid:
        response = guest_exec_get_response(domain, pid)
        smi = ET.fromstring(response)
        # GPU Name
        result['name'] = smi.findall('./gpu/product_name')[0].text
        # GPU Memory
        result['memory'] = int(smi.findall('./gpu/fb_memory_usage/total')[0].text.split(' ')[0])
        # PCI-E Generation
        result['pciegen'] = int(smi.findall('./gpu/pci/pci_gpu_link_info/pcie_gen/current_link_gen')[0].text)
        # GPU Temperature
        result['temp'] = int(smi.findall('./gpu/temperature/gpu_temp')[0].text.split(' ')[0])
        # GPU Utilization
        result['util'] = int(smi.findall('./gpu/utilization/gpu_util')[0].text.split(' ')[0])
        # GPU Memory Utilization
        result['memutil'] = int(smi.findall('./gpu/utilization/memory_util')[0].text.split(' ')[0])
        # GPU Encoder Utilization
        result['encutil'] = int(smi.findall('./gpu/utilization/encoder_util')[0].text.split(' ')[0])
        # GPU Encoder FPS
        result['encfps'] = int(smi.findall('./gpu/encoder_stats/average_fps')[0].text.split(' ')[0])
        # GPU Power
        result['power'] = float(smi.findall('./gpu/power_readings/power_draw')[0].text.split(' ')[0])
        # GPU Fans
        result['fans'] = int(smi.findall('./gpu/fan_speed')[0].text.split(' ')[0])

    return result


def get_mem_info(domain):
    result = {
        'total': 0,
        'free': 0,
        'util': 0,
    }
    pid = guest_exec(domain,
                     "wmic.exe",
                     ['OS',
                      'get', 'TotalVisibleMemorySize,FreePhysicalMemory,TotalVirtualMemorySize,FreeVirtualMemory'])
    if pid:
        response = guest_exec_get_response(domain, pid)
        mem = response.splitlines()[2].split()
        result['total'] = float(mem[3])*1024
        result['free'] = float(mem[0])*1024
        if result['total'] and result['free']:
            result['util'] = (1-result['free']/result['total'])*100
        else:
            result['util'] = 0
    return result


def get_cpu_info(domain):
    result = {
        'cores': 0,
        'threads': 0,
        'threadcount': 0,
        'util': 0
    }
    pid = guest_exec(domain,
                     "wmic.exe",
                     ['cpu', 'get', '/value'])
    if pid:
        response = filter(len, guest_exec_get_response(domain, pid).splitlines())
        cpu = dict(s.split('=') for s in response)
        result['cores'] = int(cpu['NumberOfEnabledCore'])
        result['threads'] = int(cpu['NumberOfLogicalProcessors'])
        result['threadcount'] = int(cpu['ThreadCount'])
        if cpu['LoadPercentage']:
            result['util'] = int(cpu['LoadPercentage'])
        else:
            result['util'] = 0
    return result


def main(args):
    vminfo = {}
    vminfo["values"] = {}
    vminfo["values"][args.vm] = {}
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print json.dumps(vminfo, sort_keys=True, indent=4)
        sys.exit(1)

    try:
        dom = conn.lookupByName(args.vm)
    except libvirt.libvirtError:
        vminfo["values"][args.vm]['status'] = "down"
        vminfo["values"][args.vm]['gpu'] = {
            'name': '',
            'memory': '',
            'pciegen': '',
            'temp': '',
            'util': '',
            'memutil': '',
            'encutil': '',
            'encfps': '',
            'power': '',
            'fans': ''
        }
        vminfo["values"][args.vm]['memory'] = {
            'total': '',
            'free': '',
            'util': '',
        }
        vminfo["values"][args.vm]['cpu'] = {
            'cores': '',
            'threads': '',
            'threadcount': '',
            'util': ''
        }
    else:
        vminfo["values"][args.vm]['status'] = "up"
        vminfo["values"][args.vm]['gpu'] = get_gpu_info(dom)
        vminfo["values"][args.vm]['memory'] = get_mem_info(dom)
        vminfo["values"][args.vm]['cpu'] = get_cpu_info(dom)

    print json.dumps(vminfo, sort_keys=True, indent=4)

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PlayKey VM data retriever')
    parser.add_argument('vm', type=str, action='store', help='VM Name')
    args = parser.parse_args()
    main(args)
