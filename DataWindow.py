import customtkinter as tk
import Globals
import Statistics
import threading
import time

class Scrollable(tk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.itemList = []

    def addItem(self, LapCount, Driver, DistanceDriven, LastLapTime):
            size = 13
            padding = 10

            self.titleFrame = tk.CTkFrame(master=self)
            self.titleFrame.grid(padx=10, pady=5)

            # Lap Count
            self.titleFrame.lapCountLabel = tk.CTkLabel(master=self.titleFrame, text="Lap Count:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCountLabel.grid(row=(LapCount * 2), column=0, padx=padding, pady=(3, 0),)

            self.titleFrame.lapCount = tk.CTkLabel(master=self.titleFrame, text=f"{LapCount}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCount.grid(row=(LapCount * 2) + 1, column=0, padx=padding, pady=(0, 3),)

            # Driver
            self.titleFrame.lapCountLabel = tk.CTkLabel(master=self.titleFrame, text="Driver:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCountLabel.grid(row=(LapCount * 2), column=1, padx=padding, pady=(3, 0),)

            self.titleFrame.lapCount = tk.CTkLabel(master=self.titleFrame, text=f"{Driver}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lapCount.grid(row=(LapCount * 2) + 1, column=1, padx=padding, pady=(0, 3),)

            # Distance Driven
            self.titleFrame.distanceDrivenLabel = tk.CTkLabel(master=self.titleFrame, text="Distance:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.distanceDrivenLabel.grid(row=(LapCount * 2), column=2, padx=padding, pady=(3, 0),)

            self.titleFrame.distanceDriven = tk.CTkLabel(master=self.titleFrame, text=f"{DistanceDriven}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.distanceDriven.grid(row=(LapCount * 2) + 1, column=2, padx=padding, pady=(0, 3),)

            # Last Lap Time
            self.titleFrame.lastLapTimeLabel = tk.CTkLabel(master=self.titleFrame, text="Lap Time:", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lastLapTimeLabel.grid(row=(LapCount * 2), column=3, padx=padding, pady=(3, 0),)

            self.titleFrame.lastLapTime = tk.CTkLabel(master=self.titleFrame, text=f"{LastLapTime}", justify="left", anchor="w", font=("Helvetica", size))
            self.titleFrame.lastLapTime.grid(row=(LapCount * 2) + 1, column=3, padx=padding, pady=(0, 3))

            self.itemList.append(self.titleFrame)

            index = len(self.itemList)
            for item in self.itemList:
                item.grid(row=index)
                index -= 1

class Frame(tk.CTkFrame):   
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.LapCount = 0
        padding = 10

        self.timeFrame = tk.CTkFrame(master=self)
        self.timeFrame.pack(fill="both", padx=padding, pady=(3, 3))

        # Time
        self.timeLabel = tk.CTkLabel(master=self.timeFrame, text="Timer:", font=("Helvetica", 40, "italic"))
        self.timeLabel.grid(row=0, column=0, padx=padding, pady=(5, 3))

        self.time = tk.CTkLabel(master=self.timeFrame, text="None", font=("Helvetica", 40, "italic"))
        self.time.grid(row=0, column=1, padx=padding, pady=(5, 3))

        self.frame = tk.CTkFrame(master=self)
        self.frame.pack(fill="both", padx=padding, pady=(3, 3))

        # Average Lap Time
        self.currentLapTimeLabel = tk.CTkLabel(master=self.frame, text="Current Lap:", justify="left", anchor="w", font=("Helvetica", 20))
        self.currentLapTimeLabel.grid(row=0, column=0, padx=padding, pady=7)

        self.currentLapTime = tk.CTkLabel(master=self.frame, text="No Laps", justify="right", anchor="e", font=("Helvetica", 20))
        self.currentLapTime.grid(row=0, column=1, padx=padding, pady=7)

        # Average Lap Time
        self.averageLapTimeLabel = tk.CTkLabel(master=self.frame, text="Average Lap:", justify="left", anchor="w", font=("Helvetica", 20))
        self.averageLapTimeLabel.grid(row=1, column=0, padx=padding, pady=7)

        self.averageLapTime = tk.CTkLabel(master=self.frame, text="No Laps", justify="right", anchor="e", font=("Helvetica", 20))
        self.averageLapTime.grid(row=1, column=1, padx=padding, pady=7)

        # Projected End Time
        self.projectedEndTimeLabel = tk.CTkLabel(master=self.frame, text="Projected Time Left:", justify="left", anchor="w", font=("Helvetica", 20))
        self.projectedEndTimeLabel.grid(row=2, column=0, padx=padding, pady=7)

        self.projectedEndTime = tk.CTkLabel(master=self.frame, text="00:00:00", justify="right", anchor="e", font=("Helvetica", 20))
        self.projectedEndTime.grid(row=2, column=1, padx=padding, pady=7)

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
                self.currentLapTime.configure(text=Globals.FormatTime(Globals.CurrentLapTime))
                self.averageLapTime.configure(text=Globals.FormatTime(Statistics.GetAverageLapTime()))
                self.projectedEndTime.configure(text=Globals.FormatTime(Statistics.GetProjectedEndTime()))

                time.sleep(0.5)  # Delay for half a second

        # self.update = tk.CTkButton(master=self, text="Update", command=Update, height=50, font=("Helvetica", 20))
        # self.update.grid(row=5, column=0, padx=(10, 10), pady=30, sticky="ew")

        updateUIThread = threading.Thread(target=Update, daemon=True)
        updateUIThread.start()

