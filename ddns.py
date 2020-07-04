#!/usr/bin/env python
#coding=utf-8

import os
import time
import requests
import re
import subprocess
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# Configure here.
ali_accessKeyId = '<your accessKeyId>'
ali_accessSecret = '<your accessSecret>'

# Your resource records and record id here.
# record id got in alidnsadd.py.
rr_list = [
    ['ipv6', '10000000000000000'] # for ipv6.yourdomain.com
]

def ddns_ipv6():
    ipv6_address_last = None
    while(True):
        #get ipv6 address from windows
        #ipv6_address_current = get_Local_ipv6_address()
        #get ipv6 address from linux server
        ipv6_address_current = get_Local_linux_ipv6_address()
        if not ipv6_address_last == ipv6_address_current:
            print('[%s]'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print('domain name is not the same, changing ....')
            
            for rr in rr_list:
                alidns_update(ipv6_address_current,rr[1],rr[0],'AAAA')

            ipv6_address_last = ipv6_address_current
            print('domain name have been changed, wait next time check after 600 s')
        else:
            print('domain name is the same, wait next time check after 600 s')
        time.sleep(600)

def alidns_update(ipv6_address=None,RecordId=None,RR=None,Type=None):
    client = AcsClient(ali_accessKeyId, ali_accessSecret, 'default')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('alidns.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2015-01-09')
    request.set_action_name('UpdateDomainRecord')

    request.add_query_param('RecordId', RecordId)
    request.add_query_param('RR', RR)
    request.add_query_param('Type', Type)
    request.add_query_param('Value', ipv6_address)

    response = client.do_action(request)
    print(response)

def get_Local_ipv6_address():
    """
        Get local ipv6
    """
    pageURL='http://ipv6.sjtu.edu.cn/'
    content=requests.get(pageURL).content

    ipv6_pattern='(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})'

    m = re.search(ipv6_pattern, content)

    if m is not None:
        return str(m.group())
    else:
        return None

def get_Local_linux_ipv6_address():
    (status, output) = subprocess.getstatusoutput("ifconfig|grep inet6|grep global|grep 'prefixlen 64'|awk '{print $2}'|sed -n '1p'")
    return str(output)

if __name__ == "__main__":
    ddns_ipv6()