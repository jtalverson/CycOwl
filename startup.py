import os
import subprocess
import tkinter as tk
import requests
from time import sleep
from threading import Thread
import continuous_threading
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
#rom selenium.webdriver.support.ui import WebDriverWait
#rom selenium.webdriver.support import expected_conditions as EC

def commandExists(self, cmd):
        return cmd in self._commands and hasattr(self, '_%s' % cmd) and callable(getattr(self, '_%s' % cmd))

def start_zoom():
    exec(open("/home/jdlinux/Downloads/CycOwl-main/join_zoom.py").read())

def start_ride():
    exec(open("/home/jdlinux/Downloads/CycOwl-main/Detector/video.py").read())

def connector():
    network = clicked.get()
    tpass = inputtxt.get(1.0, "end-1c")
    if tpass == '':
        os.popen("iwconfig " + winame + " essid " + network)
    else:
        connectstatus = os.popen("iwconfig " + winame + " essid " + network + " key s:" + tpass)
    print ("Connecting...")
    #if not commandExists("dhclient"):
        #print ("Looks like there isn't a dhclient program on this computer. Trying dhcpd (Used with Arch)")
        #con2 = os.popen("dhcpcd " + winame).read()
        #print(con2)
        #if not commandExists("dhcpcd"):
            #print ("Well, I'm out of options. Try installing dhcpd or dhclient.")
            #quit()
    # else:    
    os.popen("dhclient " + winame)
    ontest = os.popen("ping -c 1 google.com").read()
    if ontest == '':
        print ("Connection failed. (Bad pass?)")
        quit()
    print ("Connected successfully!")
    timeout = 1
    try:
        requests.head("http://google.com/", timeout=timeout)
        l = tk.label(root,text = "Current WiFi Connection: " + network)
        l.pack()
    except:
        t = tk.Label(root,text = "Failed to Connect, Try Again")
        t.pack()

def holder():
    print("hello")

def ssid(ssidsall):
    print("REACHED")
    user = os.popen("whoami").read()
    if 'root' not in user:
        print('You need to be the root user to run this program and you are running as '+user+'  Try sudo python <ScriptName>.py')
        print ('Exiting...')
        quit()
    status = os.popen("ifconfig wlan0 up").read()
    if not 'No such device' in status:
        winame = "wlan0"
    stream = os.popen("iwlist " + winame + " scan")
    networksfound = 0
    for line in stream:
        if "ESSID" in line:
            networksfound += 1
            ssidsall.append(line.split('ESSID:"', 1)[1].split('"', 1)[0])
    if networksfound == 0:
        print ("Looks like we didn't find any networks in your area. Exiting...")
        ssidsall = ["NO SSIDS AVAILIBLE"]
    #quit()
    print("ESCAPED")
winame = ""
ssidsall = []
#t1 = continuous_threading.ContinuousThread(target=ssid(ssidsall), args=[])
#t1.start()


# Create object
root = tk.Tk()
# Adjust size
root.geometry( "800x480" )

# datatype of menu text
clicked = tk.StringVar()
relist = tk.Button( root , text = "Refresh List" , command = ssid(ssidsall)).pack()
drop = tk.OptionMenu( root , clicked , *ssidsall )
drop.pack()

#password input
root.title("WIFI Password")
inputtxt = tk.Text(root,height = 2,width = 10)
inputtxt.pack()

button = tk.Button( root , text = "Connect To Wifi" , command = connector).pack()
zoom = tk.Button( root , text = "Start Zoom" , command = holder).pack() #exec(open("join_zoom.py").read())
ride = tk.Button( root , text = "Start Ride" , command = holder).pack()

# Execute tkinter
root.mainloop()

