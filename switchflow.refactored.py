#!/usr/bin/python
import subprocess

switchlist = []
switchlist.append("s2")
switchlist.append("s1")
switchlist.append("s4")
srcmac = "4e:ce:8c:e1:29:aa"
dstmac = "fa:91:d5:03:4e:9c"

def pushflow(swid, flowstrs):

    with open("/tmp/flow", "wb") as fo:
        fo.writelines(flowstrs)

    subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', swid, '/tmp/flow'])


def pushflows(sw2flows):

    for sw in sw2flows.keys():
        pushflow(sw, sw2flows[sw])

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
'''

def firstswitch():
    flowstrs = []

    fs = "table=1, priority=100, dl_vlan=10, " \
       + ("dl_dst=%s, actions=output:%d" % (dstmac, 4)
    flowstrs.append(fs)

    fs = "table=0, priority=99"

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
