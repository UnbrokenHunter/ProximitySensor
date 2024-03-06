import threading
import random 
import ProccessSensorData
import Globals

def ReadData():
    trackPosition = 0
    trackLength = 20

    while True:
        if (Globals.Simulated):
            trackPosition += random.random() * 1.5

            trackPosition = trackPosition % trackLength

            # Read the sensor output
            value = trackPosition > trackLength - 4

            ProccessSensorData.SensorData(value)

        else:
            return        

def Run():
    if (Globals.Simulated):
        t1 = threading.Thread(target=ReadData, daemon=True)
        t1.start()

