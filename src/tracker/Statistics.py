import time

from . import Globals
from . import StartAttempt
from .sheets import LocalSheets

def GetDistanceDriven():
    return GetLapCount() * Globals.TrackLength
        
def GetLapCount():
    return LocalSheets.find_first_empty_cell_in_column() - 1
                
def GetLastLapTime():
    return LocalSheets.read_cell(LocalSheets.find_first_empty_cell_in_column() - 1, 'B')
        
def GetAverageLapTime():
    if not StartAttempt.json_exists():
        return 0
    
    if GetLapCount() == 0:
        return GetCurrentTime()
    else:
        return GetCurrentTime() / GetLapCount()

def GetCurrentTime():
    if not StartAttempt.json_exists():
        return 0
    
    return time.time() - StartAttempt.read_timestamp_json()["created"]
        
def GetCurrentDriver():
    return Globals.CurrentDriver

def GetProjectedEndTime():
    distanceToGo = Globals.RecordRequirement - GetDistanceDriven()
    lapsToGo = distanceToGo / Globals.TrackLength
    projectedTime = lapsToGo * GetAverageLapTime()
    return projectedTime

def GetProjectedRecordMargin():
    total_time = GetProjectedEndTime() + GetCurrentTime()
    target_time = 24 * 60 * 60  # 24 hours in seconds
    margin = target_time - total_time  # Positive = time left, Negative = over time
    return margin

print("Stats Initalized")