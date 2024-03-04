import time
import threading
import ProccessSensorData
import Globals
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError as err:
    print("RPi Module not found") 

localPin = 4

# Set up the GPIO pin as an input
def SetupPin(pin):
    GPIO.setup(pin, GPIO.IN)

def ReadData():
    try:
        # Set the GPIO mode
        GPIO.setmode(GPIO.BCM)

        SetupPin(Globals.Pin)
    except NameError as err:
        print("name 'GPIO' is not defined NameError") 

    while True:
        global localPin
        if not Globals.Simulated:
            print("Sensor")
            try:
                if localPin != Globals.Pin:
                    SetupPin(Globals.Pin)

                # Read the sensor output
                value = GPIO.input(Globals.Pin)

                ProccessSensorData.SensorData(value)

                time.sleep(Globals.SensorDelay)  # Delay for half a second   
                 
            finally:
                GPIO.cleanup()
        else:
            return        
      
def Run():  
    if not Globals.Simulated:
        t1 = threading.Thread(target=ReadData, daemon=True)
        t1.start()
