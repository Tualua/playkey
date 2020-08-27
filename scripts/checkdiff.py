#!/usr/bin/python -u
import urllib, json, collections
from bs4 import BeautifulSoup
from datetime import datetime

games = { 40: 'csgo', 48: 'dota2', 38: 'fortnite', 46: 'fortnite', 35: 'gta5', 47: 'overwatch', 39: 'pubg', 43: 'rdr2', 45: 'tarkov', 49: 'thestore',
          51: 'warhammer', 44: 'warzone', 37: 'witcher', 53: 'wot', 52: 'wow', 54: 'bannerlord', 30: 'launchers', 32: 'windows' }


def load_last_check_result(result_path='/var/cache/checkdiff/last_check.txt'):
    try:
        with open(result_path) as json_file:
            data = json.loads(json_file.read())
    except IOError:
        print('Error opening last result!')
        return None
    result = collections.OrderedDict(sorted(data.items()))
    return result


def save_check_result(data, result_path='/var/cache/checkdiff/last_check.txt'):
    json_file = open(result_path, 'w')
    json.dump(data, json_file, indent=4)

def get_diff_info(games, base_url="http://92.223.101.6:81"):
    html = urllib.urlopen(base_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    diffs = {}
    diffs_a = soup.find_all('a')
    for link in diffs_a:
        diff_name = str(link.get('href'))
        if 'drive' in diff_name:
            diff_info = str(link.next_sibling).strip().split(' ')
            diffs[diff_name] = {}
            diffs[diff_name]['url'] = '{}/{}'.format(base_url,diff_name)
            try:
                diffs[diff_name]['size'] = int(diff_info[-1])
            except ValueError:
                diffs.pop(diff_name)
                pass
            else:
                if len(diff_name.split('_'))>1:
                    diffs[diff_name]['game'] = games[int(diff_name.split('_')[1].split('.')[0])]
                    diffs[diff_name]['snapshot'] = int(diff_name.split('_')[3].split('.')[0])
                else:
                    diffs[diff_name]['game'] = diff_name
                diffs[diff_name]['date'] = str.join(' ',diff_info[0:2])
    result = collections.OrderedDict(sorted(diffs.items()))
    return result


def get_latest_snapshots(diffs):
    result = {}
    for diff in diffs.values():
        if diff['game'] in result.keys():
            if diff['snapshot'] > result[diff['game']]:
                result[diff['game']] = diff['snapshot']
        else:
            result[diff['game']] = diff['snapshot']
    return result

def check_for_updates(diffs_old, diffs_new):
    updates = {}
    for k,v in diffs_new.items():
        if k in diffs_old.keys():
            date_old = datetime.strptime(v['date'], "%d-%b-%Y %H:%M")
            date_new = datetime.strptime(diffs_old[k]['date'], "%d-%b-%Y %H:%M")
            if v['size'] != diffs_old[k]['size'] or date_new != date_old:
                updates[k]=v
    return updates


def main():
    last_check_result = load_last_check_result()
    if last_check_result:
        print("Previous diff count: {}".format(len(last_check_result)))
    else:
        print("Previous check result not found!")
    diffs = get_diff_info(games)
    print("Current diff count: {}".format(len(diffs)))
    latest = get_latest_snapshots(diffs)
    for k in sorted(latest):
        print('{}: {}'.format(k,latest[k]))
    updates = check_for_updates(last_check_result, diffs)
    if len(updates):
        for v in updates.values():
            print('{} updated to {} on {}'.format(v['game'], v['snapshot'], v['date']))
    else:
        print('No updates found since last check!')
    save_check_result(diffs)

if __name__ == "__main__":
    main()


