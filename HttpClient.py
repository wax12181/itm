#!/usr/bin/env python

from urllib2 import Request, urlopen
from base64 import encodestring
import json


class Client:
    'http client'

    __account = 'admin'
    __password = 'admin'
    __url = None

    def __init__(self, account=None, password=None, url=None):
        if account is not None:
            self.__account = account
        if password is not None:
            self.__password = password
        if url is not None:
            self.__url = url

    def setUrl(self, url):
        self.__url = url

    def setAccount(self, account):
        self.__account = account

    def setPassword(self, password):
        self.__password = password

    def post(self, data):
        request = self.__build()
        request.add_data(json.dumps(data))
        return self.__open(request)

    def __build(self):
        if self.__url is None:
            return
        request = Request(self.__url)
        b64str = encodestring('%s:%s' % (self.__account, self.__password))[:-1]
        request.add_header('Authorization', 'Basic %s' % b64str)
        request.add_header('Content-type', 'application/json')
        return request

    def __open(self, request):
        res = urlopen(request)
        result = res.readline()
        res.close()
        return json.dumps(json.loads(result), indent=4)
