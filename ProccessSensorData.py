import time
import Globals
import Sheets
import LocalSheets

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

    lapStartTime = time.time()

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

        time.sleep(Globals.SensorDelay)
