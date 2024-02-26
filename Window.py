import customtkinter as tk
import Statistics as Stats

class ButtonFrame(tk.CTkFrame):
    def EnableTracking(self):
        print("Enable Tracking")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title = tk.CTkLabel(master=self, text="Lap Tracker", font=("Helvetica", 50))
        self.title.grid(row=0, column=0, padx=(10, 10), pady=20, sticky="ew")

        self.enableTracking = tk.CTkButton(master=self, text="Enable Tracking", command=self.EnableTracking, height=50, font=("Helvetica", 20))
        self.enableTracking.grid(row=1, column=0, padx=(10, 10), pady=30, sticky="ew")

class DataFrame(tk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Lap Count
        self.lapCountLabel = tk.CTkLabel(master=self, text="Lap Count:", font=("Helvetica", 20))
        self.lapCountLabel.grid(row=0, column=0, padx=(20, 3), pady=20, sticky="ew")

        self.lapCount = tk.CTkLabel(master=self, text="No Laps", font=("Helvetica", 20))
        self.lapCount.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="ew")

        # Distance Driven
        self.distanceDrivenLabel = tk.CTkLabel(master=self, text="Distance Driven:", font=("Helvetica", 20))
        self.distanceDrivenLabel.grid(row=1, column=0, padx=(20, 3), pady=20, sticky="ew")

        self.distanceDriven = tk.CTkLabel(master=self, text="No Laps", font=("Helvetica", 20))
        self.distanceDriven.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="ew")

        # Last Lap Time
        self.lastLapTimeLabel = tk.CTkLabel(master=self, text="Last Lap:", font=("Helvetica", 20))
        self.lastLapTimeLabel.grid(row=2, column=0, padx=(20, 3), pady=20, sticky="ew")

        self.lastLapTime = tk.CTkLabel(master=self, text="No Laps", font=("Helvetica", 20))
        self.lastLapTime.grid(row=2, column=1, padx=(10, 20), pady=20, sticky="ew")

        # Average Lap Time
        self.averageLapTimeLabel = tk.CTkLabel(master=self, text="Average Lap:", font=("Helvetica", 20))
        self.averageLapTimeLabel.grid(row=3, column=0, padx=(20, 3), pady=20, sticky="ew")

        self.averageLapTime = tk.CTkLabel(master=self, text="No Laps", font=("Helvetica", 20))
        self.averageLapTime.grid(row=3, column=1, padx=(10, 20), pady=20, sticky="ew")

        def Update():
            self.lapCount.configure(text=Stats.GetLapCount())
            self.distanceDrivenLabel.configure(text=Stats.GetDistanceDriven())
            self.lastLapTime.configure(text=Stats.GetLastLapTime())
            self.averageLapTime.configure(text=Stats.GetAverageLapTime())

        self.update = tk.CTkButton(master=self, text="Update", command=Update, height=50, font=("Helvetica", 20))
        self.update.grid(row=4, column=0, padx=(10, 10), pady=30, sticky="ew")


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        tk.set_appearance_mode("System")  # Modes: system (default), light, dark
        tk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.geometry("800x500")

        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.frame = ButtonFrame(master=self)
        self.frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        self.frame = DataFrame(master=self)
        self.frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

app = App()
app.mainloop()
