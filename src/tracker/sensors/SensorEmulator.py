import threading
import random 

from .. import ProccessSensorData
from .. import Globals

def ReadData():
    print("Sensor Emulator Being Initialized")

    trackPosition = 0
    trackLength = 20

    while True:
        if Globals.Mode == "Sensor Emulator" and not Globals.SensorStopEvent.is_set():
            trackPosition += random.random() * 1.5

            trackPosition = trackPosition % trackLength

            # Read the sensor output
            value = trackPosition > trackLength - 4

            ProccessSensorData.SensorData(value)

        else:
            return        
