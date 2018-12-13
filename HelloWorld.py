#!/usr/bin/env python

from urllib2 import Request, urlopen
from base64 import encodestring
import json

url = 'http://dev.snc.360es.cn:8181/restconf/operations/snc-device:get-device'
account = 'admin'
passwd = 'admin'

data = {'input': {}}

req = Request(url, json.dumps(data))

b64str = encodestring('%s:%s' % (account, passwd))[:-1]

req.add_header('Authorization', 'Basic %s' % b64str)
req.add_header('Content-type', 'application/json')

res = urlopen(req)

result = res.readline()

print json.dumps(json.loads(result), indent=4)

res.close()
