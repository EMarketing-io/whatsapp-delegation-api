from auth import authorize
from config import EMPLOYEE_SHEET_ID

def load_employee_data():
    client = authorize()
    sheet = client.open_by_key(EMPLOYEE_SHEET_ID).sheet1
    return {
        row[0].strip(): row[1].strip()
        for row in sheet.get_all_values()
        if len(row) >= 2
    }
