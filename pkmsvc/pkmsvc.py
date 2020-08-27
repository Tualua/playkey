#!/usr/bin/python -u
import argparse, ConfigParser, json, platform, time, select, subprocess, libvirt, libvirt_qemu
import xml.etree.ElementTree as ET
from systemd import journal

def pkm_read_config(inifile='./pkm.ini'):
    config = ConfigParser.SafeConfigParser()
    vms_settings = {}
    config.read(inifile)
    sections = config.sections()
    if sections:
        for section in sections:
            vms_settings[section] = {}
            for item in config.items(section):
                vms_settings[section][item[0]] = item[1]
    else:
        print('ERROR: Empty config file!')
    return vms_settings


def pkm_read_gsconfig(path="/usr/local/etc/gameserver/conf.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    vms = {}
    for server in root.iter('Server'):
        vm = server.get('name')
        vms[vm]={}
        vms[vm]['dontmine'] = True
        vms[vm]['mining'] = False
        vms[vm]['ready'] = False
    return vms


#Wrapper for shell command excecution
def exec_shell_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = proc.communicate()
    if stderr:
        print(stderr)
    return stdout.split('\n')


def guest_exec(domain, cmd, args=[], timeout=6, flags=0, capture_output=True):
    command = json.dumps({
        "execute":"guest-exec",
        "arguments": {
            "path" : cmd,
            "arg" : args,
            "capture-output" : capture_output
        }
    })    
    result = None
    try:
        result = libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags)
    except libvirt.libvirtError as e:
        print(e)
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
        print(e)
        pass
    if response:
        response_json = json.loads(response)
        while (not response_json["return"]["exited"]):
            time.sleep(0.12)
            response_json = json.loads(libvirt_qemu.qemuAgentCommand(domain, command, timeout, flags))
        if "out-data" in response_json["return"].keys():
            result = str(response_json["return"]["out-data"]).decode('base64','strict')
            return result
        else:
            return ''


def print_response(vm, response):
    for line in response.split('\n'):
        print('{}: {}'.format(vm, line))


def attach_disk(vm):
    print('{}: Attaching disks'.format(vm))
    command = '/usr/local/bin/attach_disk.sh {} data/kvm/desktop/tools'.format(vm)
    result = exec_shell_command(command)
    for line in result:
        print('{}: {}'.format(vm, line))

def prepare_disk(domain):
    vm_name = domain.name()
    print('{}: Preparing disks'.format(vm_name))
    command = '/scripts/pkmsvc/prepare_disk.sh {}'.format(vm_name)
    result = exec_shell_command(command)
    pid = int(json.loads(result[1])['return']['pid'])
    for line in result:
        print('{}: {}'.format(vm_name, line))
    guest_exec_get_response(domain, pid)
    if detachToolsDisk(domain):
        print('{}: Detached temporary disk'.format(vm_name))
    else:
        print('{}: Error detaching temporary disk'.format(vm_name))

def getToolsDiskXML(domain):
    xml = ET.fromstring(domain.XMLDesc(0))
    tools_disk = ''
    for disk in xml.findall('./devices/disk'):
        if 'tools' in disk.find('source').get('dev'):
            tools_disk = ET.tostring(disk)
    if tools_disk:
        return tools_disk
    else:
        return None

def detachToolsDisk(domain):
    tools_disk = getToolsDiskXML(domain)
    if tools_disk:
        try:
            domain.detachDevice(tools_disk)
        except Exception:
            pass
            print("Error detaching Tools disk!")
            return False
        else:
            return True
    else:
        print('Tools disk is not attached to {}'.format(domain.name()))
        return False

def start_miner(domain, algo, server, user, pl):
    vm_name = domain.name()
    print('{}: Starting miner'.format(vm_name))
    host_name = platform.node().split('.', 1)[0]
    pid_miner = guest_exec(domain, "c:/temp/gminer/miner.exe", ['--algo', algo, '--server', server, '--user', '{}.{}-{}'.format(user,host_name,vm_name)], capture_output=False)
    if pid_miner:
        print('{}: Miner PID is {}'.format(vm_name, pid_miner))
        print('{}: Miner started'.format(vm_name))
        pid_smi = guest_exec(domain, "C:/Program Files/NVIDIA Corporation/NVSMI/nvidia-smi.exe", ['-i', '0', '-pl', pl])
        if pid_smi:
            response = guest_exec_get_response(domain, pid_smi)
            print_response(vm_name, response)
        else:
            print('{}: Error launching nvidia-smi! No PID returned!'.format(vm_name))
    else:
        print('{}: Error starting miner! No PID returned!'.format(vm_name))

def stop_miner(domain, pl):
    vm_name = domain.name()
    print('{}: Stopping miner'.format(vm_name))
    pid_miner = guest_exec(domain, "c:/windows/system32/taskkill.exe", ["-f", "-im", "miner.exe"])
    if pid_miner:
        response = guest_exec_get_response(domain, pid_miner)
        print_response(vm_name, response)
        print('{}: Miner stopped'.format(vm_name))
        pid_smi = guest_exec(domain, "C:/Program Files/NVIDIA Corporation/NVSMI/nvidia-smi.exe", ['-i', '0', '-pl', pl])
        if pid_smi:
            response = guest_exec_get_response(domain, pid_smi)
            print_response(vm_name, response)
        else:
            print('{}: Error launching nvidia-smi! No PID returned!'.format(vm_name))
    else:
        print('{}: CRITICAL ERROR! UNABLE TO STOP MINER!'.format(vm_name))


def print_status(vms):
    for k,v in vms.items():
        print('{}: {}'.format(k,v))


def main(args):
    vms = pkm_read_gsconfig()
    print("DEBUG: {}".format(vms))
    vms_settings = pkm_read_config()
    print("DEBUG: {}".format(vms_settings))
    print("DEBUG: {}".format(vms_settings.keys()))

    while True:
        try: 
            conn = libvirt.open('qemu:///system')
        except:
            pass
        if not conn:
            print ('Waiting for libvirt...')
            time.sleep(3)
        else:
            print("Connected to libvirt")
            break

    j = journal.Reader()
    j.log_level(journal.LOG_INFO)
    j.add_match(
        _SYSTEMD_UNIT=u'gameserver.service')

    j.seek_tail()
    j.get_previous()
    p = select.poll()
    p.register(j, j.get_events())
    while p.poll():
        if j.process() != journal.APPEND:
            continue
        for entry in j:
            log_message = entry['MESSAGE']
            if log_message != "":
                vm = entry['SYSLOG_IDENTIFIER'].split('/')[-1]
                if vm in vms_settings.keys():
                    if ' CreateSession: session_id' in log_message:
                        print('{}: Session start. Need to stop miner'.format(vm))
                        domain = conn.lookupByName(vm)
                        stop_miner(domain, vms_settings[vm]['defaultpl'])
                        vms[vm]['dontmine'] = True
                        vms[vm]['mining'] = False
                        print_status(vms)
                    elif 'Desktop.exe uploaded successfully' in log_message:
                        domain = conn.lookupByName(vm)
                        prepare_disk(domain)
                        vms[vm]['dontmine'] = False
                        vms[vm]['ready'] = True
                        print_status(vms)
                    elif 'Check session: session_id' in log_message and vms[vm]['mining']:
                        print('{}: Session check. Need to stop miner'.format(vm))
                        domain = conn.lookupByName(vm)
                        stop_miner(domain, vms_settings[vm]['defaultpl'])
                        vms[vm]['dontmine'] = True
                        vms[vm]['mining'] = False
                        print_status(vms)
                    elif 'shutdown vm' in log_message:
                        print('{}: VM shutdown'.format(vm))
                        vms[vm]['ready'] = False
                        vms[vm]['mining'] = False
                        vms[vm]['dontmine'] = False
                        print_status(vms)
                    elif 'Waiting for explorer' in log_message:
                        print('{}: VM startup'.format(vm))
                        attach_disk(vm)
                    else:
                        try: 
                            if not vms[vm]['dontmine'] and vms[vm]['ready'] and not vms[vm]['mining']:
                                start_miner(domain, vms_settings[vm]['algo'], vms_settings[vm]['server'], vms_settings[vm]['user'], vms_settings[vm]['pl'])
                                vms[vm]['mining'] = True
                                print_status(vms)
                        except:
                            print('Error starting miner on {}'.format(vm))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PlayKey Idle Mining Service')
    parser.add_argument('--config', type=str, action='store', dest="config_path", help='Path to config file', default="/scripts/pkmsvc/pkm.ini")
    args = parser.parse_args()
    main(args)
