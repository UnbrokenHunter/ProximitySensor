import time
import threading
import customtkinter as tk

from ..utils import TimeUtils
from .. import Globals
from .. import Statistics

class Scrollable(tk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.itemList = []

    def addItem(self, LapCount, Driver, DistanceDriven, LastLapTime):
        size = 13
        padding = 10

        # Create lap row frame
        row = tk.CTkFrame(master=self)
        row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def make_pair(label_text, value_text, col):
            tk.CTkLabel(row, text=label_text, anchor="w", font=("Helvetica", size)).grid(row=0, column=col, sticky="w", padx=padding)
            tk.CTkLabel(row, text=value_text, anchor="w", font=("Helvetica", size)).grid(row=1, column=col, sticky="w", padx=padding)

        make_pair("Lap Count:", str(LapCount), 0)
        make_pair("Driver:", str(Driver), 1)
        make_pair("Distance:", f"{float(DistanceDriven) / 1000:.2f} km", 2)
        make_pair("Lap Time:", str(LastLapTime), 3)

        # Insert new row visually at the top
        if self.itemList:
            row.pack(fill="x", padx=10, pady=5, before=self.itemList[0])
        else:
            row.pack(fill="x", padx=10, pady=5)

        self.itemList.insert(0, row)

        # Remove oldest row if more than 5
        if len(self.itemList) > 5:
            oldest = self.itemList.pop()
            oldest.pack_forget()

class Frame(tk.CTkFrame):   
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.LapCount = 0
        padding = 10

        # ========== TIMER LABELS ==========
        self.timeFrame = tk.CTkFrame(self)
        self.timeFrame.pack(fill="both", padx=padding, pady=3)

        self.timeLabel = tk.CTkLabel(self.timeFrame, text="Timer:", font=("Helvetica", 40, "italic"))
        self.timeLabel.grid(row=0, column=0, padx=padding, pady=5)

        self.time = tk.CTkLabel(self.timeFrame, text="None", font=("Helvetica", 40, "italic"))
        self.time.grid(row=0, column=1, padx=padding, pady=5)

        # ========== STAT LABELS ==========
        self.frame = tk.CTkFrame(self)
        self.frame.pack(fill="both", padx=padding, pady=3)

        def label_row(text, row, ref):
            tk.CTkLabel(self.frame, text=text, anchor="w", font=("Helvetica", 20)).grid(row=row, column=0, padx=padding, pady=7)
            label = tk.CTkLabel(self.frame, text="No Laps", anchor="e", font=("Helvetica", 20))
            label.grid(row=row, column=1, padx=padding, pady=7)
            setattr(self, ref, label)

        label_row("Current Lap:", 0, "currentLapTime")
        label_row("Average Lap:", 1, "averageLapTime")
        label_row("Projected Time Left:", 2, "projectedEndTime")

        # ========== SCROLLABLE PANEL ==========
        self.scrollable = Scrollable(self)
        self.scrollable.pack(fill="both", expand=True, padx=padding, pady=10)

        # ========== UPDATE LOOP ==========
        def Update():
            while True:
                if self.LapCount != Globals.LapCount:
                    self.LapCount = Globals.LapCount
                    self.scrollable.addItem(
                        Globals.LapCount,
                        Statistics.GetCurrentDriver(),
                        f"{Statistics.GetDistanceDriven():.2f}",
                        TimeUtils.FormatTime(Statistics.GetLastLapTime())
                    )

                self.time.configure(text=TimeUtils.FormatTime(time.time() - Globals.StartTime))
                self.currentLapTime.configure(text=TimeUtils.FormatTime(Globals.CurrentLapTime))
                self.averageLapTime.configure(text=TimeUtils.FormatTime(Statistics.GetAverageLapTime()))
                self.projectedEndTime.configure(text=TimeUtils.FormatTime(Statistics.GetProjectedEndTime()))

                time.sleep(Globals.UIDelay)

        threading.Thread(target=Update, daemon=True).start()
