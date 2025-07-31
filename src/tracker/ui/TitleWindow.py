import customtkinter as tk
import time

from .. import Globals
from .. import ProccessSensorData
from .. import StartAttempt
from ..utils import TimeUtils
from ..sheets import GoogleSheets, LocalSheets

class Frame(tk.CTkFrame):     
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.titleFrame = tk.CTkFrame(master=self, fg_color="#1F6AA5")
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=7, sticky="nsew")

        self.title = tk.CTkLabel(master=self.titleFrame, text="Tracker!", justify="left", font=("Helvetica", 50, "italic", "normal"))
        self.title.pack(side="left", padx=(10), pady=7)

        self.startTime = tk.CTkLabel(master=self.titleFrame, text="", justify="right", font=("Helvetica", 15, "italic", "normal"))
        self.startTime.pack(anchor="ne", padx=(10), pady=7)

        # Only show the button if the timestamp file doesn't exist
        if not StartAttempt.json_exists():
            self.startAttemptButton = tk.CTkButton(
                self,
                text="Start Attempt",
                command=lambda: (
                    StartAttempt.ensure_timestamp_json(),
                    self.startTime.configure(text=StartAttempt.read_timestamp_json()["created_human"]),
                    self.startAttemptButton.grid_forget(),
                    print("Starting Attempt")
                )
            )
            self.startAttemptButton.grid(row=1, column=0, columnspan=2, padx=10, pady=3, sticky="ew")
        else:
            print("Reinitializing Attempt")
            self.startTime.configure(text=StartAttempt.read_timestamp_json()["created_human"])

        self.driverLabel = tk.CTkLabel(master=self, text="Current Driver: ", font=("Helvetica", 20))
        self.driverLabel.grid(row=2, column=0, padx=10, pady=(10, 3), sticky="w")

        self.driver = tk.CTkComboBox(
            master=self, 
            values=Globals.Drivers,
            command=lambda choice: (
                setattr(Globals, "CurrentDriver", choice),
                print("Driver:", choice)
            )
        )
        self.driver.set("None") 
        self.driver.grid(row=3, column=0, columnspan=2, padx=10, pady=(3, 10), sticky="ew")

        self.enableTracking = tk.CTkCheckBox(
            master=self,
            text="Enable Tracking",
            command=lambda: (
                setattr(Globals, "TrackingEnabled", not Globals.TrackingEnabled),
                print("Enable Tracking:", Globals.TrackingEnabled)
            ),            
            height=50,
            font=("Helvetica", 20)
        )
        self.enableTracking.deselect()
        self.enableTracking.grid(row=4, column=0, padx=10, pady=3, sticky="w")

        self.lapFilters = tk.CTkCheckBox(
            master=self,
            text="Lap Filters",
            command=lambda: (
                setattr(Globals, "LapFilters", not Globals.LapFilters),
                print("Lap Filters:", Globals.LapFilters)
            ),
            height=50,
            font=("Helvetica", 20)
        )
        self.lapFilters.select()
        self.lapFilters.grid(row=5, column=0, padx=10, pady=3, sticky="w")

        self.restartSensorButton = tk.CTkButton(self, text="Restart Sensor", command=ProccessSensorData.RestartSensor)
        self.restartSensorButton.grid(row=6, column=0, columnspan=2, padx=10, pady=3, sticky="ew")
