import time
import threading
import customtkinter as tk

from ..sheets import LocalSheets
from ..utils import TimeUtils
from ..utils.event_bus import event_bus
from .. import Globals
from .. import Statistics
from .. import StartAttempt

class Scrollable(tk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.itemList = []

    def addItem(self, LapCount, LastLapTime, Driver, Timestamp):
        size = 13
        padding = 10

        # Create lap row frame
        row = tk.CTkFrame(master=self)
        row.grid_columnconfigure((0, 1, 2, 3), weight=1)

        def make_pair(label_text, value_text, col):
            tk.CTkLabel(row, text=label_text, anchor="w", font=("Helvetica", size)).grid(row=0, column=col, sticky="w", padx=padding)
            tk.CTkLabel(row, text=value_text, anchor="w", font=("Helvetica", size)).grid(row=1, column=col, sticky="w", padx=padding)

        make_pair("Lap Count:", str(LapCount), 0)
        make_pair("Lap Time:", str(LastLapTime), 1)
        make_pair("Driver:", str(Driver), 2)

        if isinstance(Timestamp, (float, int)):
            timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(Timestamp))
        else:
            timestamp_str = str(Timestamp)

        make_pair("Timestamp:", timestamp_str, 3)

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
            tk.CTkLabel(self.frame, text=text, anchor="w", font=("Helvetica", 20)).grid(row=row, column=0, padx=padding, pady=7, sticky="w")
            label = tk.CTkLabel(self.frame, text="No Laps", anchor="w", font=("Helvetica", 20))
            label.grid(row=row, column=1, padx=padding, pady=7, sticky="w")
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
                if StartAttempt.json_exists():
                    self.time.configure(text=TimeUtils.FormatTime(time.time() - StartAttempt.read_timestamp_json()["created"]))
                    self.currentLapTime.configure(text=TimeUtils.FormatTime(Globals.CurrentLapTime))
                    self.averageLapTime.configure(text=TimeUtils.FormatTime(Statistics.GetAverageLapTime()))
                    self.projectedEndTime.configure(text=TimeUtils.FormatTime(Statistics.GetProjectedEndTime()))
                else: 
                    self.time.configure(text="")
                    self.currentLapTime.configure(text="")
                    self.averageLapTime.configure(text="")
                    self.projectedEndTime.configure(text="")

                time.sleep(Globals.UIDelay)

        threading.Thread(target=Update, daemon=True).start()
        
        # Subscribe to update event
        event_bus.subscribe("refresh_recent_laps", self.refresh_recent_laps)

    def refresh_recent_laps(self):
        for row in self.scrollable.itemList:
            row.destroy()
        self.scrollable.itemList.clear()

        laps = LocalSheets.get_last_n_laps()[::-1]  # Reverse to oldest first
        for lap in laps:
            self.scrollable.addItem(
                lap["lap_count"],
                lap["lap_time"],
                lap["driver"],
                lap["timestamp"]
            )

