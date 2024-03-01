import RPi.GPIO as GPIO
import time
import threading
import ProccessSensorData

def ReadData():
    # Set the GPIO mode
    GPIO.setmode(GPIO.BCM)

    # Replace 4 with the GPIO pin number you've connected your sensor to
    pin = 4

    # Set up the GPIO pin as an input
    GPIO.setup(pin, GPIO.IN)

    while True:
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

t1 = threading.Thread(target=ReadData)
t1.start()

