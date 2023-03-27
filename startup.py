import os
import subprocess
import tkinter as tk
import requests
from time import sleep
from threading import Thread
import continuous_threading
import scrapy
from threading import Thread
import pandas
import time
import os

# initialize the networks dataframe that will contain all access points nearby
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
# set the index BSSID (MAC address of the AP)
networks.set_index("BSSID", inplace=True)

def callback(packet):
    if packet.haslayer(Dot11Beacon):
        # extract the MAC address of the network
        bssid = packet[Dot11].addr2
        # get the name of it
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extract network stats
        stats = packet[Dot11Beacon].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)


def print_all():
    while True:
        os.system("clear")
        print(networks)
        time.sleep(0.5)


def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        # switch channel from 1 to 14 each 0.5s
        ch = ch % 14 + 1
        time.sleep(0.5)


if __name__ == "__main__":
    # interface name, check using iwconfig
    interface = "wlan0mon"
    # start the thread that prints all the networks
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start the channel changer
    channel_changer = Thread(target=change_channel)
    channel_changer.daemon = True
    channel_changer.start()
    # start sniffing
    sniff(prn=callback, iface=interface)

""" def start_zoom():
    exec(open("/home/jdlinux/Downloads/CycOwl-main/join_zoom.py").read())

def start_ride():
    exec(open("/home/jdlinux/Downloads/CycOwl-main/Detector/video.py").read())

def holder():
    print("hello")
 """
""" # Create object
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

 """