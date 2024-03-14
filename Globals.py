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
    
TrackingEnabled = False
LapFilters = True
MinLapTime = 10
TimeSinceLastFalseThreshold = 80

EnableLogging = False

CurrentDriver = "None"
Drivers = ["Mac", "Mitchell", "Josh", "Hunter", "John Walter", 
           "Sam", "Reid", "Jack", "Elijah", "Liam", "Mr. Lipp", 
           "Andy", "Luke B", "Truman B", "Andrew C", "Haolin C", "Ben F", "Alex G", 
           "Ciarán G", "Mason H", "Frtiz H", "Tucker H", 
           "Vincent H", "Cooper H", "Tristan J", "Nathaniel J", 
           "Reese J", "Eli K", "Garrett L", "Powers M", 
           "Immanuel N", "Alec N", "Krish P", "Carson P", 
           "Martin R", "Nathan S", "Gabriel S", "Marc W", "Other"]
LapCount = 0
CurrentLapTime = 0
LastLapTime = 0

# Statics
StartTime = time.time()
RealStart = False # Has Enable Tracking Been Enabled Before
CarLength = 0.2 # Meters
TrackLength = 0.4 # 0.4km
RecordRequirement = 825055 # Meters

# Debug
Mode = "Sensor"
Pin = 4
SensorDelay = 0.1
ControlsLapCount = "Local"
