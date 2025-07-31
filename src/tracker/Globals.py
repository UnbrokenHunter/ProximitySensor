import time
import threading

SensorStopEvent = threading.Event()
SensorThread = None  # To store a reference to the running thread

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
CurrentLapTime = 0
OfflineLaps = []  # List of lap times not yet saved to Google Sheets

# Statics
CarLength = 0.2 # Meters
TrackLength = 400 # 400m
RecordRequirement = 825055 # Meters

# Debug
Mode = "Camera"
UIDelay = 0.5
EmulateGoogleSheetsFailure = False

# ===============================
# VIDEO SOURCE CONFIGURATION
# ===============================

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ===============================
# PREDICTION PARAMETERS
# ===============================

CONFIDENCE_THRESHOLD = 0.1
IOU_THRESHOLD = 0.8
IMAGE_SIZE = 416

SHOW_VIDEO = True  # Set to False to disable OpenCV window
