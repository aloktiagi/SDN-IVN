#!/usr/bin/python
switchlist = []
switchlist.append("s2")
switchlist.append("s1")
switchlist.append("s3")
switchlist.append("s4")
srcmac = "00:00:00:00:00:01"
dstmac = "00:00:00:00:00:07"

#switchlist[0]
print "First switch configure only external ports"
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
fo.close()
#subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', self.server, '/tmp/flow'])

#switchlist[last one]
print "Last switch configure only external ports"
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
fo.close()
#subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', self.server, '/tmp/flow'])

for i in range(1,len(switchlist) - 1):
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
    #subprocess.call(['sudo', 'ovs-ofctl', 'add-flows', self.server, '/tmp/flow'])

    print switchlist[i]


