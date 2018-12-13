#!/usr/bin/env python

from HttpClient import Client

url = 'http://dev.snc.360es.cn:8181/restconf/operations/snc-device:get-device'
account = 'admin'
passwd = 'admin'

data = {'input': {}}

client = Client(account, passwd, url=url)

print client.post(data)
