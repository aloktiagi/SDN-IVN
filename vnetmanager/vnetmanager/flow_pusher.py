#!/usr/bin/python
import subprocess

class FlowPusher(object):
    def __init__(self, server):
        self.server = server

        self.addedPortList = {}
        self.addedMACList = {}

    def addflow(self, port, mac, vnet, outtable):

        vlan = vnet.vlan

        if vlan not in self.addedPortList.keys():
            self.addedPortList[vlan] = []

        self.addedPortList[vlan].append(port)

        if vlan not in self.addedMACList.keys():
            self.addedMACList[vlan] = []

        self.addedMACList[vlan].append(mac)

        ''' 
        print self.addedMACList
        for port in self.addedPortList:
            print port
        '''

        inflowstr = "table=0, priority=100, in_port=%d, vlan_tci=0, " \
                  + "dl_src=%s, actions=mod_vlan_vid:%d,resubmit(,%d)" \
                  % (port, mac, vlan, outtable)

        outflowstr = "table=%d, priority=100, dl_vlan=%d, dl_dst=%s, " \
                   + "actions=strip_vlan,output:%d" \
                   % (outtable, vlan, mac, port)


        fo = open("/tmp/flow", "wb")
        fo.write(inflowstr + "\n")
        fo.write(outflowstr)
        fo.close()
        subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', self.server, '/tmp/flow'])
        self.broadcast(self.addedPortList)

    def delflow(self, port, Mac):
        print self.addedMACList
        for port in self.addedPortList:
            print port
        dl_src = 'dl_src=' + Mac	
        dl_dst = 'dl_dst=' + Mac
        subprocess.call(['sudo', 'ovs-ofctl', 'del-flows', self.server, dl_src])
        subprocess.call(['sudo', 'ovs-ofctl', 'del-flows', self.server, dl_dst])
        self.addedPortList.remove(port)
        self.addedMACList.remove(Mac)
        self.broadcast(self.addedPortList)

    def broadcast(self, portList):
        fo = open("/tmp/flow", "wb")
        fo.write("table=1, priority=101,dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=strip_vlan,output:");
        for port in self.addedPortList: 
            fo.write(port);
            fo.write(",");
        fo.close()
        subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', self.server, '/tmp/flow'])

pusher = FlowPusher('s1')

pusher.addflow("1","00:00:00:00:00:01")
pusher.addflow("2","00:00:00:00:00:02")
pusher.addflow("3","00:00:00:00:00:03")
pusher.addflow("4","00:00:00:00:00:04")
#pusher.addflow("5","00:00:00:00:00:05")
#pusher.delflow("2","00:00:00:00:00:02")
