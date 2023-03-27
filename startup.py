import os
import subprocess
import tkinter as tk
import requests
from time import sleep
from threading import Thread
import continuous_threading
import wifimangement_linux as wifi 
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
#rom selenium.webdriver.support.ui import WebDriverWait
#rom selenium.webdriver.support import expected_conditions as EC

def start_zoom():
    exec(open("/home/jdlinux/Downloads/CycOwl-main/join_zoom.py").read())

def start_ride():
    exec(open("/home/jdlinux/Downloads/CycOwl-main/Detector/video.py").read())

def holder():
    print("hello")

def connector():
    wifi.connect(clicked.get(),inputtxt.get(1.0, "end-1c"))

def ssid(ssidsall):
    wifi.off()
    wifi.on()
    ssidsall = wifi.list()


wifi.off()
wifi.on()
ssidsall = []

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

