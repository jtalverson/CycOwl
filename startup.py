import os
import subprocess
import tkinter as tk
import requests
from time import sleep
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
#rom selenium.webdriver.support.ui import WebDriverWait
#rom selenium.webdriver.support import expected_conditions as EC

def start_ride():
    
    exec(open("/home/jdlinux/Downloads/CycOwl-main/Detector/video.py").read())

def connector():
    Wname = clicked.get()
    password = inputtxt.get(1.0, "end-1c")
    createNewConnection(Wname,Wname,password)
    Connect(Wname,Wname)
    timeout = 1
    try:
        requests.head("http://google.com/", timeout=timout)
        l = tk.label(root,text = "Current WiFi Connection: " + name)
        l.pack()
    except:
        t = tk.Label(root,text = "Failed to Connect, Try Again")
        t.pack()

def holder():
    print("hello")

print ("Checking for root access...")
user = os.popen("whoami").read()
if 'root' not in user:
    print('You need to be the root user to run this program and you are running as '+user+'  Try sudo python <ScriptName>.py')
    print ('Exiting...')
    quit()
else:
    print('Good job, you\'re root.')

print ("Trying to activate the default wlan0 network...")
status = os.popen("ifconfig wlan0 up").read()
if 'No such device' in status:
    print ("It seems your wireless device is not named wlan0, so you're going to need to enter it manually.")
    winame = raw_input('Wireless Device Name: ')
else:
    winame = "wlan0"
print ("Wireless device enabled!")
print ("Checking for available wireless networks...")
stream = os.popen("iwlist " + winame + " scan")
print ("Available Networks:")
networksfound = 0
for line in stream:
    if "ESSID" in line:
        networksfound += 1
        ssidsall.append(line.split('ESSID:"', 1)[1].split('"', 1)[0])
if networksfound == 0:
    print ("Looks like we didn't find any networks in your area. Exiting...")
    ssidsall = ["Hello", "world"]
    #quit()

# Create object
root = tk.Tk()
# Adjust size
root.geometry( "800x480" )

# datatype of menu text
clicked = tk.StringVar()
drop = tk.OptionMenu( root , clicked , *ssidsall )
drop.pack()

#password input
root.title("WIFI Password")
inputtxt = tk.Text(root,height = 2,width = 10)
inputtxt.pack()

button = tk.Button( root , text = "Connect To Wifi" , command = connector).pack()

zoom = tk.Button( root , text = "Start Zoom" , command = holder()).pack() #exec(open("join_zoom.py").read())
ride = tk.Button( root , text = "Start Ride" , command = ).pack()

# Execute tkinter
root.mainloop()

