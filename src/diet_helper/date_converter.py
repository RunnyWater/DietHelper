from datetime import datetime


def get_normalized_date(date:datetime):
    return datetime.combine(date, datetime.min.time())

def from_string_to_date(date:str):
    return datetime.strptime(date, '%Y-%m-%d')

def get_todays_date():
    return datetime.combine(datetime.today(), datetime.min.time())