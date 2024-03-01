import customtkinter as tk
import Statistics
import Globals
import SensorEmulator
import threading
import time

class ButtonFrame(tk.CTkFrame):
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
        self.title.pack(padx=(10, 40), pady=10)

        self.enableTracking = tk.CTkCheckBox(master=self, text="Enable Tracking", command=self.EnableTracking, height=50, font=("Helvetica", 20))
        self.enableTracking.select()
        self.enableTracking.grid(row=1, column=0, padx=(10, 10), pady=10, sticky="ew")

        self.lapFilters = tk.CTkCheckBox(master=self, text="Lap Filters", command=self.LapFilters, height=50, font=("Helvetica", 20))
        self.lapFilters.select()
        self.lapFilters.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="ew")

        self.driverLabel = tk.CTkLabel(master=self, text="Current Driver: ", font=("Helvetica", 20))
        self.driverLabel.grid(row=3, column=0, padx=(10, 10), pady=(10, 3), sticky="ew")
        
        self.driver = tk.CTkComboBox(master=self, 
                                     values=Globals.Drivers,
                                     command=self.SetDriver)
        self.driver.set("None") 
        self.driver.grid(row=4, column=0, padx=(10, 10), pady=(3, 30), sticky="ew")


class Scrollable(tk.CTkScrollableFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def addItem(self, LapCount, Driver, DistanceDriven, LastLapTime):
            size = 13
            padding = 7

            self.titleFrame = tk.CTkFrame(master=self)
            self.titleFrame.pack(fill="x", padx=(10, 10), pady=5)

            # Lap Count
            self.titleFrame.lapCountLabel = tk.CTkLabel(master=self.titleFrame, text="Lap Count:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCountLabel.grid(row=(LapCount * 2), column=0, padx=padding, pady=(3, 0), sticky="ew")

            self.titleFrame.lapCount = tk.CTkLabel(master=self.titleFrame, text=f"{LapCount}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCount.grid(row=(LapCount * 2) + 1, column=0, padx=padding, pady=(0, 3), sticky="ew")

            # Driver
            self.titleFrame.lapCountLabel = tk.CTkLabel(master=self.titleFrame, text="Driver:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCountLabel.grid(row=(LapCount * 2), column=1, padx=padding, pady=(3, 0), sticky="ew")

            self.titleFrame.lapCount = tk.CTkLabel(master=self.titleFrame, text=f"{Driver}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCount.grid(row=(LapCount * 2) + 1, column=1, padx=padding, pady=(0, 3), sticky="ew")

            # Distance Driven
            self.titleFrame.distanceDrivenLabel = tk.CTkLabel(master=self.titleFrame, text="Distance:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.distanceDrivenLabel.grid(row=(LapCount * 2), column=2, padx=padding, pady=(3, 0), sticky="ew")

            self.titleFrame.distanceDriven = tk.CTkLabel(master=self.titleFrame, text=f"{DistanceDriven}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.distanceDriven.grid(row=(LapCount * 2) + 1, column=2, padx=padding, pady=(0, 3), sticky="ew")

            # Last Lap Time
            self.titleFrame.lastLapTimeLabel = tk.CTkLabel(master=self.titleFrame, text="Lap Time:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lastLapTimeLabel.grid(row=(LapCount * 2), column=3, padx=padding, pady=(3, 0), sticky="ew")

            self.titleFrame.lastLapTime = tk.CTkLabel(master=self.titleFrame, text=f"{LastLapTime}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lastLapTime.grid(row=(LapCount * 2) + 1, column=3, padx=padding, pady=(0, 3), sticky="ew")


class DataFrame(tk.CTkFrame):   
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.LapCount = 0
        padding = 10

        # Time
        self.timeLabel = tk.CTkLabel(master=self, text="Timer:", justify="left", anchor="w", font=("Helvetica", 40, "italic"))
        self.timeLabel.pack(padx=padding, pady=(10, 3))

        self.time = tk.CTkLabel(master=self, text="None", justify="right", anchor="e", font=("Helvetica", 40, "italic"))
        self.time.pack(padx=padding, pady=(5, 3))

        self.frame = tk.CTkFrame(master=self)
        self.frame.pack(fill="both", padx=padding, pady=(3, 3))

        # Average Lap Time
        self.averageLapTimeLabel = tk.CTkLabel(master=self.frame, text="Average Lap:", justify="left", anchor="w", font=("Helvetica", 20))
        self.averageLapTimeLabel.grid(row=0, column=0, padx=padding, pady=7)

        self.averageLapTime = tk.CTkLabel(master=self.frame, text="No Laps", justify="right", anchor="e", font=("Helvetica", 20))
        self.averageLapTime.grid(row=0, column=1, padx=padding, pady=7)

        # Projected End Time
        self.projectedEndTimeLabel = tk.CTkLabel(master=self.frame, text="Projected Time Left:", justify="left", anchor="w", font=("Helvetica", 20))
        self.projectedEndTimeLabel.grid(row=1, column=0, padx=padding, pady=7)

        self.projectedEndTime = tk.CTkLabel(master=self.frame, text="00:00:00", justify="right", anchor="e", font=("Helvetica", 20))
        self.projectedEndTime.grid(row=1, column=1, padx=padding, pady=7)

        self.scrollable = Scrollable(master=self, width=300)
        self.scrollable.pack(fill="both", expand=True, padx=padding, pady=10)

        def Update():
            while True:
                if self.LapCount != Globals.LapCount:
                    self.LapCount += 1
                    self.scrollable.addItem(Globals.LapCount, 
                                            Statistics.GetCurrentDriver(), 
                                            str(round(Statistics.GetDistanceDriven(), 2)), 
                                            Globals.FormatTime(Statistics.GetLastLapTime()))
                    
                self.time.configure(text=Globals.FormatTime(time.time() - Globals.StartTime))
                self.averageLapTime.configure(text=Globals.FormatTime(Statistics.GetAverageLapTime()))
                self.projectedEndTime.configure(text=Globals.FormatTime(Statistics.GetProjectedEndTime()))

                time.sleep(0.5)  # Delay for half a second

        # self.update = tk.CTkButton(master=self, text="Update", command=Update, height=50, font=("Helvetica", 20))
        # self.update.grid(row=5, column=0, padx=(10, 10), pady=30, sticky="ew")

        updateUIThread = threading.Thread(target=Update)
        updateUIThread.start()


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        tk.set_appearance_mode("System")  # Modes: system (default), light, dark
        tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.title("Lap Tracker")
        self.geometry("800x500")

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.frame = ButtonFrame(master=self)
        self.frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nswe")

        self.frame = DataFrame(master=self)
        self.frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nswe")

if __name__ == "__main__":
    app = App()
    app.mainloop()

    
