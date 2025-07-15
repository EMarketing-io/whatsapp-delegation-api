import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "credentials.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
TEXT_INPUT_SHEET_ID = os.getenv("TEXT_INPUT_SHEET_ID")
EMPLOYEE_SHEET_ID = os.getenv("EMPLOYEE_SHEET_ID")
FOLDER_ID = os.getenv("FOLDER_ID")

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
