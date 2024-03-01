import time
import threading
import random 
import ProccessSensorData

def ReadData():

    trackPosition = 0
    trackLength = 400

    while True:

        trackPosition += random.random() * 1.5

        trackPosition = trackPosition % trackLength

        # Read the sensor output
        value = trackPosition > 398

        # if value:
        #      print("No object detected")
        # else:
        #     print("Object detected")

        ProccessSensorData.SensorData(value)

        time.sleep(0.05)  # Delay for half a second
    

t1 = threading.Thread(target=ReadData)
t1.start()

