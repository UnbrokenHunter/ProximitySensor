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
            trackPosition += random.random() * 1.5

            trackPosition = trackPosition % trackLength

            # Read the sensor output
            value = trackPosition > trackLength - 2

            # if value:
            #      print("No object detected")
            # else:
            #     print("Object detected")

            ProccessSensorData.SensorData(value)

            time.sleep(0.05)  # Delay for half a second
    

t1 = threading.Thread(target=ReadData, daemon=True)
t1.start()

