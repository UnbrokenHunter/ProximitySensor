import time
import threading
import random 
import ProccessSensorData

def ReadData():
    while True:
        # Read the sensor output
        value = random.randint(0, 10000) < 9900

        # if value:
        #      print("No object detected")
        # else:
        #     print("Object detected")

        ProccessSensorData.SensorData(value)

        time.sleep(0.05)  # Delay for half a second
    

t1 = threading.Thread(target=ReadData)
t1.start()

