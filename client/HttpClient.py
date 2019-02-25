#!/usr/bin/env python

from urllib2 import Request, urlopen, HTTPError, URLError
from base64 import encodestring
import json


class Client:
    """http client"""

    __account = 'admin'
    __password = 'admin'
    __contentType = 'application/json'
    __cookie_expected = None
    __captcha = None
    __url = None

    def __init__(self, account=None, password=None, contentType=None, captcha=None, url=None):
        if account is not None:
            self.__account = account
        if password is not None:
            self.__password = password
        if contentType is not None:
            self.__contentType = contentType
        if captcha is not None:
            self.__captcha = captcha
        if url is not None:
            self.__url = url

    def setUrl(self, url):
        self.__url = url

    def setAccount(self, account):
        self.__account = account

    def setPassword(self, password):
        self.__password = password

    def setContentType(self, contentType):
        self.__contentType = contentType

    def setCaptcha(self, captcha):
        self.__captcha = captcha

    def post(self, data=None):
        if data is None:
            data = {}
        result = self.__open(data)
        if result is not None and result is not '':
            try:
                return json.loads(result)
            except ValueError as err:
                print('error: ' + str(err))
                return result

    def get(self, data=None):
        result = self.__open(data)
        if result is not None:
            try:
                return json.loads(result)
            except ValueError as err:
                print('error: ' + str(err))
                return result

    def put(self, data=None):
        if data is None:
            data = {}
        return self.__open(data, method='PUT')

    def delete(self, data=None):
        return self.__open(data, method='DELETE')

    def __build(self):
        if self.__url is None:
            return
        request = Request(self.__url)
        b64str = encodestring('%s:%s' % (self.__account, self.__password))[:-1]
        request.add_header('Authorization', 'Basic {}'.format(b64str))
        request.add_header('Content-type', self.__contentType)
        if self.__captcha is not None:
            request.add_header('captcha', self.__captcha)
        return request

    def __open(self, data=None, method=None):
        request = self.__build()
        if method is not None:
            request.get_method = lambda: method
        if data is not None:
            request.add_data(json.dumps(data))
        res = None
        try:
            res = urlopen(request)
            return res.readline()
        except (HTTPError, URLError) as err:
            print('error: ' + str(err))
        finally:
            if res is not None:
                res.close()
