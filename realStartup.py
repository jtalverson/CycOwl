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

	self.loading_label = customtkinter.CTkLabel(self.sidebar_frame, text="Loading...", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.loading_label.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)

	if not self.attributes('-fullscreen'):
		self.attributes('-fullscreen', True)

	control = True
	while control:
		with open(long_path + "loading.txt") as loading:
			lines = loading.readlines()
			if lines[0].strip() == "true":
				self.destroy()
				control = False

if __name__ == "__main__":
    app = App()
    app.mainloop()
