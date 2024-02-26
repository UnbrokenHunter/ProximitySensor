import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Replace 17 with the GPIO pin number you've connected your sensor to
pin = 4

# Set up the GPIO pin as an input
GPIO.setup(pin, GPIO.IN)

try:
    while True:
        # Read the sensor output
        if GPIO.input(pin):
            print("No object detected")
        else:
            print("Object detected")
        time.sleep(0.5)  # Delay for half a second
finally:
    GPIO.cleanup()
