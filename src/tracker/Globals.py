import time

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
ManualTimeSet = False # Has Enable Tracking Been Enabled Before
CarLength = 0.2 # Meters
TrackLength = 0.4 # 0.4km
RecordRequirement = 825055 # Meters

# Debug
Mode = "Camera"
UIDelay = 0.5
SensorDelay = 0.1
ControlsLapCount = "Local"
