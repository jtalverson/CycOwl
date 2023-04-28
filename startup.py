import tkinter
import tkinter.messagebox
import customtkinter
import os
import pexpect
import sys
import time
import wifi
import subprocess
import getpass
import argparse
import shelve
import pygame
from pynput.keyboard import Key, Controller

fullscreen = True
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fullscreen", help="disables fullscreen on launch when included", action="store_true")
args = parser.parse_args()
if args.fullscreen:
    fullscreen = False

delay_ms = 750
default_width = 120
long_path = "/home/" + getpass.getuser() + "/CycOwl/"

shelf_path = long_path + "shelf/shelf"

print(shelf_path)
shelf = shelve.open(shelf_path)
shelf["processing"] = False
shelf["talking"] = False
shelf["stop"] = False
shelf["loaded"] = False
shelf["vision_down"] = True
shelf["share_ready"] = False
shelf["zoom_down"] = True
shelf["minimized"] = False
shelf["share_started"] = False
shelf["status"] = ""
shelf["zoom_error"] = False
shelf.close()
print("Database initialized")

if fullscreen:
    subprocess.Popen(['python', 'CycOwl/loadingScreen.py'])
else:
    subprocess.Popen(['python', 'CycOwl/loadingScreen.py', '-f'])

base_status = "Ready!"
status = "Status: "

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

secret_password = ""

default_sink = "alsa_output.usb-Solid_State_System_Co._Ltd._USB_PnP_Audio_Device_000000000000-00.analog-stereo"
os.system("pacmd set-default-sink " + default_sink)
pygame.mixer.init()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # customtkinter.set_widget_scaling(1.2)
        customtkinter.set_appearance_mode("Dark")

        self.bdevices = []
        self.bmacs = []
        self.bprev = ""
        self.bprevSSID = ""
        self.selectedB = ""
        self.wdevices = []
        self.wpass = ""
        self.wcurrent = ""
        self.selectedW = ""

        # configure window
        self.title("Startup.py")
        self.attributes('-fullscreen', fullscreen)
        self.attributes('-topmost', True)

        #startupWifi(self)
        scan(self)
        scanWifi(self)
        getWifis(self)

        self.var = customtkinter.StringVar(self)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        #self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=9, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Settings",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, width=default_width,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")

        #self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        #self.scaling_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        #self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, width=default_width,
        #                                                       values=["100%", "110%", "120%", "130%", "140%"],
        #                                                       command=self.change_scaling_event)
        #self.scaling_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20))
        #self.scaling_optionemenu.set("100%")

        self.up_connect = customtkinter.CTkButton(master=self.sidebar_frame, text="Update Connections", border_width=2, width=default_width,
                                                  command=lambda: callUpdate(self))
        self.up_connect.grid(row=4, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")

        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", border_width=2, width=default_width,
                                                   command=lambda: callClose(self))
        self.exit_button.grid(row=8, column=0, padx=20, pady=(20, 10))

        # Wifi Frame
        self.wifi_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.wifi_frame.grid(row=0, column=1, rowspan=7, sticky="nsew")
        # self.wifi_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.wifi_label = customtkinter.CTkLabel(self.wifi_frame, text="Wi-Fi",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wifi_label.grid(row=0, column=1, padx=20, pady=(20, 10))

        self.wifiList = customtkinter.CTkLabel(self.wifi_frame, text="Access Points Availible:", anchor="w")
        self.wifiList.grid(row=1, column=1, padx=20, pady=(10, 0))
        
        if self.wcurrent != "":
            name = self.wcurrent
            self.wdevices.remove(name)
        else:
            name = "None"

        self.wifi_optionmenu = customtkinter.CTkOptionMenu(self.wifi_frame, values=self.wdevices, width=160, command=lambda eff: playClick())
        self.wifi_optionmenu.grid(row=2, column=1, padx=20, pady=(10, 10))
        self.wifi_optionmenu.set("Select Wi-Fi Option")

        self.passentry = customtkinter.CTkEntry(self.wifi_frame, placeholder_text="Enter WiFi Password Here", width=180)
        self.passentry.grid(row=3, column=1, pady=(10, 10))

        self.wifi_connect = customtkinter.CTkButton(master=self.wifi_frame, text="Connect Wi-Fi", border_width=2, width=default_width, command=lambda: callConnectWifi(self))
        self.wifi_connect.grid(row=4, column=1, padx=(20, 20), pady=(10, 10))

        self.wific_label = customtkinter.CTkLabel(self.wifi_frame, text="Connected Wifi: ",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))  
        
        self.wific_name = customtkinter.CTkLabel(self.wifi_frame, text=name, font=customtkinter.CTkFont(size=20))  
        self.wific_label.grid(row=5, column=1, padx=20, pady=(20, 0))
        self.wific_name.grid(row=6, column=1, padx=20)

        self.status_message = customtkinter.CTkLabel(self, text="Status: Ready!", font=customtkinter.CTkFont(size=20))
        self.status_message.grid(row=7, column=1, columnspan=2, padx=(20,20), pady=(10,10))

        # Bluetooth Frame
        self.blue_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.blue_frame.grid(row=0, column=2, rowspan=7, sticky="nsew")
        # self.blue_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.blue_label = customtkinter.CTkLabel(self.blue_frame, text="Bluetooth",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.blue_label.grid(row=0, column=2, padx=20, pady=(20, 10))

        self.blueList = customtkinter.CTkLabel(self.blue_frame, text="Devices Avalible:", anchor="w")
        self.blueList.grid(row=1, column=2, padx=20, pady=(10, 0))
        self.blue_optionmenu = customtkinter.CTkOptionMenu(self.blue_frame, values=self.bdevices, command=lambda eff: playClick())
        self.blue_optionmenu.grid(row=2, column=2, padx=20, pady=(10, 10))
        self.blue_optionmenu.set("Select Bluetooth Device")

        self.blue_connect = customtkinter.CTkButton(master=self.blue_frame, text="Connect Bluetooth", border_width=2, width=default_width,
                                                    command=lambda: callConnectBluetooth(self))
        self.blue_connect.grid(row=3, column=2, padx=(20, 20), pady=(10, 10))
        self.blue_disconnect = customtkinter.CTkButton(master=self.blue_frame, text="Disconnect Bluetooth", width=default_width,
                                                       border_width=2, command=lambda: disconnect(self, False))
        self.blue_disconnect.grid(row=4, column=2, padx=(20, 20), pady=(10, 10))

        self.bluec_label = customtkinter.CTkLabel(self.blue_frame, text="Bluetooth Device:",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bluec_label.grid(row=5, column=2, padx=20, pady=(20, 0))
        self.bluec_device = customtkinter.CTkLabel(self.blue_frame, text="None",
                                                  font=customtkinter.CTkFont(size=20))
        self.bluec_device.grid(row=6, column=2, padx=20, pady=(0, 10))

        # start zoom and ride
        self.final = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.final.grid(row=0, column=3, rowspan=9, sticky="nsew")
        self.final.grid_rowconfigure(8, weight=1)
        # self.final.grid_rowconfigure((0,1,2,3,4,5), weight=1)
        self.final_label = customtkinter.CTkLabel(self.final, text="Zoom and Ride",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.final_label.grid(row=0, column=3, padx=20, pady=(20, 10))

        self.zoom_label = customtkinter.CTkLabel(self.final, text="Connect to Zoom:",
                                                 font=customtkinter.CTkFont(size=15, weight="bold"))
        self.zoom_label.grid(row=1, column=3, padx=20, pady=(10, 0))
        self.zoom = customtkinter.CTkButton(master=self.final, text="Connect to Zoom", border_width=2,
                                            command=lambda: join_zoom(self))
        self.zoom.grid(row=2, column=3, padx=(20, 20), pady=(10, 10))
        self.finalc_label = customtkinter.CTkLabel(self.final, text="Zoom is off",
                                                   font=customtkinter.CTkFont(size=15, weight="bold"))
        self.finalc_label.grid(row=3, column=3, padx=20, pady=(10, 10))

        #self.ride_label = customtkinter.CTkLabel(self.final, text="Begin Ride:",
        #                                         font=customtkinter.CTkFont(size=15, weight="bold"))
        #self.ride_label.grid(row=7, column=3, padx=20, pady=(10, 0))
        self.ride = customtkinter.CTkButton(self.final, text="Start Ride", border_width=2,
                                            command=lambda: start_ride(self))
        self.ride.grid(row=8, column=3, padx=20, pady=(20, 10))

        self.update()
        self.update_idletasks()

        if self.attributes("-fullscreen") != fullscreen:
            self.attributes('-fullscreen', fullscreen)

        shelf = shelve.open(shelf_path) 
        shelf["loaded"] = True
        shelf.close()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        playClick()
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


def connect(self):
    index = self.bdevices.index(self.selectedB)
    name = self.bdevices[index]
    address = self.bmacs[index]

    response = ''
    p = pexpect.spawn('bluetoothctl', encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect('#')
    setStatus("Disconnecting current device")
    if self.bprev != "":
        p.sendline("disconnect " + self.bprev)
        p.expect("#")
    p.sendline("remove " + address)
    setStatus("Connecting to selected device")
    p.sendline("scan on")
    p.expect("#")
    mylist = ["Discovery started", "Failed to start discovery", "Device " + address + " not available",
              "Failed to connect", "Connection successful"]
    fail_count = 0
    while response != "Connection successful" and fail_count < 20:
        p.expect(mylist)
        response = p.after
        p.sendline("connect " + address)
        #if response == "Failed to connect":
            # print('Connection failure ' + str(fail_count))
        fail_count += 1
        time.sleep(1)
    p.sendline("quit")
    p.close()
    if fail_count >= 30:
        setStatus("Failed to connect to device")
    else:
        self.bprev = address
        self.bprevSSID = name
        setStatus("Bluetooth device connected")


def disconnect(self, quiet):
    if not quiet:
        playClick()
    self.blue_disconnect.focus_set()
    disableAll(self)
    setStatus("Disconnecting device")
    response = ''
    p = pexpect.spawn('bluetoothctl', encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect('#')
    if self.bprev != "":
        p.sendline("disconnect " + self.bprev)
        p.expect("#")
        self.bmacs.append(self.bprev)
        self.bprev = ""
    else:
        print("No Bluetooth Devices are connected")
    p.sendline("quit")
    p.close()
    if self.bprevSSID != "":
        self.bdevices.append(self.bprevSSID)
        self.bprevSSID = ""
    self.bluec_device.configure(text="None")
    self.blue_optionmenu.configure(values=self.bdevices)
    self.blue_optionmenu.set("Select Bluetooth Device")
    if not quiet:
        enableAll(self)
        setStatus(base_status)


def scan(self):
    termOut = pexpect.run('hcitool scan')
    output = (termOut.decode('utf-8')).split("\r")
    output.pop(0)
    finalOut = []
    for x in output:
        x.replace('\n', '')
        finalOut.append(x.split("\t"))
    devices = []
    connections = []
    for x in finalOut:
        for y in x:
            if y != "\n" and y != "n/a":
                if len(y) == 17 and y[2] == ':' and y[5] == ':' and y[8] == ':' and y[11] == ':' and y[14] == ':':
                    connections.append(y)
                else:
                    devices.append(y)
        if len(connections) > len(devices):
            connections.pop(len(connections) - 1)
        if len(devices) > len(connections):
            devices.pop(len(devices) - 1)
    self.bdevices = devices
    self.bmacs = connections
    if self.bdevices == []:
        self.bdevices = []
        self.bconnections = []


def scanWifi(self):
    command = '/bin/bash -c "sudo iw wlan0 scan | grep -Po \'(signal|SSID):\K.*\' | sed \'s/ $/ [unknown SSID]/\' | paste -d  - - | cut -c2- | sort -gr"'
    # 'nmcli device wifi list'
    p = pexpect.spawn(command, encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect(pexpect.EOF, timeout=None)
    out = p.before
    outList = out.split("\n")
    listStart = int(len(outList) / 2)
    flist = []
    for x in range(listStart):
        temp = outList[x + listStart].replace('\r', '')
        temp = temp.replace('\t', '')
        if temp not in flist and temp != "[unknown SSID]" and "x00" not in temp:
            flist.append(temp)
    self.wdevices = flist
    if self.wdevices == []:
        self.wdevices = []
    p.close()


def connectWifi(self):
    prev = self.wcurrent
    if self.wcurrent != "":
        command = 'nmcli d wifi disconnect ' + prev[0]
        pexpect.run(command)
    password = self.wpass
    command = 'nmcli -a d wifi connect \"' + self.selectedW + "\""
    print(command)
    p = pexpect.spawn(command, encoding='utf-8')
    p.logfile_read = sys.stdout
    p.expect("Password: ")
    p.sendline(password)

    try:
        p.expect(pexpect.EOF, timeout=10)
        self.wcurrent = self.selectedW
        setStatus("Wi-Fi sucessfully connected")
    except:
        print("Timeout occurred")
        keyboard = Controller()
        self.withdraw()
        keyboard.tap(Key.esc)
        self.deiconify()
        setStatus("Incorrect password, try again")
    self.wdevices.remove(self.wcurrent)
    p.close()


def disconnectWifi(self):
    print("disconnecting")
    prev = self.wcurrent
    command = 'nmcli d wifi disconnect ' + self.wcurrent
    pexpect.run(command)
    self.wcurrent = ""


def getWifis(self):
    termOut = pexpect.run('iwgetid -r')
    output = (termOut.decode('utf-8')).split("\r")
    self.wcurrent = output[0]


def startupWifi(self):
    pexpect.run('nmcli radio wifi off')
    time.sleep(.5)
    pexpect.run('nmcli radio wifi on')
    time.sleep(2)


def disableAll(self):
    #setStatus("Disabling elements")
    for frame in self.winfo_children():
        for widget in frame.winfo_children():
            try:
                #print(widget.winfo_class())
                widget.configure(state="disabled")
            except:
                pass
    self.update()

def enableAll(self):
    #setStatus("Enabling elements")
    for frame in self.winfo_children():
        for widget in frame.winfo_children():
            try:
                #print(widget.winfo_class())
                widget.configure(state="normal")
            except:
                pass
    self.update()

def callUpdate(self):
    playClick()
    self.up_connect.focus_set()
    disableAll(self)

    setStatus("Scanning for Bluetooth devices")
    scan(self)
    setStatus("Scanning for Wi-Fi devices")
    scanWifi(self)
    getWifis(self)
    if self.wcurrent != "":
        name = self.wcurrent
        self.wdevices.remove(name)
    else:
        name = "None"
    self.wific_name.configure(text=name)
    self.blue_optionmenu.configure(values=self.bdevices)
    self.blue_optionmenu.set("Select Bluetooth Device")
    self.wifi_optionmenu.configure(values=self.wdevices)
    self.wifi_optionmenu.set("Select Wi-Fi Option")

    enableAll(self)
    setStatus(base_status)

def callConnectBluetooth(self):
    playClick()
    self.blue_connect.focus_set()
    disableAll(self)
    self.selectedB = self.blue_optionmenu.get()
    if self.selectedB in self.bdevices:
        connect(self)
        if self.bprevSSID != "":
            self.bluec_device.configure(text=self.bprevSSID)
            self.bdevices.remove(self.bprevSSID)
            self.bmacs.remove(self.bprev)
        else:
            self.bluec_device.configure(text="None")
    else:
        setStatus("Invalid Bluetooth device")
    self.blue_optionmenu.configure(values=self.bdevices)
    self.blue_optionmenu.set("Select Bluetooth Device")
    enableAll(self)


def callConnectWifi(self):
    playClick()
    self.wifi_connect.focus_set()
    self.selectedW = self.wifi_optionmenu.get()
    self.wpass = self.passentry.get()
    self.passentry.delete(0, len(self.wpass))
    self.passentry.configure(placeholder_text="Enter WiFi Password Here")
    disableAll(self)
    setStatus("Connecting to Wi-Fi")
    command = 'gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled false'
    pexpect.run(command)
    
    scanWifi(self)

    if self.selectedW in self.wdevices and len(self.wpass) > 0:
        connectWifi(self)
        self.wific_name.configure(text=self.wcurrent)
    else:
        print("Invalid settings")
        setStatus("Invalid Wi-Fi Settings")
        self.wdevices.remove(self.wcurrent)
        #self.after(5000, setStatus(base_status))
    self.wifi_optionmenu.configure(values=self.wdevices)
    self.wifi_optionmenu.set("Select Wi-Fi Option")
    enableAll(self)

def callKey(event, button):
    if button.cget("state") != "disabled":
        playClick()
        setStatus("Opening keyboard")
        command = 'gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled false'
        pexpect.run(command)
        time.sleep(.5)
        command = 'gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled true'
        pexpect.run(command)
        time.sleep(6)
        setStatus(base_status)

def join_zoom(self):
    playClick()
    self.zoom.focus_set()
    #self.zoom.configure(state="disabled")
    disableAll(self)
    shelf = shelve.open(shelf_path)
    vision_down = shelf["vision_down"]
    shelf.close()
    if self.wcurrent != "" and not vision_down:
        setStatus("Launching Zoom room")
        subprocess.Popen(["python3.6", "CycOwl/join_zoom.py"])
        zoom_error = False
        minimize = False
        old_status = ""
        while not minimize and not zoom_error:
            shelf = shelve.open(shelf_path)
            minimize = shelf["share_ready"]
            zoom_error = shelf["zoom_error"]
            status = shelf["status"]
            shelf.close()
            if status != old_status:
                setStatus(status)
                old_status = status
            time.sleep(.05)

        if not zoom_error:
            self.withdraw()
            shelf = shelve.open(shelf_path)
            shelf["minimized"] = True
            shelf.close()

        shared = False
        while not shared and not zoom_error:
            shelf = shelve.open(shelf_path)
            shared = shelf["share_started"]
            zoom_error = shelf["zoom_error"]
            shelf.close()
            time.sleep(.05)

        if not zoom_error:
            self.deiconify()
            setStatus("Zoom room launched")
            self.zstart = "Yes"
            self.finalc_label.configure(text="Zoom Started")
            self.after(500, disable_zoom_button, self)
        else:
            setStatus("Zoom error occurred, try again")
            self.deiconify()
    elif self.wcurrent == "":
        setStatus("No Wi-Fi connected. Launch fail")
    else:
        setStatus("Vision system not running")
    enableAll(self)    


def disable_zoom_button(self):
    shelf = shelve.open(shelf_path)
    error = shelf["zoom_error"]
    shelf.close()
    if not error:
        self.zoom.configure(state="disabled")
        self.after(500, disable_zoom_button, self)
    else:
        self.zoom.configure(state="normal")
        self.zstart = "No"
        self.finalc_label.configure(text="Zoom Disconnected")
        setStatus("Zoom disconnected")
        shelf = shelve.open(shelf_path)
        shelf["zoom_error"] = False
        shelf["share_ready"] = False
        shelf["minimized"] = False
        shelf["share_started"] = False
        shelf["status"] = ""
        talking = shelf["talking"]
        shelf.close()
        while talking:
            shelf = shelve.open(shelf_path)
            talking = shelf["talking"]
            shelf.close()
            time.sleep(.1)
        subprocess.Popen(["python3.6", long_path + "detection/speakWarning.py", "zoom_dropped"])
        callUpdate(self)


def start_ride(self):
    playClick()
    subprocess.Popen(["python", "CycOwl/rideScreen.py"])
    time.sleep(1)
    shelf = shelve.open(shelf_path)
    shelf["processing"] = True
    shelf.close()

def callClose(self):
    playClick()
    self.exit_button.focus_set()
    disableAll(self)
    global secret_password
    secret_password = self.passentry.get()
    shelf = shelve.open(shelf_path)
    shelf["stop"] = True
    vision_stop = shelf["vision_down"]
    zoom_stop = shelf["zoom_down"]
    shelf.close()
    need_to_wait = False
    while not vision_stop:
        shelf = shelve.open(shelf_path)
        vision_stop = shelf["vision_down"]
        shelf.close()
        setStatus("Waiting for machine learning")
        need_to_wait = True
        time.sleep(.75)
    while not zoom_stop:
        shelf = shelve.open(shelf_path)
        zoom_stop = shelf["zoom_down"]
        shelf.close()
        setStatus("Waiting for Zoom to close")
        need_to_wait = True
        time.sleep(.75)
    disconnect(self, True)
    setStatus("Thank you!!")
    if need_to_wait:
        time.sleep(3)
    self.destroy()


def enforceFull():
    if app.attributes("-fullscreen") != fullscreen:
        app.attributes('-fullscreen', fullscreen)
        app.after(delay_ms, enforceFull)


def returnHandler(event):
    callConnectWifi(app)


def setStatus(newStatus):    
    app.status_message.configure(state="normal")
    app.status_message.configure(text=status+newStatus)
    app.update()


def playClick():
    pygame.mixer.music.load(long_path + "click.wav")
    pygame.mixer.music.play(loops=0)


def PlayClick(event, object):
    if object.cget("state") != "disabled":
        playClick()
        object.focus_set()


def minimize():
    app.withdraw()
    time.sleep(3)
    app.deiconify()



if __name__ == "__main__":
    app = App()
    app.passentry.bind("<FocusIn>", lambda eff: callKey(eff, app.passentry))    
    app.passentry.bind("<Return>", returnHandler)
    app.appearance_mode_optionemenu.bind("<Enter>", lambda eff: PlayClick(eff, app.appearance_mode_optionemenu))
    app.wifi_optionmenu.bind("<Enter>", lambda eff: PlayClick(eff, app.wifi_optionmenu))
    app.blue_optionmenu.bind("<Enter>", lambda eff: PlayClick(eff, app.blue_optionmenu))
    app.after(delay_ms, enforceFull)
    app.mainloop()


print("JOB DONE")
print(secret_password)
os.system("rm " + shelf_path[:-5] + "*")
if secret_password != "cap2023":
    command = 'sudo shutdown now'
    print(command)
    pexpect.run(command)
