import tkinter
import tkinter.messagebox
import customtkinter
import os
import pexpect
import sys
import time
import wifi


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_widget_scaling(1.2)
        customtkinter.set_appearance_mode("Dark")

        self.bdevices = []
        self.bmacs = []
        self.bprev = ""
        self.selectedB = ""
        self.wdevices = []
        self.wpass = ""
        self.wcurrent = ""
        self.selectedW = ""

        # configure window
        self.title("CustomTkinter complex_example.py")
        #self.geometry(f"{800}x{480}")
        #self.attributes('-topmost', True)
        self.attributes('-fullscreen', True)
	    #self.attributes('-topmost', True)

        startupWifi(self)
        scan(self)
        scanWifi(self)
        getWifis(self)

        self.var = customtkinter.StringVar(self)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Settings", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=4, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20))

        self.up_connect = customtkinter.CTkButton(master=self.sidebar_frame, text = "Update Connections" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command = lambda: callUpdate(self))
        self.up_connect.grid(row=6, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.destroy)
        self.exit_button.grid(row = 7, column = 0, padx = 20, pady = (20 , 10))

        self.key_button = customtkinter.CTkButton(self.sidebar_frame, text="Keyboard", command = lambda: callKey(self))
        self.key_button.grid(row = 8, column = 0, padx = 20, pady = (20 , 10))


        #Wifi Frame
        self.wifi_frame = customtkinter.CTkFrame(self,width = 100,corner_radius = 0)
        self.wifi_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.wifi_frame.grid_rowconfigure(8, weight=1)
        self.wifi_label = customtkinter.CTkLabel(self.wifi_frame, text="Wi-Fi", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wifi_label.grid(row=0, column=1, padx=20, pady=(20, 10))

        self.wifiList = customtkinter.CTkLabel(self.wifi_frame, text="Access Points Availible:", anchor="w")
        self.wifiList.grid(row=2, column=1, padx=20, pady=(10, 0))
        self.wifi_optionmenu = customtkinter.CTkOptionMenu(self.wifi_frame, values = self.wdevices)
        self.wifi_optionmenu.grid(row=3, column=1, padx=20, pady=(10, 10))
        self.passentry = customtkinter.CTkEntry(self.wifi_frame, placeholder_text="Enter WiFi Password Here")
        self.passentry.grid(row=5, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.wifi_connect = customtkinter.CTkButton(master=self.wifi_frame, text = "Connect Wi-Fi" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command =lambda: callConnectWifi(self))
        self.wifi_connect.grid(row=6, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #Bluetooth Frame
        self.blue_frame = customtkinter.CTkFrame(self,width = 100,corner_radius = 0)
        self.blue_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.blue_frame.grid_rowconfigure(8, weight=1)
        self.blue_label = customtkinter.CTkLabel(self.blue_frame, text="Bluetooth", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.blue_label.grid(row=0, column=2, padx=20, pady=(20, 10))

        self.blueList = customtkinter.CTkLabel(self.blue_frame, text="Devices Avalible:", anchor="w")
        self.blueList.grid(row=2, column=2, padx=20, pady=(10, 0))
        self.blue_optionmenu = customtkinter.CTkOptionMenu(self.blue_frame, values=self.bdevices)
        self.blue_optionmenu.grid(row=3, column=2, padx=20, pady=(10, 10))

        self.blue_connect = customtkinter.CTkButton(master=self.blue_frame, text = "Connect Bluetooth" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command = lambda: callConnectBluetooth(self))
        self.blue_connect.grid(row=5, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #start zoom and ride
        self.final = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.final.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.final.grid_rowconfigure(8, weight=1)
        self.final_label = customtkinter.CTkLabel(self.final, text="Zoom and Ride", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.final_label.grid(row=0, column=3, padx=20, pady=(20, 10))
        
        self.zoom_label = customtkinter.CTkLabel(self.final, text="Connect to Zoom:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.zoom_label.grid(row=1, column=3, padx=20, pady=(20, 10))
        self.zoom = customtkinter.CTkButton(master=self.final, text = "Connect to Zoom" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.zoom.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.ride_label = customtkinter.CTkLabel(self.final, text="Begin Ride:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ride_label.grid(row=3, column=3, padx=20, pady=(20, 10))
        self.ride = customtkinter.CTkButton(master=self.final, text = "Start Ride" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.ride.grid(row=4, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def Close(self):
        self.destroy()

def connect(self):
    index = self.bdevices.index(self.selectedB)
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
    if(self.bdevices == []):
        self.bdevices = ["NONE"]
        self.bconnections = ["NONE"]

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
    if(self.wdevices == []):
    	self.wdevices = ["NONE"]

def connectWifi(self):
    prev = self.wcurrent
    if(self.wcurrent != ""):
        command = 'nmcli d wifi disconnect ' + prev[0]
        pexpect.run(command)
    password = self.wpass
    command = 'nmcli -a d wifi connect ' + self.selectedW
    p = pexpect.spawn(command, encoding = 'utf-8')
    p.logfile_read = sys.stdout
    p.expect("Password:")
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

def callUpdate(self):
    scan(self)
    scanWifi(self)
    self.var.set('')
    for string in self.bdevices:
         self.blue_optionmenu.add_command(label = string, command = customtkinter.setit(self.var,string))
    self.var.set('')
    for string in self.wdevices:
         self.wifi_optionmenu.add_command(label = string, command = customtkinter.setit(self.var,string))

def callConnectBluetooth(self):
    self.selectedB = self.blue_optionmenu.get()
    connect(self)

def callConnectWifi(self):
    self.selectedW = self.wifi_optionmenu.get()
    self.wpass = self.passentry.get()
    connectWifi(self)

def callKey(self):
    command = 'gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled false'
    pexpect.run(command)
    command = 'gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled true'
    pexpect.run(command)

if __name__ == "__main__":
    app = App()
    app.mainloop()
