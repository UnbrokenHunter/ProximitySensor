import customtkinter as tk
import Globals
import Sensor
import SensorEmulator
import MotionSensor

class Frame(tk.CTkFrame):  
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.CreateUI()

    def Mode(self, choice):
        Globals.Mode = choice
        print("Mode: ", choice)

        SensorEmulator.Run()
        Sensor.Run()
        MotionSensor.Run()

    def Pin(self):
        Globals.Pin = int(self.pinEntry.get())
        print("Pin: ", Globals.Pin)

    def Delay(self):
        Globals.SensorDelay = float(self.delayEntry.get())
        print("Delay: ", Globals.SensorDelay)

    def MinLapTime(self):
        Globals.MinLapTime = float(self.minLapTimeEntry.get())
        print("Min Lap Time: ", Globals.MinLapTime)

    def BrokenSensorDetection(self):
        Globals.TimeSinceLastFalseThreshold = int(self.brokenSensorEntry.get())
        print("Broken Sensor: ", Globals.TimeSinceLastFalseThreshold)

    def CreateUI(self):
        self.titleFrame = tk.CTkFrame(master=self)
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=7, sticky="ew")

        self.title = tk.CTkLabel(master=self.titleFrame, text="Debug:", justify="left", anchor="w",font=("Helvetica", 40, "italic", "normal"))
        self.title.pack(padx=(10, 40), pady=10, fill="x")

        self.mode = tk.CTkComboBox(master=self, 
                                     values=["Sensor", "Motion Sensor", "Sensor Emulator"],
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


        self.minLapTimeEntry = tk.CTkEntry(master=self, placeholder_text=f"Min Lap: {Globals.SensorDelay}s", height=40, font=("Helvetica", 20))
        self.minLapTimeEntry.grid(row=4, column=0, padx=(10, 5), pady=5)

        self.minLapTimeBtn = tk.CTkButton(master=self, text="Select Time", command=self.MinLapTime, height=40, font=("Helvetica", 20))
        self.minLapTimeBtn.grid(row=4, column=1, padx=(5, 10), pady=5)


        self.brokenSensorEntry = tk.CTkEntry(master=self, placeholder_text=f"Broken Sensor: {Globals.SensorDelay}s", height=40, font=("Helvetica", 20))
        self.brokenSensorEntry.grid(row=5, column=0, padx=(10, 5), pady=5)

        self.brokenSensorBtn = tk.CTkButton(master=self, text="Select Value", command=self.BrokenSensorDetection, height=40, font=("Helvetica", 20))
        self.brokenSensorBtn.grid(row=5, column=1, padx=(5, 10), pady=5)

