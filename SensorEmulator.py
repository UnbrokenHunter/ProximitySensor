import time
import threading
import random 
import ProccessSensorData
import Globals

def ReadData():
    trackPosition = 0
    trackLength = 400

    while True:
        if (Globals.Simulated):
            print("Emulator")

            trackPosition += random.random() * 1.5

            trackPosition = trackPosition % trackLength

            # Read the sensor output
            value = trackPosition > trackLength - 2

            ProccessSensorData.SensorData(value)

            time.sleep(Globals.SensorDelay)  # Delay for half a second
        else:
            return        

def Run():
    if (Globals.Simulated):
        t1 = threading.Thread(target=ReadData, daemon=True)
        t1.start()

