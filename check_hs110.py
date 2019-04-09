#!/usr/bin/env python
#
# This plugin is based on the work of the following projects:
# - https://github.com/softScheck/tplink-smartplug
# - http://www.evilbox.ro/linux/tp-link-hs110-smartplug-linux-monitoring-with-grafana/
#

import sys
import json
import socket
import argparse

# Constants
VERSION = '1.0.0'
PORT = 9999

# Functions
def validIP(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:
		parser.error("Invalid IP Address.")
	return ip 

def encrypt(string):
	key = 171
        result = pack('>I', len(string))
	for i in string: 
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171 
	result = ""
	for i in string: 
		a = key ^ ord(i)
		key = ord(i) 
		result += chr(a)
	return result

# Main programm
parser = argparse.ArgumentParser(description="check_smartplug for TP-Link Wi-Fi Smartplug HS110 v" + str(VERSION))
parser.add_argument("-H", "--host", metavar="<host>", required=True, help="Host IP Address", type=validIP)
args = parser.parse_args()

cmd = {'power' : '{"emeter":{"get_realtime":{}}}'}

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((args.host, PORT))
	sock.send(encrypt(cmd['power']))
	result = sock.recv(2048)
	sock.close()

	jsonstr = decrypt(result[4:])
	data = json.loads(jsonstr)
	data = data["emeter"]["get_realtime"]
        if "power_mw" in data:
                perf = "| power=" + str(data["power_mw"]) + " current=" + str(data["current_ma"]) + " voltage=" + str(data["voltage_mv"])
                print "OK - " + str(data["power_mw"]) + " watt's are in use." + perf
        else:
                perf = "| power=" + str(data["power"]) + " current=" + str(data["current"]) + " voltage=" + str(data["voltage"])
                print "OK - " + str(data["power"]) + " watt's are in use." + perf
	sys.exit(0)
except socket.error:
	print "CRITICAL - Cound not connect to host " + args.host + ":" + str(PORT)
	sys.exit(2)
