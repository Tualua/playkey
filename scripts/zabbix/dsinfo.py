#!/usr/bin/python
import sys,subprocess, json

#Wrapper for shell command excecution
def exec_shell_command(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout,stderr = proc.communicate()
    return stdout.split('\n')

def get_datasets():
    zfslist = 'zfs list -o name,used,avail -r data/kvm/desktop -H'
    cmd = exec_shell_command(zfslist)
    totalused = float(cmd[0].split('\t')[1][:-1])
    avail = float(cmd[0].split('\t')[2][:-1])
    
    del cmd[0]
    filtered = [i for i in cmd if '-vm' not in i]
    datasets={}
    for line in filtered[:-1]:
        dataset = line.split('\t')[0].split('/')[-1]
        path = line.split('\t')[0]
        size = float(line.split('\t')[1][:-1])
        last_snapshot = exec_shell_command('zfs list -t snapshot -o name -s creation -r {} -H'.format(path))[-2].split('/')[-1]
        datasets[dataset] = {'path': path,'used': size, 'last_snapshot': last_snapshot}
    return totalused, avail, datasets

discovery = {}
discovery["values"] = {}
discovery["lld"] = []

totalused, avail, datasets = get_datasets()
discovery['values']['summary'] = {'used' : totalused, 'avail' : avail}

for dataset in datasets:
    discovery['lld'].append({'{#DATASET}' : dataset})
    discovery['values'][dataset] = datasets[dataset]

print(json.dumps(discovery, sort_keys=True, indent=4))
