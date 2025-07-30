import os
import customtkinter as tk

from .. import Globals
from ..sensors import SensorEmulator, Camera
from ..sheets import GoogleSheets


class Frame(tk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        self.titleFrame = tk.CTkFrame(master=self, fg_color="#1F6AA5")
        self.titleFrame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="nsew")

        self.title = tk.CTkLabel(
            master=self.titleFrame,
            text="Debug:",
            justify="left",
            anchor="w",
            font=("Helvetica", 40, "italic", "normal")
        )
        self.title.pack(side="left", padx=10, pady=7)

        self.build_general()
        self.build_filters()
        self.build_camera()
        
        # Set your file names here
        self.file1 = "offline_laps.json"
        self.file2 = "sheets_backup.xlsx"

        reset_btn = tk.CTkButton(
            master=self,
            text="Reset System",
            command=self.reset_everything,
            font=("Helvetica", 20),
            fg_color="red",
            hover_color="#880000"
        )
        reset_btn.grid(row=999, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


    def build_general(self):
        self.general = tk.CTkFrame(master=self, fg_color="#2A2A2A")
        self.general.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")
        self.general.grid_columnconfigure(0, weight=1)
        self.general.grid_columnconfigure(1, weight=1)

        tk.CTkLabel(
            master=self.general,
            text="General Settings",
            font=("Helvetica", 24, "italic")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        self.mode = tk.CTkComboBox(
            master=self.general,
            values=["Camera", "Sensor Emulator"],
            command=lambda choice: (
                setattr(Globals, "Mode", choice),
                print("Mode:", choice),
                SensorEmulator.Run() if choice == "Sensor Emulator" else Camera.Run()
            )
        )
        self.mode.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.mode.set(Globals.Mode)
        
        self.controlsLaps = tk.CTkComboBox(
            master=self.general,
            values=["Local", "Google"],
            command=lambda choice: (
                setattr(Globals, "ControlsLapCount", choice),
                print("Controls Lap Count:", choice)
            )
        )
        self.controlsLaps.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.controlsLaps.set(Globals.ControlsLapCount)

        self.enableLoggingCheck = tk.CTkCheckBox(
            master=self.general,
            text="Enable Logging",
            command=lambda: (
                setattr(Globals, "EnableLogging", self.enableLoggingCheck.get() == 1),
                print("Enable Logging:", Globals.EnableLogging)
            ),
            height=40,
            font=("Helvetica", 20)
        )
        self.enableLoggingCheck.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.enableLoggingCheck.select() if Globals.EnableLogging else self.enableLoggingCheck.deselect()

        self.emulateGoogleSheetsFailure = tk.CTkCheckBox(
            master=self.general,
            text="Sheets Failure",
            command=lambda: (
                setattr(Globals, "EmulateGoogleSheetsFailure", self.emulateGoogleSheetsFailure.get() == 1),
                print("Enable Sheets Failure:", Globals.EmulateGoogleSheetsFailure)
            ),
            height=40,
            font=("Helvetica", 20)
        )
        self.emulateGoogleSheetsFailure.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.emulateGoogleSheetsFailure.select() if Globals.EmulateGoogleSheetsFailure else self.emulateGoogleSheetsFailure.deselect()


    def build_filters(self):
        self.filters = tk.CTkFrame(master=self, fg_color="#2F2F2F")
        self.filters.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.filters.grid_columnconfigure(0, weight=1)
        self.filters.grid_columnconfigure(1, weight=1)

        tk.CTkLabel(
            master=self.filters,
            text="Filters",
            font=("Helvetica", 24, "italic")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        self.minLapTimeEntry = tk.CTkEntry(
            master=self.filters,
            placeholder_text=f"Min Lap: {Globals.MinLapTime}s",
            height=40,
            font=("Helvetica", 20)
        )
        self.minLapTimeEntry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.minLapTimeEntry.bind("<FocusOut>", lambda e: self.apply_min_lap_time())
        self.minLapTimeEntry.bind("<Return>", lambda e: self.apply_min_lap_time())

        self.brokenSensorEntry = tk.CTkEntry(
            master=self.filters,
            placeholder_text=f"Broken Sensor: {Globals.TimeSinceLastFalseThreshold}s",
            height=40,
            font=("Helvetica", 20)
        )
        self.brokenSensorEntry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.brokenSensorEntry.bind("<FocusOut>", lambda e: self.apply_broken_sensor())
        self.brokenSensorEntry.bind("<Return>", lambda e: self.apply_broken_sensor())

    def build_camera(self):
        self.camera = tk.CTkFrame(master=self, fg_color="#2B2B2B")
        self.camera.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")
        self.camera.grid_columnconfigure(0, weight=1)
        self.camera.grid_columnconfigure(1, weight=1)

        tk.CTkLabel(
            master=self.camera,
            text="Camera Settings",
            font=("Helvetica", 24, "italic")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        # === Image Size Dropdown ===
        tk.CTkLabel(master=self.camera, text="Image Size:", font=("Helvetica", 18)).grid(
            row=1, column=0, sticky="w", padx=10, pady=5
        )

        image_sizes = ["320", "416", "640", "960", "1280", "1920"]
        self.imageSizeDropdown = tk.CTkComboBox(
            master=self.camera,
            values=image_sizes,
            command=lambda v: (
                setattr(Globals, "IMAGE_SIZE", int(v)),
                print("Image Size:", Globals.IMAGE_SIZE)
            )
        )
        self.imageSizeDropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.imageSizeDropdown.set(str(Globals.IMAGE_SIZE))

        # === Frame Size Dropdown ===
        tk.CTkLabel(master=self.camera, text="Frame Size:", font=("Helvetica", 18)).grid(
            row=2, column=0, sticky="w", padx=10, pady=5
        )

        frame_sizes = {
            "320x240": (320, 240),
            "640x480": (640, 480),
            "800x600": (800, 600),
            "1280x720": (1280, 720),
            "1920x1080": (1920, 1080)
        }
        self.frameSizeDropdown = tk.CTkComboBox(
            master=self.camera,
            values=list(frame_sizes.keys()),
            command=lambda choice: (
                setattr(Globals, "FRAME_WIDTH", frame_sizes[choice][0]),
                setattr(Globals, "FRAME_HEIGHT", frame_sizes[choice][1]),
                print("Frame Size:", frame_sizes[choice])
            )
        )
        self.frameSizeDropdown.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.frameSizeDropdown.set(f"{Globals.FRAME_WIDTH}x{Globals.FRAME_HEIGHT}")

        # === Confidence Threshold Entry ===
        self.confThresholdEntry = tk.CTkEntry(
            master=self.camera,
            placeholder_text=f"Confidence Threshold (0–1): {Globals.CONFIDENCE_THRESHOLD}",
            height=40,
            font=("Helvetica", 20)
        )
        self.confThresholdEntry.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.confThresholdEntry.bind("<FocusOut>", lambda e: self.apply_clamped_entry(
            self.confThresholdEntry, "CONFIDENCE_THRESHOLD", 0.0, 1.0))
        self.confThresholdEntry.bind("<Return>", lambda e: self.apply_clamped_entry(
            self.confThresholdEntry, "CONFIDENCE_THRESHOLD", 0.0, 1.0))

        # === IoU Threshold Entry ===
        self.iouThresholdEntry = tk.CTkEntry(
            master=self.camera,
            placeholder_text=f"IoU Threshold (0–1): {Globals.IOU_THRESHOLD}",
            height=40,
            font=("Helvetica", 20)
        )
        self.iouThresholdEntry.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.iouThresholdEntry.bind("<FocusOut>", lambda e: self.apply_clamped_entry(
            self.iouThresholdEntry, "IOU_THRESHOLD", 0.0, 1.0))
        self.iouThresholdEntry.bind("<Return>", lambda e: self.apply_clamped_entry(
            self.iouThresholdEntry, "IOU_THRESHOLD", 0.0, 1.0))

        # === Show Video Checkbox ===
        self.showVideoCheck = tk.CTkCheckBox(
            master=self.camera,
            text="Show Video",
            command=lambda: (
                setattr(Globals, "SHOW_VIDEO", self.showVideoCheck.get() == 1),
                print("Show Video:", Globals.SHOW_VIDEO)
            ),
            height=40,
            font=("Helvetica", 20)
        )
        self.showVideoCheck.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.showVideoCheck.select() if Globals.SHOW_VIDEO else self.showVideoCheck.deselect()

    def reset_everything(self):
        # --- Delete files ---
        for path in [self.file1, self.file2]:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"Deleted file: {path}")
                else:
                    print(f"File not found: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")

        # --- Clear Google Sheet ---
        try:
            GoogleSheets.clear_sheet("Sheet1")
            print("Google Sheet cleared successfully.")
        except Exception as e:
            print("Failed to clear Google Sheet:", e)


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

def apply_clamped_entry(self, entry_widget, global_key, min_val, max_val):
    text = entry_widget.get().strip()
    if not text:
        return
    try:
        val = float(text)
        val = max(min_val, min(max_val, val))  # clamp between min_val and max_val
        setattr(Globals, global_key, val)
        print(f"{global_key}:", val)
    except ValueError:
        print(f"Invalid value for {global_key}: '{text}'")
