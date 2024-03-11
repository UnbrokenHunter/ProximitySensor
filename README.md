# Lap Tracker

This Python application was developed to solve the issue of maintaining an accurate lap count when racing an RC car around a track.

> Please note that this application is designed to function with a hardware sensor's input. This should be plugged in via GPIO pins. The program will still run without this (with some errors), but lap tracking will be entirely non-functional.

Another note is that while this application will run on both Windows and Mac machines, it will not function correctly, as the GPIO library that is used in this program is designed specificly to run on Linux powered Raspberry Pi's.

## Notes on Google Sheets Integration

In order to allow this program to interact with a Google Sheets file, you will have to create a "Google Project" and replace the "Credentials.json" information with your own. A guide on how to do this is provided below:

https://developers.google.com/sheets/api/quickstart/python

## Required Python Libraries

    pip install --upgrade RPi.GPIO spidev Adafruit_GPIO customtkinter google-api-python-client google-auth-httplib2 google-auth-oauthlib openpyxl

## Program Flow
1. Data is read from Sensor or Sensor Emulator.
	* The Sensor Emulator serves as a way to test and debug the program without having to actually run it on a Pi with a sensor. It simply simulates a car going around a "track" having a value and a max value. The value is continually added to in slightly random intervals, and when the value is within a range, it is counted as a lap, and when it beyond the max value, it is reset to 0. This simulates both the fact that a track is circular, and that the pit (and the sensor) must have a detection speed that is able to capture the speed of the car.
2. Data is sent to be proccessed
	Values are compared to the previous value to understand the current state. The logic is:
    | Logic: | Conclusion: |
    | --- | --- |
    | Current Value is not Equal to Previous Value, and the Previous Value is False | We can conclude that the car entered the sensor on this detection. |
    | Current Value is not Equal to Previous Value, and the Previous Value is True  | We can conclude that the car exited the sensor on this detection.  |

3. Lap is Saved
	* When the car is determined to have exited the sensor, a lap is saved. First however, the "Lap Time" is compared to a minimum time variable (10 by default), and if it is below the threshold, the lap is disqualified. 
    * Once verified however, the lap can actually be saved. First the program will attempt to reach the Google Sheets API, and update the data there. If it is successful, the data will be logged in the first empty row.
        * The program will iterate through all previous rows to find this
        * The current lap is also determined by by the row that it finds. It was designed this way to hopefully be more resiliant towards crashes, as even if the program crashes, the local lap count can automaticly update it's self to match the Sheets count (In otherwords, Sheets take priority)
    * Next, the program will save the data to a local Excel file. This is always done to ensure that, at the very least, if the internet connection goes down, we still have useable data. 
    * Finally, if the data is not successfully saved to Google Sheets (And therefore an accurate lap count can not be gathered), the program will increment the lap count variable by one. 
        * This may seem unimportant to note, but by having the lap count be determined by a local variable, a program crash becomes a massive concern, as that variable will not persist across instances. 
