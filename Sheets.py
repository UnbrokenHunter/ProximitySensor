import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import threading

import Globals
import Statistics
import time

# Define your scopes and spreadsheet ID here
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1sEYu1HKDWDgpvX_UFaLtAZdG9tZmoTQ_ZqGHnp3WTpA"  # Update this with your Spreadsheet ID

def get_service(timeout):
    """Attempt to authenticate and return a Google Sheets API service with a timeout."""
    service = [None]  # Use a list to store the service since lists are mutable

    def authenticate_and_build_service():
        """Authenticate and build the Google Sheets API service."""
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token_file:
                token_file.write(creds.to_json())
        
        service[0] = build("sheets", "v4", credentials=creds)

    # Run the authentication in a separate thread
    thread = threading.Thread(target=authenticate_and_build_service)
    thread.start()
    thread.join(timeout=timeout)  # Wait for the specified timeout

    if thread.is_alive():
        print("Failed to get the service in time")
        return None  # Return None if the thread is still alive after the timeout
    else:
        return service[0]  # Return the service if the thread completed

def update_cell(range_name, new_value):
    """Updates a specific cell in a spreadsheet."""
    try:
        service = get_service(5)
        body = {'values': [[new_value]]}
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_name,
            valueInputOption="RAW", body=body).execute()
        print(f"Updated {result.get('updatedCells')} cell(s).")
    except HttpError as err:
        print(err)

def get_values(range_name):
    """Retrieves the values of a specific cell or cell range from a spreadsheet."""
    try:
        service = get_service(5) 
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return []
        else:
            for row in values:
                # Print columns A and B, which correspond to indices 0 and 1.
                print(row)
            return values
    except HttpError as err:
        print(err)
        return None
    
def find_first_empty_cell_in_column(sheet_name):
    """Finds the first empty cell in the second column of a specified sheet."""
    try:
        service = get_service(5)
        column_letter = 'A'
        range_name = f'{sheet_name}!{column_letter}:{column_letter}'
        
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])

        # Find the first empty row in the column
        row_number = 1  # Start at the second row
        for value in values:
            if not value:  # If the cell is empty
                break
            row_number += 1
        
        if row_number <= len(values):
            print(f"First empty cell in column {column_letter} is at row {row_number}")
        else:
            print(f"All cells in column {column_letter} up to row {row_number} are filled. The first empty cell is at row {row_number + 1}")
            
        if Globals.ControlsLapCount == "Google":
            Globals.LapCount = int(row_number) - 1
        return f"{row_number}"
    except HttpError as err:
        print(err)
        return None

def SaveDataManual(LapTime, Driver, DistanceDriven, InstantSpeed, Time):
    try:
        minRow = find_first_empty_cell_in_column("Sheet1")

        update_cell(f"Sheet1!A{minRow}", Globals.LapCount)

        # Lap Time
        update_cell(f"Sheet1!B{minRow}", LapTime)

        # Driver Name
        update_cell(f"Sheet1!C{minRow}", Driver)

        # Distance Driven
        update_cell(f"Sheet1!D{minRow}", f"{DistanceDriven}km")

        # Instant Speed
        update_cell(f"Sheet1!E{minRow}", f"{((Globals.CarLength / InstantSpeed) * 3600) * 0.621371192}") # From Car Length / Time To Drive that Distance to Km / H to Mph

        # Average Speed
        update_cell(f"Sheet1!F{minRow}", f"{((DistanceDriven / LapTime) * 3600) * 0.621371192}") # From Km / S to Km / H to Mph

        # Time
        update_cell(f"Sheet1!G{minRow}", Time)

    except HttpError as err:
        print(err)


def SaveData(LapTime, InstantSpeed):
    SaveDataManual(LapTime, Globals.CurrentDriver, Statistics.GetDistanceDriven(), InstantSpeed, time.strftime("%Y-%m-%d %H:%M:%S"))
