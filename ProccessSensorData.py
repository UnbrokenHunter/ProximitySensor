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
    Globals.LastLapTime = (time.time() - lapStartTime)

    # Calculate Instant Speed
    InstantSpeed = (time.time() - speedTrackerTimer)

    try:
        Sheets.SaveData(Globals.LastLapTime, InstantSpeed)
    except Exception as err:
        print("Error Saving Sheet Data")
        #print(f"There was an error saving the data to a sheet.\nThe Last Lap was {Globals.LastLapTime}\n Instant Speed: {InstantSpeed}")

        # Update Lap Count Because Digital save is unreachable
        Globals.LapCount += 1

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


def Test():
    # Tests
    for x in range(100):
        value = x % 10 == 0
        SensorData(value)
        time.sleep(0.1)  # Delay for half a second
