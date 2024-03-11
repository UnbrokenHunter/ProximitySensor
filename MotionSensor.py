import Globals
import time
import ProccessSensorData
import threading
try:
    from gpiozero import MotionSensor
except ModuleNotFoundError as err:
    print("GPIOZero Not Found")

def ReadData():
    while True:
        global localPin
        pir = MotionSensor(4)

        if Globals.Mode == "Motion Sensor":
            # Read the sensor output
            value = pir.motion_detected
            print ("Motion: ", value)
            ProccessSensorData.SensorData(value)
        else:
            return        
      
def Run():  
    if Globals.Mode == "Motion Sensor":
        t1 = threading.Thread(target=ReadData, daemon=True)
        t1.start()
