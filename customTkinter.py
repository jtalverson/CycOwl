import tkinter
import tkinter.messagebox
import customtkinter
import pexpect
import getpass
import os

long_path = "/home/" + getpass.getuser() + "/CycOwl/"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_widget_scaling(1.2)
        customtkinter.set_appearance_mode("Dark")
        
        # configure window
        self.title("Ride")
        #self.geometry(f"{800}x{480}")
        #self.attributes('-topmost', True)
        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.val = customtkinter.DoubleVar()
        self.slider = customtkinter.CTkSlider(master = self, from_=100, to=0, variable = self.val, command= lambda v: pexpect.run("amixer -D pulse sset Master " + str(int(self.val.get())) + "%"))
        self.slider.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)
        self.slider.set(50)

        self.exit_button = customtkinter.CTkButton(self, text="Exit", command=lambda: callClose(self))
        self.exit_button.grid(row = 4, column = 4, padx = 20, pady = (20 , 10))

def callClose(self):
	os.system("echo false > \"" + long_path + "detection/process.txt\"")
	self.destroy()

def vol(self):
        command = "amixer -D pulse sset Master " + str(int(self.val.get())) + "%"
        print(command)
        pexpect.run(command) 

if __name__ == "__main__":
    app = App()
    app.mainloop()
