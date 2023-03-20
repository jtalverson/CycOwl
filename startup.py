import PySimpleGUI as sg
import os
import subprocess
import tkinter as tk
import requests
# function to establish a new connection
def createNewConnection(name, SSID, password):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+password+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
    with open(name+".xml", 'w') as file:
        file.write(config)
    os.system(command)


# function to connect to a network   
def connect(name, SSID):
    command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    os.system(command)

# function to display avavilabe Wifi networks   
def displayAvailableNetworks():
    command = "netsh wlan show networks interface=Wi-Fi"
    os.system(command)

def connecting():
# input wifi name and password
    name = clicked.get()
    password = inputtxt.get(1.0, "end-1c")
    createNewConnection(name, name, password)
    connect(name, name)
    timeout = 1 
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        l = tk.Label(root, text = "Current WiFi Connection: " + clicked.get())
        l.pack()
    except requests.ConnectionError:
        t = tk.Label(root, text = "Failed to Connect")
        t.pack()

def holder():
    print("hello")


# using the check_output() for having the network term retrieval
results = subprocess.check_output(["netsh", "wlan", "show", "network"])
results = results.decode("ascii") # needed in python 3
results = results.replace("\r","")
ls = results.split("\n")
ls = ls[4:]
ssids = []
x = 0
while x < len(ls):
    if x % 5 == 0:
        ssids.append(ls[x])
    x += 1
ssids = [ssid.split(':',1)[-1].strip() for ssid in ssids]
ssidsall = []
x = 0
while x < len(ssids):
    if ssids[x] != "":
        ssidsall.append(ssids[x])
    x+=1

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

button = tk.Button( root , text = "Connect" , command = connecting).pack()

zoom = tk.Button( root , text = "Start Zoom" , command = holder).pack()
ride = tk.Button( root , text = "Start Ride" , command = holder).pack()

# Execute tkinter
root.mainloop()

