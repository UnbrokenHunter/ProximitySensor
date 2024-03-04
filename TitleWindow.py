import customtkinter as tk
import Globals

class Frame(tk.CTkFrame):     
    def LapFilters(self):
        Globals.LapFilters = not Globals.LapFilters
        print("Lap Filters: ", Globals.LapFilters)

    def EnableTracking(self):
        Globals.TrackingEnabled = not Globals.TrackingEnabled
        print("Enable Tracking: ", Globals.TrackingEnabled)

    def SetDriver(self, choice):
        Globals.CurrentDriver = choice
        print("Driver: ", choice)

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.titleFrame = tk.CTkFrame(master=self, fg_color="#1F6AA5")
        self.titleFrame.grid(row=0, column=0, padx=(10, 10), pady=20, sticky="ew")

        self.title = tk.CTkLabel(master=self.titleFrame, text="Lap Tracker", font=("Helvetica", 50, "italic", "normal"))
        self.title.pack(padx=(30, 40), pady=10)

        self.driverLabel = tk.CTkLabel(master=self, text="Current Driver: ", font=("Helvetica", 20))
        self.driverLabel.grid(row=1, column=0, padx=(10, 10), pady=(10, 3), sticky="ew")
        
        self.driver = tk.CTkComboBox(master=self, 
                                     values=Globals.Drivers,
                                     command=self.SetDriver)
        self.driver.set("None") 
        self.driver.grid(row=2, column=0, padx=(10, 10), pady=(3, 30), sticky="ew")

        self.enableTracking = tk.CTkCheckBox(master=self, text="Enable Tracking", command=self.EnableTracking, height=50, font=("Helvetica", 20))
        self.enableTracking.select()
        self.enableTracking.grid(row=3, column=0, padx=(10, 10), pady=10, sticky="ew")

        self.lapFilters = tk.CTkCheckBox(master=self, text="Lap Filters", command=self.LapFilters, height=50, font=("Helvetica", 20))
        self.lapFilters.select()
        self.lapFilters.grid(row=4, column=0, padx=(10, 10), pady=10, sticky="ew")
        