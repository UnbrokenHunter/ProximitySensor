import time
import threading
import ProccessSensorData
import Globals
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError as err:
    print("RPi Module not found") 

def ReadData():
    pin = 4

    try:
        # Set the GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Set up the GPIO pin as an input
        GPIO.setup(pin, GPIO.IN)
    except NameError as err:
        print("name 'GPIO' is not defined") 

    while True:
        if Globals.Simulated:
            try:
                # Read the sensor output
                value = GPIO.input(pin)

                if value:
                    print("No object detected")
                else:
                    print("Object detected")

                ProccessSensorData.SensorData(value)

                time.sleep(0.1)  # Delay for half a second    
            finally:
                GPIO.cleanup()

t1 = threading.Thread(target=ReadData, daemon=True)
t1.start()

