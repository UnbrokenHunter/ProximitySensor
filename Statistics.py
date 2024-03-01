import Globals
import time

def GetDistanceDriven():
    return Globals.LapCount * Globals.TrackLength
        
def GetLapCount():
    return Globals.LapCount
                
def GetLastLapTime():
    return Globals.LastLapTime
        
def GetAverageLapTime():
    if GetLapCount() == 0:
        return (time.time() - Globals.StartTime)
    else:
        return (time.time() - Globals.StartTime) / GetLapCount()
        
def GetCurrentDriver():
    return Globals.CurrentDriver

def GetProjectedEndTime():
    distanceToGo = Globals.RecordRequirement - GetDistanceDriven()
    lapsToGo = distanceToGo / (Globals.TrackLength * 1000) # km to meters
    projectedTime = lapsToGo * GetAverageLapTime()
    return projectedTime

print("Stats Initalized")