import time

from . import Globals
from .sheets import LocalSheets

def GetDistanceDriven():
    return GetLapCount() * Globals.TrackLength
        
def GetLapCount():
    return LocalSheets.find_first_empty_cell_in_column() - 1
                
def GetLastLapTime():
    return LocalSheets.read_cell(LocalSheets.find_first_empty_cell_in_column() - 1, 'B')
        
def GetAverageLapTime():
    if GetLapCount() == 0:
        return (time.time() - Globals.StartTime)
    else:
        return (time.time() - Globals.StartTime) / GetLapCount()
        
def GetCurrentDriver():
    return Globals.CurrentDriver

def GetProjectedEndTime():
    distanceToGo = Globals.RecordRequirement - GetDistanceDriven()
    lapsToGo = distanceToGo / Globals.TrackLength
    projectedTime = lapsToGo * GetAverageLapTime()
    return projectedTime

print("Stats Initalized")