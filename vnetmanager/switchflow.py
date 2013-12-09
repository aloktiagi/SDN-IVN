#!/usr/bin/python
import subprocess
import flask
from vnetmanager import db, app
from vnetmanager.models import *

'''
switchlist = []
switchlist.append("s2")
switchlist.append("s1")
switchlist.append("s4")
srcmac = "4e:ce:8c:e1:29:aa"
dstmac = "fa:91:d5:03:4e:9c"
'''

def pushflow(swid, flowstrs):

    with open("/tmp/flow", "wb") as fo:
        fo.writelines(flowstrs)

    subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', swid, '/tmp/flow'])


def pushflows(sw2flows):

    for sw in sw2flows.keys():
        pushflow(sw, sw2flows[sw])

def createAndAddFirstSwitchFlows(switchlist,dstmac):
    flowstrs = []
    srcswitch = NetworkSwitch.query.filter_by(swid = switchlist[0]).first()
    dstswitch = NetworkSwitch.query.filter_by(swid = switchlist[1]).first()
    extport = srcswitch.links.filter_by(dstswitch_id = dstswitch.id).first().srcswitch_port
    print 'Switch port {}'.format(extport)
    '''

    swflow = 'table=1, priority=100,dl_vlan=10, dl_dst={}, actions=output:{}'.format(dstmac,extport)
    flowstrs.append(swflow)
    swflow = 'table=0, priority=99, in_port={}, actions=resubmit(,1)'.format(extport)
    flowstrs.append(swflow)
    swflow = 'table=1, priority=100, dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=output:{}'.format(extport)
    flowstrs.append(swflow)
    pushflow(switchlist[0],flowstrs)
    '''

def addMultiSwitchFlows(switchlist, srcmac, dstmac):
    createAndAddFirstSwitchFlows(switchlist,dstmac)
    
    
'''
#switchlist[0]
print 'First switch configure only external ports {}'.format(switchlist[0])
fo = open("/tmp/flow", "wb")
fo.write("table=1, priority=100,dl_vlan=10, dl_dst=");
fo.write(dstmac);
fo.write(", actions=output:");
#TODO Find port that connects switchlist[i] to switchlist[i+1]
fo.write("4");
fo.write("\n")
fo.write("table=0, priority=99, in_port=");
#TODO Find port that connects switchlist[i] to switchlist[i+1]
fo.write("4");
fo.write(", actions=resubmit(,1)");
fo.write("\n")

fo.write("table=1, priority=100, dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=output:");
#TODO Find port that connects switchlist[0] to switchlist[1]
fo.write("4");
fo.write("\n")

fo.close()
subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', switchlist[0], '/tmp/flow'])

#switchlist[last one]
print 'Last switch configure only external ports {}'.format(switchlist[len(switchlist)-1])
fo = open("/tmp/flow", "wb")
fo.write("table=1, priority=100,dl_vlan=10, dl_dst=");
#srcmac is the dst mac for the last switch
fo.write(srcmac);
fo.write(", actions=output:");
#TODO Find port that connects switchlist[i] to switchlist[i+1]
fo.write("4");
fo.write("\n")
fo.write("table=0, priority=99, in_port=");
#TODO Find port that connects switchlist[i] to switchlist[i+1]
fo.write("4");
fo.write(", actions=resubmit(,1)");

fo.write("\n")
fo.write("table=1, priority=100, dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=output:");
#TODO Find port that connects switchlist[last] to switchlist[last - 1]
fo.write("4");
fo.write("\n")
fo.close()

subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', switchlist[len(switchlist)-1], '/tmp/flow'])

for i in range(1,len(switchlist) - 1):
    print 'Configuring intermediate switch {}'.format(switchlist[i])
    fo = open("/tmp/flow", "wb")
    fo.write("table=0, priority=99,in_port=");
    #TODO get port connected to switchlist[i-1] 
    fo.write("1");
    fo.write(", actions=resubmit(,1)");
    #TODO Find port that connects switchlist[i] to switchlist[i+1]
    fo.write("\n")
    fo.write("table=1, priority=100, dl_vlan=10, dl_dst=");
    fo.write(dstmac);
    fo.write(", actions=output:");
    #TODO Find port that connects switchlist[i] to switchlist[i+1]
    fo.write("3");
    fo.write("\n")
    
    fo.write("table=0, priority=99,in_port=");
    #TODO get port connected to switchlist[i+1]
    fo.write("3");
    fo.write(", actions=resubmit(,1)");
    #TODO Find port that connects switchlist[i] to switchlist[i+1]
    fo.write("\n")
    fo.write("table=1, priority=100, dl_vlan=10, dl_dst=");
    fo.write(srcmac);
    fo.write(", actions=output:");
    #TODO Find port that connects switchlist[i] to switchlist[i-1]
    fo.write("1");
    fo.write("\n")

    fo.write("table=1, priority=100, dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=output:");
    #TODO Find port that connects switchlist[i] to switchlist[i-1] and switchlist[i+1]
    fo.write("1");
    fo.write(",");
    fo.write("3");
    fo.write("\n")

    fo.close()
    subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', switchlist[i], '/tmp/flow'])
'''
