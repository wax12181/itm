#!/usr/bin/env python
# coding=utf-8

from http.HttpClient import Client


class Api:
    __baseUrl = None
    __client = Client()

    def __init__(self, nspm_address, port=8080):
        self.__baseUrl = 'http://' + str(nspm_address) + ':' + str(port) + '/api/v1/'

    def url(self):
        return self.__baseUrl

    def getClient(self):
        return self.__client


class Device(Api):
    def getDevices(self):
        self.getClient().setUrl(self.url() + 'devices?pageNum=1&pageSize=100')
        return self.getClient().get().get('items')

    def getRoutes(self, deviceId):
        self.getClient().setUrl(self.url() + 'device-data/' + deviceId + '/routers?pageNum=1&pageSize=100')
        return self.getClient().get().get('items')

    def queryRoutes(self, deviceId, routeType='INDIRECT'):
        routes = self.getRoutes(deviceId)
        result = []
        if routes is not None:
            for r in routes:
                if r.get('type') == routeType:
                    result.append(r)
        return result

    def getInterfaces(self, deviceId):
        self.getClient().setUrl(self.url() + 'device-data/' + deviceId +
                                '/physical-interfaces?pageNum=1&pageSize=100')
        return self.getClient().get().get('items')

    def queryInterfaces(self, deviceId, ipIsNotNone=True):
        interfaces = self.getInterfaces(deviceId)
        result = []
        if interfaces is None:
            return result
        if ipIsNotNone:
            for tp in interfaces:
                if tp.get('ipItems') is not None:
                    result.append(tp)
        return result


class Topology(Api):
    def getStartPoint(self):
        self.getClient().setUrl(self.url() + 'topology/start-points')
        return self.getClient().get()

    def getTopology(self):
        self.getClient().setUrl(self.url() + 'topology')
        return self.getClient().get()

    def getNodes(self):
        topology = self.getTopology()
        if topology is None:
            return None
        return topology.get("nodes")

    def getLines(self):
        topology = self.getTopology()
        if topology is None:
            return None
        return topology.get("lines")

    def getNodeByIp(self, ip):
        nodes = self.getNodes()
        if nodes is None:
            return None
        for n in nodes:
            if n.get('host') == ip:
                return n
        return None

    def getNodeIdByIp(self, ip):
        node = self.getNodeByIp(ip)
        if node is None:
            return None
        return node.get('id')

    def removeLineById(self, lineId):
        self.getClient().setUrl(self.url() + 'topology/lines' + lineId)
        self.getClient().delete()


class Tighten(Api):
    def getConfig(self):
        self.getClient().setUrl(self.url() + 'shrink-config')
        return self.getClient().get()

    def setConfig(self, data):
        self.getClient().setUrl(self.url() + 'shrink-config')
        self.getClient().post(data)
