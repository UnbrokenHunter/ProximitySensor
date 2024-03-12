import threading
import ProccessSensorData
import Globals
try:
    import RPi.GPIO as GPIO
    # Initialize GPIO mode outside the function to avoid resetting it unnecessarily
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError as err:
    print("GPIO Not Found")

# Set up the GPIO pin as an input
def SetupPin(pin):
    """Set up the GPIO pin as an input"""
    GPIO.setup(pin, GPIO.IN)

def ReadData():
    """Read data from the sensor and process it"""
    current_pin = None  # Track the current pin setup to avoid unnecessary calls to setup_pin
    
    while Globals.Mode == "Sensor":  # Use the Globals.Mode to control the loop
        if current_pin != Globals.Pin:
            SetupPin(Globals.Pin)
            current_pin = Globals.Pin  # Update current_pin after setting up
        
        # Read the sensor output
        value = GPIO.input(Globals.Pin)
        ProccessSensorData.SensorData(value)
                 
    # Clean up GPIO once the loop is exited
    GPIO.cleanup()
          
def Run():  
    if Globals.Mode == "Sensor":
        t1 = threading.Thread(target=ReadData, daemon=True)
        t1.start()
