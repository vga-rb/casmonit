#!/usr/bin/env python

import requests
import time
import sys
import paramiko
import subprocess
import datetime
import os

#create dir and file-report
date = datetime.datetime.now()
date_now = (str(date.year) + '_' + str(date.month) + '_' + str(date.day))
subprocess.call(['mkdir', date_now])
dir_path = os.path.dirname(os.path.realpath(__file__)) + '/everyday_monitoring/' + date_now + '/'
name_repo = date_now + '.log'
file_repo = open(name_repo, 'a')
file_repo.write('MONITORING REPORT for ' + date_now + '\r\n' + '*** *** *** *** *** *** *** ***' + '\r\n')
file_repo.close()


# find Error in log-files
def monit_log(f_log, hostname, port, username, password):
    try:    
        sys.stdout = open('temp.file', 'a')
        client = paramiko.SSHClient() 
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        client.connect(hostname, port=port, username=username, password=password) 
        stdin, stdout, stderr = client.exec_command('cat ' + f_log) 
        print stdout.read()
        client.close()
        filename = hostname.replace('.', '_') + '.log'
        with open('temp.file', 'r') as f:
            for sub_str in f.readlines():
                if 'ERROR' in sub_str:
                    sys.stdout = open(filename, 'a')
                    print sub_str.rstrip('\r\n')
                    sys.stdout.close()
                elif 'Error' in sub_str:
                    sys.stdout = open(filename, 'a')
                    print sub_str.rstrip('\r\n')
                    sys.stdout.close()
                elif 'error' in sub_str:
                    sys.stdout = open(filename, 'a')
                    print sub_str.rstrip('\r\n')
        f.close()
    except Exception:
        print ('Could not connect to ', hostname)
    sys.stdout.close()
    subprocess.call(['rm', 'temp.file'])

#find statistics queue
def queue_report(rep_file, hostname,auth_pass):
    sys.stdout = open(rep_file, 'a')
    try:
        addr_queue = 'http://' + hostname + '/api/core/queued_datas'
        reqv_queue = requests.get(addr_queue, auth=('admin', auth_pass)) 
        count_queue = reqv_queue.json()['size']
        if count_queue != 0:
            print hostname, ' has queued datas: ', count_queue, '\r\n'
        else:
            print hostname, ' has no queue', '\r\n'
    except Exception:
        print ('Error request queue: ' + hostname + '\r\n')
    sys.stdout.close()

#find password from file
def ip_pass(pwdfile):
    result = []
    with open(pwdfile) as f:
        for line in f.readlines():
            ip, pwd = line.split(' ')
            result.append(ip + ' ' + pwd)
    return result

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



hostname = ()
password = ()
port = 22
username = 'aire'
app_log = '/home/aire/control/logs/app.log'
d_log = '/home/aire/daemon/daemon.log'
sys_log = '/var/log/syslog'

with open('ip_invent.txt') as f:
    for line in f.readlines():
        ip = line.rstrip('\r\n')
        req_status(ip)
 
with open(name_repo, 'a') as f:
    f.write('\r\n' + 'RUNNING' + '\r\n') 
    run = find_state('temp', 'running')
    for r in run:
        f.write(r + '\r\n')
    f.write('\r\n' + 'NOT RUNNING' + '\r\n')
    n_run = find_state('temp', 'not_running')
    for n in n_run:
        f.write(n + '\r\n')
    f.write('\r\n' + 'INIT' + '\r\n')
    ini = find_state('temp', 'init')
    for i in ini:
        f.write(i + '\r\n')
    f.write('\r\n' + 'UNKNOWN' + '\r\n')
    unk = find_state('temp', 'unknown')
    for u in unk:
        f.write(u + '\r\n')
    f.write('\r\n' + 'ERROR' + '\r\n')
    err = find_state('temp', 'error')
    for e in err:
        f.write(e + '\r\n')
    f.write('\r\n' + 'UNREACHABLE' + '\r\n')
    unr = find_state('temp', 'unreachable')
    for un in unr:
        f.write(un + '\r\n')
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
    f.write('Unreachable -' + str(count_unr) + '\r\n' + '*** *** *** ***' + '\r\n')
subprocess.call(['rm', 'temp'])

ps = ip_pass('ip_pas.txt')
for p in ps:
    hostname, pwd = p.split(' ')
    monit_log(app_log, hostname, port, username, pwd.rstrip('\r\n'))
    monit_log(d_log, hostname, port, username, pwd.rstrip('\r\n'))
    monit_log(sys_log, hostname, port, username, pwd.rstrip('\r\n'))
    subprocess.call(['mv', hostname.replace('.', '_') + '.log', dir_path])
    queue_report(name_repo, hostname, 'admin')
    queue_report(name_repo,hostname, 'adminctd')
subprocess.call(['mv', name_repo, dir_path])

