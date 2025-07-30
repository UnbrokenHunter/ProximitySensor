import time
import threading

from . import Globals
from .sensors import Camera
from .sensors import SensorEmulator
from .sheets import Sheets
from .sheets import LocalSheets

previousValue = False
lapStartTime = time.time()
speedTrackerTimer = 0
timeSinceLastFalse = 0

def SaveLap():
    global lapStartTime
    global speedTrackerTimer
    global timeSinceLastFalse

    # Lap Count Is Calculated Based on Spreadsheet Row 

    # If __ then Lap is probably not accurate
    if Globals.CurrentLapTime < Globals.MinLapTime and Globals.LapFilters == True:
        print(f"Lap with time of {Globals.FormatTime(Globals.CurrentLapTime)} likely fraudulent. It has been disqualified.")
        return
    
    if timeSinceLastFalse > Globals.TimeSinceLastFalseThreshold and Globals.LapFilters == True:
        print(f"There has been {timeSinceLastFalse} true reading in a row. This is likely fraudulent. Nothing will be saved. \nPlease Check Sensor!")
        return

    Globals.LastLapTime = Globals.CurrentLapTime

    t1 = threading.Thread(target=SaveToSheets, daemon=True)
    t1.start()

    lapStartTime = time.time()

def SaveToSheets():
    # Calculate Instant Speed
    InstantSpeed = (time.time() - speedTrackerTimer)

    localMin = LocalSheets.find_first_empty_cell_in_column("Sheet1")
    try:
        sheetsMin = Sheets.find_first_empty_cell_in_column("Sheet1")
        Sheets.SaveData(sheetsMin, Globals.LastLapTime, InstantSpeed)
    except Exception as err:
        Globals.LapCount += 1 # Update Lap Count Because Digital save is unreachable
        print("Error Saving Sheet Data")

    # Always Update Local Save
    LocalSheets.SaveData(localMin, Globals.LastLapTime, InstantSpeed)


def SensorData(value):
    if (Globals.EnableLogging == True):
        print(value)

    if (Globals.TrackingEnabled == True):

        global previousValue
        global lapStartTime
        global speedTrackerTimer
        global timeSinceLastFalse

        if value == True:
            timeSinceLastFalse += 1
        else:
            timeSinceLastFalse = 0

        # Calculate Lap Time
        Globals.CurrentLapTime = (time.time() - lapStartTime)

        # If was not active and now is (Entered Sensor)
        if value != previousValue and previousValue == False:
            speedTrackerTimer = time.time()

        # If was active and now is not (Exited Sensor)
        if value != previousValue and previousValue == True:
            SaveLap()

        previousValue = value

        # time.sleep(Globals.SensorDelay)

def StartSensor():
    if Globals.SensorThread and Globals.SensorThread.is_alive():
        print("Sensor thread already running.")
        return

    if Globals.Mode == "Camera":
        Globals.SensorStopEvent.clear()
        Globals.SensorThread = threading.Thread(target=Camera.DetectionLoop, daemon=True)
        Globals.SensorThread.start()

    elif Globals.Mode == "Sensor Emulator":
        Globals.SensorStopEvent.clear()
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
