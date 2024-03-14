import customtkinter as tk
import Globals
import Sheets
import LocalSheets
import time

class Frame(tk.CTkFrame):     
    
    manualDriverInput = "None"

    def LapFilters(self):
        Globals.LapFilters = not Globals.LapFilters
        print("Lap Filters: ", Globals.LapFilters)

    def EnableTracking(self):
        if (Globals.RealStart == False):
            Globals.RealStart = True
            Globals.StartTime = time.time()
            self.startTime.configure(text=time.strftime("%Y-%m-%d %H:%M:%S"))
        
        Globals.TrackingEnabled = not Globals.TrackingEnabled
        print("Enable Tracking: ", Globals.TrackingEnabled)

    def SetDriver(self, choice):
        Globals.CurrentDriver = choice
        print("Driver: ", choice)

    def SetManualDriver(self, choice):
        self.manualDriverInput = choice
        print("Manual Driver Set:", choice)

    def AddManualLap(self):
        Sheets.SaveDataManual(self.lapTime.get(), self.manualDriverInput, self.distanceDriven.get(), "", "")
        LocalSheets.SaveDataManual(self.lapTime.get(), self.manualDriverInput, self.distanceDriven.get(), "", "")
        print("Manual Lap Added")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.titleFrame = tk.CTkFrame(master=self, fg_color="#1F6AA5")
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=7, sticky="nsew")

        self.title = tk.CTkLabel(master=self.titleFrame, text="Lap Tracker", justify="left", font=("Helvetica", 50, "italic", "normal"))
        self.title.pack(side="left", padx=(10), pady=7)

        self.startTime = tk.CTkLabel(master=self.titleFrame, text="", justify="right", font=("Helvetica", 20, "italic", "normal"))
        self.startTime.pack(anchor="se", padx=(10), pady=7)

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
        

        padding = 10

        self.addLapFrame = tk.CTkFrame(master=self)
        self.addLapFrame.grid(row=5, column=0, columnspan=2, padx=10, pady=(3, 6), sticky="nsew")

        self.addLapFrame.grid_columnconfigure(0, weight=1)
        self.addLapFrame.grid_columnconfigure(1, weight=1)

        self.addLapFrameLabel = tk.CTkLabel(master=self.addLapFrame, text="Manual Add: ", justify="left", anchor="w", font=("Helvetica", 20))
        self.addLapFrameLabel.grid(row=0, column=0, padx=10, pady=(6, 3), sticky="ew", columnspan=2)

        self.lapCount = tk.CTkEntry(master=self.addLapFrame, placeholder_text="Description: ", font=("Helvetica", 20))
        self.lapCount.grid(row=1, column=0, padx=padding, pady=7, sticky="ew")

        self.manualDriver = tk.CTkComboBox(master=self.addLapFrame, 
                                     values=Globals.Drivers,
                                     command=self.SetManualDriver)
        self.manualDriver.grid(row=1, column=1, padx=padding, pady=7, sticky="ew")

        self.lapTime = tk.CTkEntry(master=self.addLapFrame, placeholder_text="Lap Time: ", font=("Helvetica", 20))
        self.lapTime.grid(row=2, column=0, padx=padding, pady=7, sticky="ew")

        self.distanceDriven= tk.CTkEntry(master=self.addLapFrame, placeholder_text="Distance Driven (km): ", font=("Helvetica", 20))
        self.distanceDriven.grid(row=2, column=1, padx=padding, pady=(4, 5), sticky="ew")

        self.confirmLap = tk.CTkButton(master=self.addLapFrame, text="Add Lap: ", font=("Helvetica", 20), command=self.AddManualLap)
        self.confirmLap.grid(row=3, column=0, columnspan=2, padx=padding, pady=(7, 10))


