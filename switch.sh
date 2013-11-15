#sudo ovs-ofctl add-flows s1 - <<'EOF'
#table=0, priority=99, in_port=1, vlan_tci=0, dl_src=00:00:00:00:00:01, actions=mod_vlan_vid:10,resubmit(,1)
#EOF

#sudo ovs-ofctl add-flows s1 - <<'EOF'
#table=0, priority=99, in_port=2, vlan_tci=0, dl_src=00:00:00:00:00:02, actions=mod_vlan_vid:10,resubmit(,1)
#EOF

#sudo ovs-ofctl add-flows s1 - <<'EOF'
#table=1, priority=100,dl_vlan=10, dl_dst=00:00:00:00:00:01, actions=strip_vlan,output:1
#EOF

#sudo ovs-ofctl add-flows s1 - <<'EOF'
#table=1, priority=100,dl_vlan=10, dl_dst=00:00:00:00:00:02, actions=strip_vlan,output:2
#EOF

#sudo ovs-ofctl add-flows s1 - <<'EOF'
#table=1, priority=100,dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=strip_vlan,output:1,2
#EOF

########## Three switch test setup ######################


##### s2 -> s1 -> s4
sudo ovs-ofctl add-flows s2 - <<'EOF'
table=0, priority=99, in_port=1, vlan_tci=0, dl_src=f6:d1:5e:ff:1a:eb, actions=mod_vlan_vid:10,resubmit(,1)
EOF

sudo ovs-ofctl add-flows s2 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=de:6b:f2:34:ea:58, actions=output:4
EOF

sudo ovs-ofctl add-flows s1 - <<'EOF'
table=0, priority=99, in_port=1, actions=resubmit(,1)
EOF

sudo ovs-ofctl add-flows s1 - <<'EOF'
table=1, priority=100, dl_vlan=10, dl_dst=de:6b:f2:34:ea:58, actions=output:3
EOF

sudo ovs-ofctl add-flows s4 - <<'EOF'
table=0, priority=99, in_port=4,  actions=resubmit(,1)
EOF

sudo ovs-ofctl add-flows s4 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=de:6b:f2:34:ea:58, actions=strip_vlan,output:1
EOF


######## s4 -> s1 -> s2

sudo ovs-ofctl add-flows s4 - <<'EOF'
table=0, priority=99, in_port=1, vlan_tci=0, dl_src=de:6b:f2:34:ea:58, actions=mod_vlan_vid:10,resubmit(,1)
EOF

sudo ovs-ofctl add-flows s4 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=f6:d1:5e:ff:1a:eb, actions=output:4
EOF

sudo ovs-ofctl add-flows s1 - <<'EOF'
table=0, priority=99, in_port=3, actions=resubmit(,1)
EOF

sudo ovs-ofctl add-flows s1 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=f6:d1:5e:ff:1a:eb, actions=output:1
EOF

sudo ovs-ofctl add-flows s2 - <<'EOF'
table=0, priority=99, in_port=4, actions=resubmit(,1)
EOF

sudo ovs-ofctl add-flows s2 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=f6:d1:5e:ff:1a:eb, actions=strip_vlan,output:1
EOF


################ broadcast rules ###############

sudo ovs-ofctl add-flows s2 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=output:4
EOF

sudo ovs-ofctl add-flows s2 - <<'EOF'
table=1, priority=101,dl_vlan=10, in_port=4, dl_dst=ff:ff:ff:ff:ff:ff, actions=strip_vlan,output:1
EOF

sudo ovs-ofctl add-flows s1 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=output:1,3
EOF

sudo ovs-ofctl add-flows s4 - <<'EOF'
table=1, priority=100,dl_vlan=10, dl_dst=ff:ff:ff:ff:ff:ff, actions=output:4
EOF

sudo ovs-ofctl add-flows s4 - <<'EOF'
table=1, priority=101,dl_vlan=10, in_port=4, dl_dst=ff:ff:ff:ff:ff:ff, actions=strip_vlan,output:1
EOF


