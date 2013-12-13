#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc
import subprocess
import commands
import flask
import urllib2
import json
import sys, getopt
from flask import Flask, abort, request, jsonify

username = ''
password = ''
mac = ''
vnetid = 0
try:
   opts, args = getopt.getopt(sys.argv[1:],"h:u:p:m:v:")
except getopt.GetoptError:
   print 'Usage: login -u <username> -p <password> -m <MAC address> -v <vnetid>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-h':
      print 'login -u <username> -p <password> -m <MAC address> -v <vnetid>'
      sys.exit()
   elif opt in ("-u"):
      username = arg
   elif opt in ("-p"):
      password = arg
   elif opt in ("-m"):
      mac = arg
   elif opt in ("-v"):
      vnetid = int(arg)

url = 'http://192.168.237.148:5000/api/'
print 'Username {} password {} mac {} vnet {}'.format(username,password,mac,vnetid)
authdata = { "username": username, "password": password, "mac": mac }
authdata = json.dumps(authdata)
request = urllib2.Request(url + 'authenticate', authdata, {'Content-Type': 'application/json'})

f = urllib2.urlopen(request)
response = f.read()
print response
f.close()
json.loads(response)
sessionid = json.loads(response)['session_id']

joindata = { "username": username, "password": password, "mac": mac , "vnetwork_id" : vnetid, "session_id" : sessionid }
joindata = json.dumps(joindata)
request = urllib2.Request(url + 'join', joindata, {'Content-Type': 'application/json'})
f = urllib2.urlopen(request)
response = f.read()
print response
f.close()
json.loads(response)
ipToAdd = ''
macToAdd = ''
ipToAdd = json.loads(response)['ip']
macToAdd = json.loads(response)['mac']
ipToAdd += '/8'
print 'IP to add {}'.format(ipToAdd)
print 'Mac to add {}'.format(macToAdd)

dev = commands.getstatusoutput('ip a | grep eth0 | grep inet | awk \'{print $7}\'')
ipToDel = commands.getstatusoutput('ip a | grep eth0 | grep inet | awk \'{print $2}\'')

subprocess.call(["ifconfig", dev[1], "hw", "ether", macToAdd])
subprocess.call(["ip", "a", "d", ipToDel[1] , "dev", dev[1]])
subprocess.call(["ip", "a", "a", ipToAdd , "dev", dev[1]])
