from auth import authorize
from config import SPREADSHEET_ID


def write_to_sheet(rows):
    if not rows:
        return
    client = authorize()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    sheet.append_rows(rows, value_input_option="USER_ENTERED")
