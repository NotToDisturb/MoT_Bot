import csv
import os

import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
RESOURCES_FOLDER = os.getenv("RESOURCES_FOLDER")

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]


def do_resources_path(file_path):
    return os.path.normpath(RESOURCES_FOLDER + file_path)


def open_spreadsheet(sheet_id):
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    auth = gspread.authorize(creds)

    return auth.open_by_key(sheet_id)


def generate_spreadsheet_csv(spreadsheet):
    for worksheet in spreadsheet.worksheets():
        filename = do_resources_path(worksheet.title + '.csv')
        with open(filename, 'wt') as file:
            writer = csv.writer(file)
            writer.writerows(worksheet.get_all_values())
            print(filename + "(ID " + str(worksheet.id) + ") has been generated")


def get_index_in_column(file_path, column_name, element):
    with open(do_resources_path(file_path), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for index, line in enumerate(reader):
            if line[column_name] == element:
                return index
        return -1


def get_line_at_row(file_path, index):
    with open(do_resources_path(file_path), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for csv_index, line in enumerate(reader):
            if csv_index == index:
                return line
        return None


def find_item_in_columns_and_get_row(file_path, column_names, element, ignore_case=True):
    with open(do_resources_path(file_path), "rt") as csv_file:
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


def get_num_of_rows(file_path):
    with open(do_resources_path(file_path), "rt") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        return len(list(reader)) - 1
