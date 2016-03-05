#!/usr/bin/env python

import requests
import sys
import datetime
import subprocess

hostname = ()
count_run = int()
count_not = int()
count_in = int()
count_un = int()
count_er = int()
count_unr = int()

date = datetime.datetime.now()
date_now = (str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '-' + str(date.hour))

def req_status(hostname):
    sys.stdout = open('temp', 'a')
    try:
        addr = 'http://' + hostname + '/api/core/status'
        r = requests.get(addr)
        if str(r) == '<Response [200]>':
            print hostname, r.json()['running']
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
 
with open(date_now + '_state.log', 'a') as f:
    f.write('AVAILABLE HOSTS' + '\r\n' + '*** *** *** ***' + '\r\n' + 'RUNNING' + '\r\n') 
    run = find_state('temp', 'running')
    for r in run:
        f.write(r + '\r\n')
    f.write('\r\n' + 'NOT RUNNING' + '\r\n')
    n_run = find_state('temp', 'not_running')
    for n in n_run:
        f.write(n + '\n')
    f.write('\r\n' + 'INIT' + '\r\n')
    ini = find_state('temp', 'init')
    for i in ini:
        f.write(i + '\n')
    f.write('\r\n' + 'UNKNOWN' + '\r\n')
    unk = find_state('temp', 'unknown')
    for u in unk:
        f.write(u + '\n')
    f.write('\r\n' + 'ERROR' + '\r\n')
    err = find_state('temp', 'error')
    for e in err:
        f.write(e + '\n')
    f.write('\r\n' + 'UNREACHABLE' + '\r\n')
    unr = find_state('temp', 'unreachable')
    for un in unr:
        f.write(un + '\n')
    f.write('\r\n' + '*** *** *** ***' + '\r\n' + 'TOTAL' + '\r\n')
    count_run = len(run)
    f.write('Running -' + str(count_run) + '\r\n')
    count_not = len(n_run)
    f.write('Not Running -' + str(count_not) + '\r\n')
    count_in = len(ini)
    f.write('Init -' + str(count_in) + '\r\n')
    count_un = len(unk)
    f.write('Unknoun -' + str(count_un) + '\r\n')
    count_er = len(err)
    f.write('Error -' + str(count_er) + '\r\n')
    count_unr = len(unr)
    f.write('Unreachable -' + str(count_unr))


