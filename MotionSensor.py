from gpiozero import MotionSensor
import Globals
import time
import ProccessSensorData
import threading

pir = None

def ReadData():
    global pir

    while True:
        global localPin
        pir = MotionSensor(4)

        if Globals.Mode == "Motion Sensor":
            # Read the sensor output
            value = pir.motion_detected
            pir.wait_for_motion()

            ProccessSensorData.SensorData(value)
        else:
            return        
      
def Run():  
    if not Globals.Simulated:
        t1 = threading.Thread(target=ReadData, daemon=True)
        t1.start()
