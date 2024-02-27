import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define your scopes and spreadsheet ID here
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1sEYu1HKDWDgpvX_UFaLtAZdG9tZmoTQ_ZqGHnp3WTpA"  # Update this with your Spreadsheet ID

def get_service():
    """Authenticate and return a Google Sheets API service."""
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
    
    service = build("sheets", "v4", credentials=creds)
    return service

def update_cell(range_name, new_value):
    """Updates a specific cell in a spreadsheet."""
    try:
        service = get_service()
        body = {'values': [[new_value]]}
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_name,
            valueInputOption="RAW", body=body).execute()
        print(f"Updated {result.get('updatedCells')} cell(s).")
    except HttpError as err:
        print(err)
