import tkinter
import tkinter.messagebox
import customtkinter
import pexpect
import getpass
import os
import time
from PIL import Image

long_path = "/home/" + getpass.getuser() + "/CycOwl/"

delay_ms = 750

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_widget_scaling(1.2)
        customtkinter.set_appearance_mode("Light")

        # configure window
        self.title("Loading Screen")
        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, columnspan=4, rowspan=9, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.loading_label = customtkinter.CTkLabel(self.sidebar_frame, text="Loading", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.loading_label.place(relx=.5, rely=.9, anchor=tkinter.CENTER)

        image_size = 350
        cyc_owl = customtkinter.CTkImage(light_image=Image.open(long_path + "baseImage.png"), size=(image_size, image_size))
        image_holder = customtkinter.CTkButton(self.sidebar_frame, image=cyc_owl, text=None, height=image_size, width=image_size, fg_color=("#DBDBDB", "#2B2B2B"), hover=False)
        image_holder.place(relx=.5, rely=.4, anchor=tkinter.CENTER)

        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", width=70, border_width=2, command= lambda: callClose(self))
        self.exit_button.place(relx=.09, rely=.9, anchor=tkinter.CENTER)

        if not self.attributes('-fullscreen'):
            self.attributes('-fullscreen', True)

def checkLoading():
    print("CHECKING")
    with open(long_path + "loading.txt") as loading:
        lines = loading.readlines()
        if lines[0].strip() == "true":
            app.destroy()

    if app.loading_label.cget("text") == "Loading...":
        app.loading_label.configure(text="Loading")
    elif app.loading_label.cget("text") == "Loading":
        app.loading_label.configure(text="Loading.")
    elif app.loading_label.cget("text") == "Loading.":
        app.loading_label.configure(text="Loading..")
    elif app.loading_label.cget("text") == "Loading..":
        app.loading_label.configure(text="Loading...")

    if not app.attributes("-fullscreen"):
        app.attributes('-fullscreen', True)

    app.after(delay_ms, checkLoading)

def callClose(self):
    self.destroy()

if __name__ == "__main__":
    app = App()
    print ("Done initializing")
    app.after(delay_ms, checkLoading)
    app.mainloop()
