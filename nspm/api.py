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

    # node
    def importNodes(self, data):
        self.getClient().setUrl(self.url() + 'topology/nodes')
        self.getClient().put(data)

    def getNodes(self):
        topology = self.getTopology()
        if topology is None:
            return None
        return topology.get("nodes")

    def queryNode(self, host=None, name=None):
        nodes = self.getNodes()
        result = []
        for node in nodes:
            if host is not None and host != node.get('host'):
                continue
            if name is not None and name != node.get('name'):
                continue
            result.append(node)
        return result

    def getNodeIdByIp(self, host):
        nodes = self.queryNode(host=host)
        if nodes is None:
            return None
        return nodes[0].get('id')

    # subnet
    def addSubnet(self, data):
        self.getClient().setUrl(self.url() + 'topology/subnets')
        self.getClient().post(data)

    def removeSubnet(self, subnetId):
        self.getClient().setUrl(self.url() + 'topology/subnets/' + subnetId)
        self.getClient().delete()

    def querySubnet(self, networkSegment=None):
        result = []
        topology = self.getTopology()
        if topology is None:
            return []
        for subnet in topology.get("subnets"):
            if networkSegment is not None and networkSegment != subnet.get('networkSegment'):
                continue
            result.append(subnet)
        return result

    # line
    def addLine(self, data):
        self.getClient().setUrl(self.url() + 'topology/lines')
        self.getClient().post(data)

    def removeLine(self, lineId):
        self.getClient().setUrl(self.url() + 'topology/lines/' + lineId)
        self.getClient().delete()

    def queryLine(self, subnet=None, node=None):
        topology = self.getTopology()
        result = []
        if topology is None:
            return result
        for line in topology.get("lines"):
            if subnet is not None and subnet != line.get('subnet'):
                continue
            if node is not None and node != line.get('tp').get('node'):
                continue
            result.append(line)
        return result

    # link
    def addLink(self, data):
        self.getClient().setUrl(self.url() + 'topology/links')
        self.getClient().post(data)

    def removeLink(self, linkId):
        self.getClient().setUrl(self.url() + 'topology/links/' + linkId)
        self.getClient().delete()

    def queryLink(self, linkType=None, srcNode=None, srcTpName=None, dstNode=None, dstTpName=None):
        topology = self.getTopology()
        result = []
        if topology is None:
            return result
        for link in topology.get("links"):
            if linkType is not None and linkType != link.get('linkType'):
                continue
            if srcNode is not None and srcNode != link.get('source').get('node'):
                continue
            if srcTpName is not None and srcTpName != link.get('source').get('name'):
                continue
            if dstNode is not None and dstNode != link.get('destination').get('node'):
                continue
            if dstTpName is not None and dstTpName != link.get('destination').get('name'):
                continue
            result.append(link)
        return result


class Tighten(Api):
    def getConfig(self):
        self.getClient().setUrl(self.url() + 'shrink-config')
        return self.getClient().get()

    def setConfig(self, data):
        self.getClient().setUrl(self.url() + 'shrink-config')
        self.getClient().post(data)
