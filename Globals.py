import time

def FormatTime(time):
    # Extract whole seconds and milliseconds
    seconds = int(time)
    milliseconds = int((time - seconds) * 1000)

    # Compute Days
    days = seconds // (24 * 3600)
    
    # Compute hours, minutes, and seconds
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    # Return including days
    if days != 0:
        return "%d:%d:%02d:%02d.%03d" % (days, hour, minutes, seconds, milliseconds)
    
    # Return including hours
    elif hour != 0:
        return "%d:%02d:%02d.%03d" % (hour, minutes, seconds, milliseconds)
    
    # Return including hours
    else:
        return "%02d:%02d.%03d" % (minutes, seconds, milliseconds)
    
TrackingEnabled = True
LapFilters = True
MinLapTime = 10

CurrentDriver = "None"
Drivers = ["Mac", "Mitchell", "Josh", "Hunter", "John Walter"]
LapCount = 0
CurrentLapTime = 0
LastLapTime = 0

# Statics
StartTime = time.time()
CarLength = 0.2 # Meters
TrackLength = 0.4 # 0.4km
RecordRequirement = 825055 # Meters

# Debug
Simulated = False
Pin = 4
SensorDelay = 0.1
