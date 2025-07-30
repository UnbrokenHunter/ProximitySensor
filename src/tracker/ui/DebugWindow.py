import customtkinter as tk

from .. import Globals
from ..sensors import SensorEmulator
from ..sensors import Camera

class Frame(tk.CTkScrollableFrame):  
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.CreateUI()

    def Mode(self, choice):
        Globals.Mode = choice
        print("Mode: ", choice)

        SensorEmulator.Run()
        Camera.Run()


    def EnableLogging(self):
        Globals.EnableLogging = not Globals.EnableLogging
        print("Enable Logging: ", Globals.EnableLogging)

    def Pin(self):
        Globals.Pin = int(self.pinEntry.get())
        print("Pin: ", Globals.Pin)

    def Delay(self):
        Globals.SensorDelay = float(self.delayEntry.get())
        print("Delay: ", Globals.SensorDelay)

    def UIDelay(self):
        Globals.UIDelay = float(self.uidelayEntry.get())
        print("UI Delay: ", Globals.UIDelay)

    def MinLapTime(self):
        Globals.MinLapTime = float(self.minLapTimeEntry.get())
        print("Min Lap Time: ", Globals.MinLapTime)

    def BrokenSensorDetection(self):
        Globals.TimeSinceLastFalseThreshold = int(self.brokenSensorEntry.get())
        print("Broken Sensor: ", Globals.TimeSinceLastFalseThreshold)

    def ControlsLapCount(self, choice):
        Globals.ControlsLapCount = choice
        print("Controls Lap Count: ", Globals.ControlsLapCount)

    def ManualSetStartTime(self):
        Globals.StartTime = float(self.manualStartTime.get())
        Globals.ManualTimeSet = True
        print("Start Time: ", Globals.StartTime)

    def CreateUI(self):
        self.titleFrame = tk.CTkFrame(master=self)
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=7, sticky="ew")

        self.title = tk.CTkLabel(master=self.titleFrame, text="Debug:", justify="left", anchor="w",font=("Helvetica", 40, "italic", "normal"))
        self.title.pack(padx=(10, 40), pady=10, fill="x")

        self.mode = tk.CTkComboBox(master=self, 
                                     values=["Camera", "Sensor Emulator"],
                                     command=self.Mode)
        self.mode.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.pinEntry = tk.CTkEntry(master=self, placeholder_text=f"Pin: {Globals.Pin}", height=40, font=("Helvetica", 20))
        self.pinEntry.grid(row=2, column=0, padx=(10, 5), pady=5)

        self.pinButton = tk.CTkButton(master=self, text="Select Pin", command=self.Pin, height=40, font=("Helvetica", 20))
        self.pinButton.grid(row=2, column=1, padx=(5, 10), pady=5)

        self.delayEntry = tk.CTkEntry(master=self, placeholder_text=f"Delay: {Globals.SensorDelay}s", height=40, font=("Helvetica", 20))
        self.delayEntry.grid(row=3, column=0, padx=(10, 5), pady=5)

        self.delayButton = tk.CTkButton(master=self, text="Select Delay", command=self.Delay, height=40, font=("Helvetica", 20))
        self.delayButton.grid(row=3, column=1, padx=(5, 10), pady=5)

        self.uidelayEntry = tk.CTkEntry(master=self, placeholder_text=f"UI Delay: {Globals.SensorDelay}s", height=40, font=("Helvetica", 20))
        self.uidelayEntry.grid(row=4, column=0, padx=(10, 5), pady=5)

        self.uidelayButton = tk.CTkButton(master=self, text="Select Delay", command=self.Delay, height=40, font=("Helvetica", 20))
        self.uidelayButton.grid(row=4, column=1, padx=(5, 10), pady=5)

        self.minLapTimeEntry = tk.CTkEntry(master=self, placeholder_text=f"Min Lap: {Globals.MinLapTime}s", height=40, font=("Helvetica", 20))
        self.minLapTimeEntry.grid(row=5, column=0, padx=(10, 5), pady=5)

        self.minLapTimeBtn = tk.CTkButton(master=self, text="Select Time", command=self.MinLapTime, height=40, font=("Helvetica", 20))
        self.minLapTimeBtn.grid(row=5, column=1, padx=(5, 10), pady=5)


        self.brokenSensorEntry = tk.CTkEntry(master=self, placeholder_text=f"Broken Sensor: {Globals.TimeSinceLastFalseThreshold}s", height=40, font=("Helvetica", 20))
        self.brokenSensorEntry.grid(row=6, column=0, padx=(10, 5), pady=5)

        self.brokenSensorBtn = tk.CTkButton(master=self, text="Select Value", command=self.BrokenSensorDetection, height=40, font=("Helvetica", 20))
        self.brokenSensorBtn.grid(row=6, column=1, padx=(5, 10), pady=5)

        self.enableLoggingCheck = tk.CTkCheckBox(master=self, text="Enable Logging", command=self.EnableLogging, height=40, font=("Helvetica", 20))
        self.enableLoggingCheck.deselect()
        self.enableLoggingCheck.grid(row=7, column=0, columnspan=2, padx=(5, 10), pady=5, sticky="ew")

        self.controlsLaps = tk.CTkComboBox(master=self, 
                                     values=["Local", "Google"],
                                     command=self.ControlsLapCount)
        self.controlsLaps.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.manualStartTime = tk.CTkEntry(master=self, placeholder_text=f"Start Time: {Globals.StartTime}s", height=40, font=("Helvetica", 20))
        self.manualStartTime.grid(row=9, column=0, padx=(10, 5), pady=5)

        self.manualStartTimeBtn = tk.CTkButton(master=self, text="Set Time", command=self.ManualSetStartTime, height=40, font=("Helvetica", 20))
        self.manualStartTimeBtn.grid(row=9, column=1, padx=(5, 10), pady=5)
