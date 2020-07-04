#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

# Configure here.
ali_accessKeyId = '<your accessKeyId>'
ali_accessSecret = '<your accessSecret>'
rr = '<your resource records>'
ipv6 = '<your ipv6 address>'
domain = '<your domain name>'
# End configure.

client = AcsClient(ali_accessKeyId, ali_accessSecret, 'default')

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('alidns.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2015-01-09')
request.set_action_name('AddDomainRecord')

request.add_query_param('DomainName', domain)
request.add_query_param('RR', rr)
request.add_query_param('Type', 'AAAA')
request.add_query_param('Value', ipv6)

response = client.do_action(request)
print(str(response, encoding = 'utf-8'))