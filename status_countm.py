#!/usr/bin/env python

import requests
import sys
import datetime
import subprocess
import re

hostname = ()
count_run = int()
count_unr = int()

date = datetime.datetime.now()
date_now = (str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '-' + str(date.hour))

def req_status(hostname):
    sys.stdout = open('temp_count', 'a')
    re_name = re.compile("alt=\"(.*?)\"/>")
    try:
        addr = 'http://' + hostname + '/footer.html'
        r = requests.get(addr)
        if str(r) == '<Response [200]>':
            state = re_name.findall(r.content)
            print hostname, str(state).lstrip("['").rstrip("']")
    except Exception:
        print hostname, 'unreachable'
    sys.stdout.close() 



def find_state(filename, state_host):
    result = []
    with open(filename) as f:
        for line in f.readlines():
            ip, state = line.split(' ')
            if state.rstrip('\r\n') == state_host:
                result.append(ip)
    return result



with open('ip_invent.txt') as f:
    for line in f.readlines():
        ip = line.rstrip('\r\n')
        req_status(ip)
 
with open(date_now + '_countMax.log', 'a') as f:
    f.write('AVAILABLE HOSTS' + '\n' + '*** *** *** ***' + '\n') 
    run = find_state('temp_count', 'CountMax')
    for r in run:
        f.write(r + '\n')
    f.write('\n' + 'UNREACHABLE' + '\n')
    unr = find_state('temp_count', 'unreachable')
    for un in unr:
        f.write(un + '\n')
    f.write('\n' + '*** *** *** ***' + '\n' + 'TOTAL' + '\n')
    count_run = len(run)
    f.write('Running -' + str(count_run) + '\n')
    count_unr = len(unr)
    f.write('Unreachable -' + str(count_unr))

