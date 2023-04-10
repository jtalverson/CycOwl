import tkinter
import tkinter.messagebox
import customtkinter
import kivy  
from kivy.app import App
from kivy.uix.vkeyboard import VKeyboard

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        #self.geometry(f"{800}x{480}")
        #self.geometry(f"{1024}x{720}")
        self.attributes('-fullscreen', True)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7 , 8), weight=1)

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

        self.up_connect = customtkinter.CTkButton(master=self.sidebar_frame, text = "Update Connections" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.up_connect.grid(row=6, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.destroy)
        self.exit_button.grid(row = 7, column = 0, padx = 20, pady = (20 , 10))

        #Wifi Frame
        self.wifi_frame = customtkinter.CTkFrame(self,width = 100,corner_radius = 0)
        self.wifi_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.wifi_frame.grid_rowconfigure(8, weight=1)
        self.wifi_label = customtkinter.CTkLabel(self.wifi_frame, text="Wi-Fi", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wifi_label.grid(row=0, column=1, padx=20, pady=(20, 10))

        self.wifiList = customtkinter.CTkLabel(self.wifi_frame, text="Access Points Availible:", anchor="w")
        self.wifiList.grid(row=2, column=1, padx=20, pady=(10, 0))
        self.wifi_optionemenu = customtkinter.CTkOptionMenu(self.wifi_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.wifi_optionemenu.grid(row=3, column=1, padx=20, pady=(10, 10))
        self.passentry = customtkinter.CTkEntry(self.wifi_frame, placeholder_text="Enter WiFi Password Here", command = key)
        self.passentry.grid(row=5, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.wifi_connect = customtkinter.CTkButton(master=self.wifi_frame, text = "Connect Wi-Fi" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.wifi_connect.grid(row=6, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #Bluetooth Frame
        self.blue_frame = customtkinter.CTkFrame(self,width = 100,corner_radius = 0)
        self.blue_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.blue_frame.grid_rowconfigure(8, weight=1)
        self.blue_label = customtkinter.CTkLabel(self.blue_frame, text="Bluetooth", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.blue_label.grid(row=0, column=2, padx=20, pady=(20, 10))

        self.blueList = customtkinter.CTkLabel(self.blue_frame, text="Devices Avalible:", anchor="w")
        self.blueList.grid(row=2, column=2, padx=20, pady=(10, 0))
        self.blue_optionemenu = customtkinter.CTkOptionMenu(self.blue_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.blue_optionemenu.grid(row=3, column=2, padx=20, pady=(10, 10))

        self.blue_connect = customtkinter.CTkButton(master=self.blue_frame, text = "Connect Bluetooth" ,fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
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

def key(VKeyboard):
    player = VKeyboard()

if __name__ == "__main__":
    app = App()
    app.mainloop()