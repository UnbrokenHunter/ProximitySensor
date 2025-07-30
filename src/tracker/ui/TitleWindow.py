import customtkinter as tk
import time

from .. import Globals
from ..sheets import Sheets, LocalSheets


class Frame(tk.CTkFrame):     
    
    manualDriverInput = "None"

    def LapFilters(self):
        Globals.LapFilters = not Globals.LapFilters
        print("Lap Filters: ", Globals.LapFilters)

    def EnableTracking(self):
        if (Globals.ManualTimeSet == True):
            self.startTime.configure(text=Globals.ConvertToFormattedDate(Globals.StartTime))
            self.startTimeUnix.configure(text=Globals.StartTime)
        elif (Globals.RealStart == False):
            Globals.RealStart = True
            Globals.StartTime = time.time()
            self.startTime.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))
            self.startTimeUnix.configure(text=Globals.StartTime)
            
        Globals.TrackingEnabled = not Globals.TrackingEnabled
        print("Enable Tracking: ", Globals.TrackingEnabled)

    def SetDriver(self, choice):
        Globals.CurrentDriver = choice
        print("Driver: ", choice)

    def SetManualDriver(self, choice):
        self.manualDriverInput = choice
        print("Manual Driver Set:", choice)

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.titleFrame = tk.CTkFrame(master=self, fg_color="#1F6AA5")
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=7, sticky="nsew")

        self.title = tk.CTkLabel(master=self.titleFrame, text="Lap Tracker", justify="left", font=("Helvetica", 50, "italic", "normal"))
        self.title.pack(side="left", padx=(10), pady=7)

        self.startTime = tk.CTkLabel(master=self.titleFrame, text="", justify="right", font=("Helvetica", 20, "italic", "normal"))
        self.startTime.pack(anchor="ne", padx=(10), pady=7)

        self.startTimeUnix = tk.CTkLabel(master=self.titleFrame, text="", justify="right", font=("Helvetica", 20, "italic", "normal"))
        self.startTimeUnix.pack(anchor="se", padx=(10), pady=7)

        self.driverLabel = tk.CTkLabel(master=self, text="Current Driver: ", font=("Helvetica", 20))
        self.driverLabel.grid(row=1, column=0, padx=10, pady=(10, 3), sticky="ew")
        
        self.driver = tk.CTkComboBox(master=self, 
                                     values=Globals.Drivers,
                                     command=self.SetDriver)
        self.driver.set("None") 
        self.driver.grid(row=2, column=0, padx=10, pady=(3, 10), sticky="ew")

        self.enableTracking = tk.CTkCheckBox(master=self, text="Enable Tracking", command=self.EnableTracking, height=50, font=("Helvetica", 20))
        self.enableTracking.deselect()
        self.enableTracking.grid(row=3, column=0, padx=10, pady=3, sticky="ew")

        self.lapFilters = tk.CTkCheckBox(master=self, text="Lap Filters", command=self.LapFilters, height=50, font=("Helvetica", 20))
        self.lapFilters.select()
        self.lapFilters.grid(row=4, column=0, padx=10, pady=3, sticky="ew")
        


