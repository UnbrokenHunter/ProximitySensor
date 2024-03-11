import threading
import ProccessSensorData
import Globals
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError as err:
    print("GPIO Not Found")

localPin = -1

# Set up the GPIO pin as an input
def SetupPin(pin):
    global localPin 
    localPin = pin
    GPIO.setup(pin, GPIO.IN)

def ReadData():
    # Set the GPIO mode
    GPIO.setmode(GPIO.BCM)

    while True:
        global localPin

        if Globals.Mode == "Sensor":
            try:
                if localPin != Globals.Pin:
                    SetupPin(Globals.Pin)

                # Read the sensor output
                value = GPIO.input(Globals.Pin)

                ProccessSensorData.SensorData(value)
                 
            finally:
                GPIO.cleanup()
        else:
            return        
      
def Run():  
    if not Globals.Simulated:
        t1 = threading.Thread(target=ReadData, daemon=True)
        t1.start()
