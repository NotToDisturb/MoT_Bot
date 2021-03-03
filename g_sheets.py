import csv
import os

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials


load_dotenv()
SHEETS_ID = os.getenv("SHEETS_ID")

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]


def open_spreadsheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    auth = gspread.authorize(creds)

    return auth.open_by_key(SHEETS_ID)


def generate_spreadsheet_csv(spreadsheet):
    for worksheet in spreadsheet.worksheets():
        filename = worksheet.title + '.csv'
        with open(filename, 'wt') as file:
            writer = csv.writer(file)
            writer.writerows(worksheet.get_all_values())
