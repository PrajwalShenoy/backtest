# Historical data curtosy of http://historical.maticalgos.com/
from maticalgos.historical import historical
import datetime
import os


def increment_date(d):
    d = d + datetime.timedelta(1)
    if d.weekday() == 5 or d.weekday() == 6:
        d = increment_date(d)
    return d

def create_date(d):
    return datetime.date(int(d.split('-')[0]), int(d.split('-')[1]), int(d.split('-')[2]))

def get_historical_data(index, email, password, start_date, end_date, file_path):
    ma = historical(email)
    ma.login(password)
    current_date_format = create_date(start_date)
    end_date_format = create_date(end_date)
    faulty_dates = []
    while (end_date_format - current_date_format).days >= 0:
        try:
            data = ma.get_data(index, current_date_format)
            csv_path = os.path.join(file_path, str(current_date_format).replace("-", "") + ".csv")
            data.to_csv(csv_path)
            print("\033[1;92mFinished processing the following date", str(current_date_format), "\033[0m")
        except Exception as err:
            faulty_dates.append(str(current_date_format))
            print("\033[1;91mCould not process the following date", str(current_date_format), "\033[0m")
            print(err)
        current_date_format = increment_date(current_date_format)
    print("Failed to get data for the following dates", faulty_dates)
