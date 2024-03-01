import customtkinter as tk
import Statistics
import Globals
import SensorEmulator
import threading
import time

def FormatTime(time):
    # Extract whole seconds and milliseconds
    seconds = int(time)
    milliseconds = int((time - seconds) * 1000)
    
    # Compute hours, minutes, and seconds
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    # Return formatted time string including milliseconds
    return "%d:%02d:%02d.%03d" % (hour, minutes, seconds, milliseconds)

class ButtonFrame(tk.CTkFrame):
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
        self.enableTracking.grid(row=1, column=0, padx=(10, 10), pady=30, sticky="ew")

        self.driverLabel = tk.CTkLabel(master=self, text="Current Driver: ", font=("Helvetica", 20))
        self.driverLabel.grid(row=2, column=0, padx=(10, 10), pady=(30, 3), sticky="ew")
        
        self.driver = tk.CTkComboBox(master=self, 
                                     values=["Mac", "Mitchell", "Josh", "Hunter", "John Walter"],
                                     command=self.SetDriver)
        self.driver.set("None") 
        self.driver.grid(row=3, column=0, padx=(10, 10), pady=(3, 30), sticky="ew")


class Scrollable(tk.CTkScrollableFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def addItem(self, LapCount, Driver, DistanceDriven, LastLapTime):
            size = 13

            # Lap Count
            lapCountLabel = tk.CTkLabel(master=self, text="Lap Count:", justify="left", anchor="w", font=("Helvetica", size))
            lapCountLabel.grid(row=(LapCount * 2), column=0, padx=(3, 3), pady=(3, 0), sticky="ew")

            lapCount = tk.CTkLabel(master=self, text=f"{LapCount}", justify="left", anchor="e", font=("Helvetica", size))
            lapCount.grid(row=(LapCount * 2) + 1, column=0, padx=(3, 3), pady=(0, 3), sticky="ew")

            # Driver
            lapCountLabel = tk.CTkLabel(master=self, text="Driver:", justify="left", anchor="w", font=("Helvetica", size))
            lapCountLabel.grid(row=(LapCount * 2), column=1, padx=(3, 3), pady=(3, 0), sticky="ew")

            lapCount = tk.CTkLabel(master=self, text=f"{Driver}", justify="left", anchor="e", font=("Helvetica", size))
            lapCount.grid(row=(LapCount * 2) + 1, column=1, padx=(3, 3), pady=(0, 3), sticky="ew")

            # Distance Driven
            distanceDrivenLabel = tk.CTkLabel(master=self, text="Distance Driven:", justify="left", anchor="w", font=("Helvetica", size))
            distanceDrivenLabel.grid(row=(LapCount * 2), column=2, padx=(3, 3), pady=(3, 0), sticky="ew")

            distanceDriven = tk.CTkLabel(master=self, text=f"{DistanceDriven}", justify="left", anchor="e", font=("Helvetica", size))
            distanceDriven.grid(row=(LapCount * 2) + 1, column=2, padx=(3, 3), pady=(0, 3), sticky="ew")

            # Last Lap Time
            lastLapTimeLabel = tk.CTkLabel(master=self, text="Lap Time:", justify="left", anchor="w", font=("Helvetica", size))
            lastLapTimeLabel.grid(row=(LapCount * 2), column=3, padx=(7, 3), pady=(3, 0), sticky="ew")

            lastLapTime = tk.CTkLabel(master=self, text=f"{LastLapTime}", justify="left", anchor="e", font=("Helvetica", size))
            lastLapTime.grid(row=(LapCount * 2) + 1, column=3, padx=(7, 3), pady=(0, 3), sticky="ew")


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
                                            FormatTime(Statistics.GetLastLapTime()))
                    
                self.time.configure(text=FormatTime(time.time() - Globals.StartTime))
                self.averageLapTime.configure(text=FormatTime(Statistics.GetAverageLapTime()))
                self.projectedEndTime.configure(text=FormatTime(Statistics.GetProjectedEndTime()))

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

    
