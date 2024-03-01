import os
import openpyxl
from openpyxl import Workbook
import time

import Globals
import Statistics

SPREADSHEET_FILE_PATH = "sheets_backup.xlsx"

def get_or_create_workbook(file_path):
    """Check if the spreadsheet file exists. If not, create it and add headers."""
    headers = ["Lap Count", "Lap Time", "Driver Name", "Distance Driven", "Instant Speed", "Average Speed", "Time"]  # Define your headers here
    if not os.path.exists(file_path):
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.append(headers)  # Add headers to the first row
        wb.save(file_path)
    else:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb["Sheet1"]
        if sheet.max_row == 1:
            # Check if the first row is empty or only contains headers; if so, append the headers.
            # Note: This is a basic check and might need adjustments based on your actual requirements.
            empty_or_headers_only = all(sheet[f"A1":f"G1"][0][i].value in (None, headers[i]) for i in range(len(headers)))
            if empty_or_headers_only:
                for col_num, header in enumerate(headers, start=1):
                    sheet.cell(row=1, column=col_num, value=header)
                wb.save(file_path)
    return wb

def update_cell(sheet_name, row_number, column_letter, new_value):
    """Updates a specific cell in a spreadsheet."""
    wb = get_or_create_workbook(SPREADSHEET_FILE_PATH)
    sheet = wb[sheet_name]
    cell_reference = f"{column_letter}{row_number + 1}"
    sheet[cell_reference] = new_value
    wb.save(SPREADSHEET_FILE_PATH)
    print(f"Updated cell {cell_reference}.")

def SaveData(LapTime, InstantSpeed):
    try:
        sheet_name = "Sheet1"
        minRow = Globals.LapCount

        # Lap Count
        update_cell(sheet_name, minRow, 'A', Globals.LapCount)

        # Lap Time
        update_cell(sheet_name, minRow, 'B', LapTime)

        # Driver Name
        update_cell(sheet_name, minRow, 'C', Globals.CurrentDriver)

        # Distance Driven
        distance_driven = f"{Statistics.GetDistanceDriven()}km"
        update_cell(sheet_name, minRow, 'D', distance_driven)

        # Instant Speed
        instant_speed_mph = f"{((Globals.CarLength / InstantSpeed) * 3600) * 0.621371192}"  # From Car Length / Time To Drive that Distance to Km / H to Mph
        update_cell(sheet_name, minRow, 'E', instant_speed_mph)

        # Average Speed
        average_speed_mph = f"{((Statistics.GetDistanceDriven() / LapTime) * 3600) * 0.621371192}"  # From Km / S to Km / H to Mph
        update_cell(sheet_name, minRow, 'F', average_speed_mph)

        # Time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        update_cell(sheet_name, minRow, 'G', current_time)

    except Exception as err:
        print(err)
