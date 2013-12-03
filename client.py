#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc
import subprocess
import commands

http_client = pyjsonrpc.HttpClient(
    url = "http://localhost:8080/jsonrpc",
    username = "Username",
    password = "Password"
)

macIPPair = http_client.call("add", "aloktiagi", "password")
ip = ''
ip += macIPPair[1]
ip += '/8'
print ip 
dev = commands.getstatusoutput('ip r | cut -f 3 -d " "')
ipToDel = commands.getstatusoutput('ip r | cut -f 12 -d " "')

subprocess.call(["ifconfig", dev[1], "hw", "ether", macIPPair[0]])
subprocess.call(["ip", "a", "d", ipToDel[1] , "dev", dev[1]])
subprocess.call(["ip", "a", "a", ip , "dev", dev[1]])
