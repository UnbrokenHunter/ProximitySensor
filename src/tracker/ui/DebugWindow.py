import customtkinter as tk

from .. import Globals
from ..sensors import SensorEmulator, Camera


class Frame(tk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        self.titleFrame = tk.CTkFrame(master=self, fg_color="#1F6AA5")
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=7, sticky="nsew")

        self.title = tk.CTkLabel(
            master=self.titleFrame,
            text="Debug:",
            justify="left",
            anchor="w",
            font=("Helvetica", 40, "italic", "normal")
        )
        self.title.pack(side="left", padx=10, pady=7)

        # Mode ComboBox
        self.mode = tk.CTkComboBox(
            master=self,
            values=["Camera", "Sensor Emulator"],
            command=lambda choice: (
                setattr(Globals, "Mode", choice),
                print("Mode:", choice),
                SensorEmulator.Run() if choice == "Sensor Emulator" else Camera.Run()
            )
        )
        self.mode.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.mode.set(Globals.Mode)

        # Min Lap Time Entry
        self.minLapTimeEntry = tk.CTkEntry(
            master=self,
            placeholder_text=f"Min Lap: {Globals.MinLapTime}s",
            height=40,
            font=("Helvetica", 20)
        )
        self.minLapTimeEntry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.minLapTimeEntry.bind("<FocusOut>", lambda e: self.apply_min_lap_time())

        # Broken Sensor Threshold Entry
        self.brokenSensorEntry = tk.CTkEntry(
            master=self,
            placeholder_text=f"Broken Sensor: {Globals.TimeSinceLastFalseThreshold}s",
            height=40,
            font=("Helvetica", 20)
        )
        self.brokenSensorEntry.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.brokenSensorEntry.bind("<FocusOut>", lambda e: self.apply_broken_sensor())

        # Enable Logging Checkbox
        self.enableLoggingCheck = tk.CTkCheckBox(
            master=self,
            text="Enable Logging",
            command=lambda: (
                setattr(Globals, "EnableLogging", self.enableLoggingCheck.get() == 1),
                print("Enable Logging:", Globals.EnableLogging)
            ),
            height=40,
            font=("Helvetica", 20)
        )
        self.enableLoggingCheck.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.enableLoggingCheck.select() if Globals.EnableLogging else self.enableLoggingCheck.deselect()

        # Lap Control Mode ComboBox
        self.controlsLaps = tk.CTkComboBox(
            master=self,
            values=["Local", "Google"],
            command=lambda choice: (
                setattr(Globals, "ControlsLapCount", choice),
                print("Controls Lap Count:", choice)
            )
        )
        self.controlsLaps.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.controlsLaps.set(Globals.ControlsLapCount)

    def apply_min_lap_time(self):
        text = self.minLapTimeEntry.get().strip()
        if text:
            try:
                Globals.MinLapTime = float(text)
                print("Min Lap Time:", Globals.MinLapTime)
            except ValueError:
                print("Invalid Min Lap Time entry")

    def apply_broken_sensor(self):
        text = self.brokenSensorEntry.get().strip()
        if text:
            try:
                Globals.TimeSinceLastFalseThreshold = int(text)
                print("Broken Sensor Threshold:", Globals.TimeSinceLastFalseThreshold)
            except ValueError:
                print("Invalid Broken Sensor Threshold entry")
