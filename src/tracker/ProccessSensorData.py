import time
import threading
import json
import os

from . import Globals
from . import Statistics
from . import StartAttempt
from .utils import TimeUtils
from .utils.event_bus import event_bus
from .sensors import Camera
from .sensors import SensorEmulator
from .sheets import GoogleSheets
from .sheets import LocalSheets

previousValue = False
lapStartTime = time.time()
speedTrackerTimer = 0
timeSinceLastFalse = 0

OFFLINE_PATH = "offline_laps.json"

def SaveLap():
    global lapStartTime
    global speedTrackerTimer
    global timeSinceLastFalse

    if Globals.CurrentLapTime < Globals.MinLapTime and Globals.LapFilters:
        print(f"Lap with time of {TimeUtils.FormatTime(Globals.CurrentLapTime)} likely fraudulent. It has been disqualified.")
        return

    if timeSinceLastFalse > Globals.TimeSinceLastFalseThreshold and Globals.LapFilters:
        print(f"{timeSinceLastFalse} true readings in a row. Likely fraudulent. Lap skipped.")
        return

    threading.Thread(target=SaveToGoogleSheets, daemon=True).start()
    lapStartTime = time.time()

def SaveToGoogleSheets():
    info = {
        "lap_time": Globals.CurrentLapTime,
        "lap_count": Statistics.GetLapCount(),
        "driver": Globals.CurrentDriver,
        "timestamp": time.time()
    }

    LocalSheets.SaveData(LocalSheets.find_first_empty_cell_in_column(), info["lap_time"])
    event_bus.emit("refresh_recent_laps")

    if Globals.EmulateGoogleSheetsFailure:
        buffer_offline_lap(info)
        print("[EMULATED FAILURE] Pretending Google Sheets is unreachable. Buffered offline.")
        return

    try:
        if Globals.OfflineLaps:
            print(f"Flushing {len(Globals.OfflineLaps)} buffered lap(s)...")
            for cached in Globals.OfflineLaps:
                GoogleSheets.SaveDataManual(
                    GoogleSheets.find_first_empty_cell_in_column("Sheet1"), 
                    cached['lap_count'] + 1, 
                    cached["lap_time"], 
                    cached['driver'], 
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cached['timestamp'])),
                    "Buffered Offline"
                )
                print(f"Recovered Lap {cached['lap_count']} by {cached['driver']} @ {TimeUtils.FormatTime(cached['timestamp'])}")
                
            Globals.OfflineLaps.clear()
            save_offline_laps_to_disk()  # Clear disk backup too

        GoogleSheets.SaveData(GoogleSheets.find_first_empty_cell_in_column("Sheet1"), info["lap_time"])
        print("Saved to Google Sheets:", TimeUtils.FormatTime(info["lap_time"]))


    except Exception as err:
        buffer_offline_lap(info)
        print("Google Sheets unreachable. Saved locally and buffered offline.")

def buffer_offline_lap(lap_info):
    Globals.OfflineLaps.append(lap_info)
    save_offline_laps_to_disk()

def save_offline_laps_to_disk():
    try:
        with open(OFFLINE_PATH, "w") as f:
            json.dump(Globals.OfflineLaps, f)
    except Exception as e:
        print("Failed to save offline buffer:", e)

def load_offline_laps_from_disk():
    if os.path.exists(OFFLINE_PATH):
        try:
            with open(OFFLINE_PATH, "r") as f:
                Globals.OfflineLaps = json.load(f)
            print(f"Loaded {len(Globals.OfflineLaps)} offline lap(s) from disk.")
        except Exception as e:
            print("Failed to load offline laps from disk:", e)

def SensorData(value):
    if Globals.EnableLogging:
        print(value)

    if Globals.TrackingEnabled and StartAttempt.json_exists():
        global previousValue, lapStartTime, speedTrackerTimer, timeSinceLastFalse

        timeSinceLastFalse = timeSinceLastFalse + 1 if value else 0
        Globals.CurrentLapTime = time.time() - lapStartTime

        if value != previousValue:
            if not previousValue:  # rising edge
                speedTrackerTimer = time.time()
            else:  # falling edge
                SaveLap()

        previousValue = value

def StartSensor():
    load_offline_laps_from_disk()

    if Globals.SensorThread and Globals.SensorThread.is_alive():
        print("Sensor thread already running.")
        return

    Globals.SensorStopEvent.clear()

    if Globals.Mode == "Camera":
        Globals.SensorThread = threading.Thread(target=Camera.DetectionLoop, daemon=True)
    elif Globals.Mode == "Sensor Emulator":
        Globals.SensorThread = threading.Thread(target=SensorEmulator.ReadData, daemon=True)

    Globals.SensorThread.start()

def StopSensor():
    Globals.SensorStopEvent.set()
    if Globals.SensorThread:
        Globals.SensorThread.join(timeout=2)
        print("Sensor thread stopped.")
        Globals.SensorThread = None

def RestartSensor():
    StopSensor()
    StartSensor()
