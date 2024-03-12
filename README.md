# Lap Tracker

This Python application was developed to solve the issue of maintaining an accurate lap count when racing an RC car around a track.

> Please note that this application is designed to function with a hardware sensor's input. This should be plugged in via GPIO pins. The program will still run without this (with some errors), but lap tracking will be entirely non-functional.

Another note is that while this application will run on both Windows and Mac machines, it will not function correctly, as the GPIO library that is used in this program is designed specifically to run on Linux powered Raspberry Pi's.

## Notes on Google Sheets Integration

If this is being read in the future, and your use case is unrelated to a certain World Record attempt that is happening in early 2024, then, in order to allow this program to interact with a Google Sheets file, you will have to create a "Google Project" and replace both the "Credentials.json", and the "token.json" files with your own information. You will also have to change the "SPREADSHEET_ID" variable in the "Sheets.py" file with your own spreadsheet. A guide on how to do this is provided below:

https://developers.google.com/sheets/api/quickstart/python

If your use case is related to the above mentioned World Record Attempt, then all that is required is to delete the "Credentials.json" file, if present, then run the program. This will prompt you to log into a Google Account via web browser. Log in, and rerun the program.

## Required Python Libraries

    pip install --upgrade RPi.GPIO spidev Adafruit_GPIO customtkinter google-api-python-client google-auth-httplib2 google-auth-oauthlib openpyxl gpiozero

## Program Flow

1. Data is read from Sensor or Sensor Emulator.
   - The Sensor Emulator serves as a way to test and debug the program without having to actually run it on a Pi with a sensor. It simply simulates a car going around a "track" having a value and a max value. The value is continually added to in slightly random intervals, and when the value is within a range, it is counted as a lap, and when it exceeds the max value, it is reset to 0. This simulates both the fact that a track is circular, and that the pit (and the sensor) must have a detection speed that is able to capture the speed of the car.
2. Data is sent to be processed
   Values are compared to the previous value to understand the current state. The logic is:
   | Logic: | Conclusion: |
   | --- | --- |
   | Current Value is not Equal to Previous Value, and the Previous Value is False | We can conclude that the car entered the sensor on this detection. |
   | Current Value is not Equal to Previous Value, and the Previous Value is True | We can conclude that the car exited the sensor on this detection. |

3. Lap is Saved

   - When the car is determined to have exited the sensor, a lap is saved. First however, the "Lap Time" is compared to a minimum time variable (10 by default), and if it is below the threshold, the lap is disqualified.
   - The second filter checks that the sensor is not endlessly displaying a positive value. This is to prevent a misaligned sensor from appearing as if it is working, by displaying new laps being saved. The default threshold is if all of the last 80 values were true, it will begin halting future lap saves, and printing a warning message to the screen.
   - Once verified however, the lap can actually be saved. First the program will attempt to reach the Google Sheets API, and update the data there. If it is successful, the data will be logged in the first empty row.
     - The program will iterate through all previous rows to find this
     - The current lap is also determined by the row that it finds. It was designed this way to hopefully be more resilient towards crashes, as even if the program crashes, the local lap count can automatically update itself to match the Sheets count (In other words, Sheets take priority)
   - Next, the program will save the data to a local Excel file. This is always done to ensure that, at the very least, if the internet connection goes down, we still have usable data.
   - Finally, if the data is not successfully saved to Google Sheets (And therefore an accurate lap count can not be gathered), the program will increment the lap count variable by one.
     - This may seem unimportant to note, but by having the lap count be determined by a local variable, a program crash becomes a much larger concern, as that variable will not persist across instances.

4. Program startup and GUI
   - The GUI functions entirely independently of the sensor. When the program is run (Through the file, "Window.py"), three other files will be run immediately. In order they are "TitleWindow.py", "DataWindow.py", and "DebugWindow.py". Then, the Run() method is called on the Sensor.py file. As said earlier, the sensor file will run, independent of the GUI. This is done using multithreading. When the Run() method is called, a new thread is created and it will infinitely loop checking the selected pin for data. This data is then passed to be Processed, therefore completing the core program loop.
   - Title Window
     - Controls whether or not to Filter Laps (Disqualify laps that are below 10 seconds), Whether or not to track data, who the current selected driver is (Has to be selected from a dropdown in the GUI), and finally, the option to add laps manually.
   - Data Window
     - The Data Window the data stored locally, for the pit crew to view, without having to check a spreadsheet. It stores Lap Count, Current Lap Time, Average Lap Time, a Projected End Time, and finally, displays all previous laps in a scrollable box.
     - The live data in the Data Window is continuously updated using multithreading. Then the file is run for the first time, a new thread is created that will loop forever, updating all of the fields to reflect the new data.
   - The Debug Window allows you to change certain core variables in the program, such as the GPIO pin that is being checked by the sensor, amount of time between each GPIO pin read, and finally, a dropdown to select what kind of sensor should be used for input (for testing and debugging).
     - When a Mode Dropdown is selected, it will kill the thread that is currently running, and start a new thread of the opposite type.
   - You can also change settings related to Lap Filtering, including the minimum time per lap, and the threshold for considering the sensor to be misaligned or broken.
