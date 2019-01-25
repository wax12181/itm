#!/usr/bin/env python
# coding=utf-8

import networkx as nx
import matplotlib.pyplot as plt
from Tkinter import Button, Label, Text
from nspm.api import Topology


class TopologyGraph:
    __digraph = nx.DiGraph()
    __topology = None
    __source = None
    __destination = None
    __protocol = None
    __dPort = None

    def __init__(self, nspm_address):
        self.__topology = Topology(nspm_address)
        self.__digraph = nx.DiGraph()
        self.__importTopology(self.__topology.getTopology())

    def __importTopology(self, date):
        pass

    def find(self):
        print self.__source.get()
        print "hello world"
        print "hello world"
        print "hello world"

    def show(self):
        nx.draw(self.__digraph)

        Label(text='源IP').pack({"side": "left"})
        self.__source = Text(width=20, height=1)
        self.__source.pack({"side": "left"})

        Label(text='目的IP').pack({"side": "left"})
        self.__destination = Text(width=20, height=1)
        self.__destination.pack({"side": "left"})

        Label(text='协议').pack({"side": "left"})
        self.__protocol = Text(width=20, height=1)
        self.__protocol.pack({"side": "left"})

        Label(text='目的端口').pack({"side": "left"})
        self.__dPort = Text(width=20, height=1)
        self.__dPort.pack({"side": "left"})

        find = Button(text="寻路", command=self.find)
        find.pack()
        plt.show()
