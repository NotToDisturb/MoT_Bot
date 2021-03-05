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


def find_item_in_columns_and_get_row(file_path, column_names, element, ignore_case=True):
    with open(file_path, "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for index, line in enumerate(reader):
            if isinstance(column_names, str):
                if compare_item_with_case(element, line[column_names], ignore_case):
                    return line, index
            else:
                for column_name in column_names:
                    if compare_item_with_case(element, line[column_name], ignore_case):
                        return line, index
        return None, -1


def compare_item_with_case(element, content, ignore_case):
    if ignore_case:
        element = element.lower()
        content = content.lower()
    return content == element
