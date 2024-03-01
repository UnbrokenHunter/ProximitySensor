import Globals
import time

def GetDistanceDriven():
    trackLength = 0.4 # 0.4km
    return Globals.LapCount * trackLength
        
def GetLapCount():
    return Globals.LapCount
                
def GetLastLapTime():
    return Globals.LastLapTime
        
def GetAverageLapTime():
    return GetLapCount() / (time.time() - Globals.StartTime)
        
def GetCurrentDriver():
    return Globals.CurrentDriver

print("Stats Initalized")