import time
import Globals
import Sheets
import LocalSheets

previousValue = False
lapStartTime = time.time()
speedTrackerTimer = 0

def SaveLap():
    global lapStartTime
    global speedTrackerTimer

    # Lap Count Is Calculated Based on Spreadsheet Row 

    # Calculate Lap Time
    lapTime = (time.time() - lapStartTime)

    # If __ then Lap is probably not accurate
    if lapTime < Globals.MinLapTime:
        print(f"Lap with time of {Globals.FormatTime(lapTime)} likely fraudulent. It has been disqualified.")
        return

    Globals.LastLapTime = lapTime

    # Calculate Instant Speed
    InstantSpeed = (time.time() - speedTrackerTimer)

    try:
        Sheets.SaveData(Globals.LastLapTime, InstantSpeed)
    except Exception as err:
        Globals.LapCount += 1 # Update Lap Count Because Digital save is unreachable
        print("Error Saving Sheet Data")

    # Always Update Local Save
    LocalSheets.SaveData(Globals.LastLapTime, InstantSpeed)

    lapStartTime = time.time()

def SensorData(value):
    if (Globals.TrackingEnabled == True):

        global previousValue
        global lapStartTime
        global speedTrackerTimer

        # If was not active and now is (Entered Sensor)
        if value != previousValue and previousValue == False:
            speedTrackerTimer = time.time()

        # If was active and now is not (Exited Sensor)
        if value != previousValue and previousValue == True:
            SaveLap()

        previousValue = value

        time.sleep(Globals.SensorDelay)
