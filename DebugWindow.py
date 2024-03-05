import customtkinter as tk
import Globals
import Sensor
import SensorEmulator

class Frame(tk.CTkFrame):  
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.CreateUI()

    def Simulated(self):
        Globals.Simulated = not Globals.Simulated
        print("Simulated: ", Globals.Simulated)

        SensorEmulator.Run()
        Sensor.Run()

    def Pin(self):
        Globals.Pin = int(self.pinEntry.get())
        print("Pin: ", Globals.Pin)

    def Delay(self):
        Globals.SensorDelay = float(self.delayEntry.get())
        print("Delay: ", Globals.SensorDelay)

    def CreateUI(self):
        self.titleFrame = tk.CTkFrame(master=self)
        # Use columnspan=2 to make the titleFrame span across both columns
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=7, sticky="ew")

        self.title = tk.CTkLabel(master=self.titleFrame, text="Debug:", justify="left", anchor="w",font=("Helvetica", 40, "italic", "normal"))
        self.title.pack(padx=(10, 40), pady=10, fill="x")

        self.simulated = tk.CTkCheckBox(master=self, text="Simulate Sensor Data", command=self.Simulated, height=50, font=("Helvetica", 20))
        self.simulated.deselect()
        self.simulated.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.pinEntry = tk.CTkEntry(master=self, placeholder_text="Pin", height=40, font=("Helvetica", 20))
        self.pinEntry.grid(row=2, column=0, padx=(10, 5), pady=5)

        self.pinButton = tk.CTkButton(master=self, text="Select Pin", command=self.Pin, height=40, font=("Helvetica", 20))
        self.pinButton.grid(row=2, column=1, padx=(5, 10), pady=5)

        self.delayEntry = tk.CTkEntry(master=self, placeholder_text=f"Delay: {Globals.SensorDelay}s", height=40, font=("Helvetica", 20))
        self.delayEntry.grid(row=3, column=0, padx=(10, 5), pady=5)

        # Adjusted the placement of the delayButton to row 3, column 1
        self.delayButton = tk.CTkButton(master=self, text="Select Delay", command=self.Delay, height=40, font=("Helvetica", 20))
        self.delayButton.grid(row=3, column=1, padx=(5, 10), pady=5)
