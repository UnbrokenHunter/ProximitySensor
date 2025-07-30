import time

TrackingEnabled = False
LapFilters = True
MinLapTime = 10
TimeSinceLastFalseThreshold = 80

EnableLogging = False

CurrentDriver = "None"

Drivers = ["Mac Spear", "Mitchell Wolken", "Josh Wagner", 
           "Sam Gallivan", "Reid Martin", "Elijah Butcher", 
           "Ciarán Greer", "Nathan Salamin", "Chris Lipp",
           "Hunter Frederick", "John Walter Whisenhunt", 
           "Other"]
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
