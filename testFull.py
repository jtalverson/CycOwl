import os
import tkinter as tk
import pexpect
import sys
import time
import wifi
class App():
    def __init__(self):
        self.bdevices = []
        self.bmacs = []
        self.bprev = ""
        self.selectedB = ""
        self.wdevices = []
        self.wpass = ""
        self.wcurrent = ""
        self.selectedW = ""
        
        startupWifi(self)
        scan(self)
        # print(self.bdevices)
        # self.tmp = int(input("HERE: "))
        # connect(self)
        # disconnect(self)
        # scan(self)
        # print(self.bdevices)
        # self.tmp = int(input("HERE: "))
        # connect(self)
        # disconnect(self)

        getWifis(self)
        print(self.wcurrent)
		
		





def connect(self):
    index = self.tmp      #self.bdevices.index(self.selectedB)
    name = self.bdevices[index]
    address = self.bmacs[index]

    response = ''
    p = pexpect.spawn('bluetoothctl',encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect('#')
    if(self.bprev != ""):
        p.sendline("disconnect " + self.bprev)
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
    self.bprev = address
    p.sendline("quit")
    p.close()

def disconnect(self):
    response = ''
    p = pexpect.spawn('bluetoothctl',encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect('#')
    if(self.bprev != ""):
        p.sendline("disconnect " + self.bprev)
        p.expect("#")
        self.bprev = ""
    else:
        print("No Bluetooth Devices are connected")
    p.sendline("quit")
    p.close()
		
def scan(self):
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
    self.bdevices = devices
    self.bmacs = connections

def scanWifi(self):
    command = '/bin/bash -c "sudo iw wlan0 scan | grep -Po \'(signal|SSID):\K.*\' | sed \'s/ $/ [unknown SSID]/\' | paste -d  - - | cut -c2- | sort -gr"'
    #'nmcli device wifi list'
    p = pexpect.spawn(command, encoding = 'utf-8')
    p.logfile_read = sys.stdout
    p.expect(pexpect.EOF, timeout=None)		
    out = p.before
    outList = out.split("\n")
    listStart =int (len(outList)/2)
    flist = []
    for x in range(listStart):
        temp = outList[x+listStart].replace('\r','')
        temp = temp.replace('\t','')
        flist.append(temp)
    self.wdevices = flist

def connectWifi(self):
    prev = self.wcurrent
    if(self.wcurrent != ""):
        command = 'nmcli d wifi disconnect ' + prev[0]
        pexpect.run(command)
    password = self.wpass
    command = 'nmcli -a d wifi connect ' + self.selectedW
    p = pexpect.spawn(command, encoding = 'utf-8')
    p.logfile_read = sys.stdout
    p.expect("Password: ")
    p.sendline(password)

def disconnectWifi(self):
    prev = self.wcurrent
    command = 'nmcli d wifi disconnect ' + self.wcurrent
    pexpect.run(command)

def getWifis(self):
    termOut = pexpect.run('iwgetid -r')
    output = (termOut.decode('utf-8')).split("\r")
    self.wcurrent = output[0]

def startupWifi(self):
    pexpect.run('nmcli radio wifi off')
    time.sleep(3)
    pexpect.run('nmcli radio wifi on')
    time.sleep(8)

tmp = App()