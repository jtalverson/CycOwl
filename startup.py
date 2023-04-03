import os
import tkinter as tk
import pexpect
import sys
import time

def scan():
	termOut = pexpect.run('hcitool scan')
	output = (termOut.decode('utf-8')).split("\r")
	output.pop(0)
	finalOut = []
	for x in output:
		x.replace('\n','')
		finalOut.append(x.split("\t"))
	devices = []
	connections = []
	for x in finalOut:
		for y in x:
			if y !="\n" and y != "n/a":
				if len(y) == 17 and y[2] == ':' and y[5] == ':' and y[8] == ':' and y[11] == ':' and y[14] == ':':
					connections.append(y)
				else:
					devices.append(y)
		if(len(connections)>len(devices)):
			connections.pop(len(connections)-1)
		if(len(devices)>len(connections)):
			devices.pop(len(devices)-1)
	print(devices)
	return devices,connections
 
def connect(index,devices,connections,prev):
	if(got != ''):
		name = devices[index]
		address = connections[index]
		response = ''
		p = pexpect.spawn('bluetoothctl',encoding='utf-8')
		p.logfile_read = sys.stdout
		p.expect('#')
		if(prev != ""):
			p.sendline("disconnect " + prev)
			p.expect("#")
		p.sendline("remove " +address)
		p.sendline("scan on")
		p.expect("#")
		mylist = ["Discovery started","Failed to start discovery","Device "+address+" not available","Failed to connect","Connection successful"]
		while response != "Connection successful":
			p.expect(mylist)
			response=p.after
			p.sendline("connect "+address)
			time.sleep(1)
		prev = address
		p.sendline("quit")
		p.close()
		#time.sleep(1)
	return prev

def disconnect(prev):
	response = ''
	p = pexpect.spawn('bluetoothctl',encoding='utf-8')
	p.logfile_read = sys.stdout
	p.expect('#')
	if(prev != ""):
		p.sendline("disconnect " + prev)
		p.expect("#")
		prev = ""
	else:
		print("No Bluetooth Devices are connected")
	p.sendline("quit")
	p.close()
	return prev

def getWifi():
	termOut = pexpect.run('iwgetid -r')
	output = (termOut.decode('utf-8')).split("\r")
	return output

def scanWifi():
	response = ""
	p = pexpect.spawn('sudo iw wlan0 scan | grep -Po \'(signal|SSID):\K.*\' | sed \'s/ $/ [unknown SSID]/\' | paste -d \' \' - - | cut -c2- | sort -gr', encoding ='utf-8')
	p.logfile_read = sys.stdout
	p.expect_exact('[sudo] password for capstone: ')
	p.sendline("cap2023")
	#p.expect(pexpect.EOF, timeout=None)
	response = p.after
	print(response)

prev = ""
devices = []
connections = []

"""
devices,connections = scan()
print("here")
got = input()
got = int(got)
connect(got,devices,connections,prev)
disconnect(prev)
"""

prevW = getWifi()
print(prevW)
devicesW = []
connectionsW = []
scanWifi()

