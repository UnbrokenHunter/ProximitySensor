import Globals
import time
import ProccessSensorData
import threading
try:
    from gpiozero import MotionSensor
except ModuleNotFoundError as err:
    print("GPIOZero Not Found")

def ReadData(pir):
    while True:
        if Globals.Mode == "Motion Sensor":
            try:
                # Read the sensor output
                value = pir.motion_detected
                print("Motion: ", value)
                ProccessSensorData.SensorData(value)
            except Exception as e:
                print(f"An error occurred: {e}")
                # Handle or log the error appropriately
        else:
            return  # Exit the loop if the mode is not "Motion Sensor"
      
def Run():  
    if Globals.Mode == "Motion Sensor":
        try:
            pir = MotionSensor(4)  # Define pin as needed
            t1 = threading.Thread(target=ReadData, args=(pir,), daemon=True)
            t1.start()
        except Exception as e:
            print(f"Failed to start motion sensor thread: {e}")
            # Handle or log the error appropriately
