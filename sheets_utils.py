import csv

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]


def open_spreadsheet(sheet_id):
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    auth = gspread.authorize(creds)

    return auth.open_by_key(sheet_id)


def generate_spreadsheet_csv(spreadsheet):
    for worksheet in spreadsheet.worksheets():
        filename = worksheet.title + '.csv'
        with open(filename, 'wt') as file:
            writer = csv.writer(file)
            writer.writerows(worksheet.get_all_values())
            print(filename + "(ID " + str(worksheet.id) + ") has been generated")


def get_index_in_column(file_path, column_name, element):
    with open(file_path, "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for index, line in enumerate(reader):
            if line[column_name] == element:
                return index
        return -1


def get_element_in_column(file_path, column_name, index):
    with open(file_path, "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for csv_index, line in enumerate(reader):
            if csv_index == index:
                return line[column_name]
        return None
