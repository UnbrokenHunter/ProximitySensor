import customtkinter as tk

from .ui import TitleWindow, DataWindow, DebugWindow
from .sensors import Camera

class App(tk.CTk):
    def __init__(self):
        super().__init__()
        tk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.title("Lap Tracker")
        self.geometry("1600x600")

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        self.frame = TitleWindow.Frame(master=self)
        self.frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nswe")

        self.frame = DataWindow.Frame(master=self)
        self.frame.grid(row=0, column=1, padx=10, pady=20, sticky="nswe")

        self.debug = DebugWindow.Frame(master=self)  # Place your debug frame in this new window
        self.debug.grid(row=0, column=2, padx=(10, 20), pady=20, sticky="nswe")

        Camera.Run()


def run():
    app = App()
    app.mainloop()

     