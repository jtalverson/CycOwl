import os
import tkinter as tk
import pexpect
import sys
import time
import wifi
import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.bdevices = []
        self.bmacs = []
        self.bprev = ""
        self.selectedB = ""
        self.wdevices = []
        self.wpass = ""
        self.wcurrent = ""
        self.selectedW = ""

        #startupWifi(self)
        #scan(self)
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
        scanWifi(self)
        print(self.wdevices)
        
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{800}x{480}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkRadioButton(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
		    
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

if __name__ == "__main__":
    app = App()
    app.mainloop()