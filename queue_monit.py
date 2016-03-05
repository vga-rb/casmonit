#!/usr/bin/env python

import requests
import sys
import json


"""  set ntp-server in Network
ntp_srv - dns-name or IP-address ntp-server as ["ms-ntp001.vimpelcom.ru"], 192.168.0.15
afte apply server synchronyses
"""
def queue_report(hostname,auth_pass):
    sys.stdout = open('queue.log', 'a')
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

with open('ip_available.txt') as f:
    for line in f.readlines():
        ip = line.rstrip('\r\n')
        addr = 'http://' + ip + '/api/core/network'
        r = requests.get(addr, auth=('admin', 'adminctd'))
        if str(r) == '<Response [200]>':
            queue_report(ip, 'adminctd')
        elif str(r) == '<Response [401]>':
            queue_report(ip, 'admin')
