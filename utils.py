from datetime import datetime


def str_to_date_converter(date_str):
    if len(date_str) <= 10:
        data = datetime.strptime(date_str, "%d-%m-%Y")
    else:
        data = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
    return data