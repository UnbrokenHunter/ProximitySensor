import time

def FormatTime(time):
    # Extract whole seconds and milliseconds
    seconds = int(time)
    milliseconds = int((time - seconds) * 1000)
    
    # Compute hours, minutes, and seconds
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    # Return formatted time string including milliseconds
    return "%d:%02d:%02d.%03d" % (hour, minutes, seconds, milliseconds)

TrackingEnabled = True
LapFilters = True
MinLapTime = 10

CurrentDriver = "None"
Drivers = ["Mac", "Mitchell", "Josh", "Hunter", "John Walter"]
LapCount = 0
LastLapTime = 0

DebugMode = False
Simulated = False

# Statics
StartTime = time.time()
CarLength = 0.2 # Meters
TrackLength = 0.4 # 0.4km
RecordRequirement = 825055 # Meters
