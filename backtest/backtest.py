import pandas as pd
import datetime
import logging
import csv



class Backtester():

    months = {
                        "01": "Jan", "1": "Jan",
                        "02": "Feb", "2": "Feb",
                        "03": "Mar", "3": "Mar",
                        "04": "Apr", "4": "Apr",
                        "05": "May", "5": "May",
                        "06": "Jun", "6": "Jun",
                        "07": "Jul", "7": "Jul",
                        "08": "Aug",
                        "09": "Sep",
                        "10": "Oct",
                        "11": "Nov",
                        "12": "Dec"
                    }

    def __init__(self, index="BANKNIFTY", start_date="", end_date="", **kwargs):
        self.log = logging.getLogger(__name__)
        self.log.addHandler(logging.NullHandler())
        self.index = index
        self.start_date = start_date
        self.end_date = end_date
        self.get_base_vars(kwargs)
        self.get_trading_holidays()

    def get_base_vars(self, kwargs):
        pass

    def get_trading_holidays(self):
        from publicHolidays import public_holidays
        self.public_holidays = public_holidays

    
    def create_scrip_symbol(self, date, month, year, option_type, strike_price, index = "BANKNIFTY"):
        return self.df.iloc[10]["symbol"][:16] + str(strike_price) + option_type.upper()
        # symbol = ""
        # if str(year) + "-" + str(month) + "-" + str(date) in self.public_holidays:
        #     date = "0" + str(int(date) - 1) if (int(date) - 1)//10 < 1 else str(int(date) - 1)
        # if index == "BANKNIFTY":
        #     symbol = "BANKNIFTY" + str(date) + self.months[str(month)].upper() + str(year)[-2:] + str(strike_price) + option_type.upper()
        #     self.log.debug("Created scrip symbol " + symbol)
        # else:
        #     self.log.error("Other indeces are not yet supported")
        # return symbol
    
    def calculate_result(self, ce_price, current_ce_price, pe_price, current_pe_price):
        net = ce_price - current_ce_price + pe_price - current_pe_price
        return (net * self.number_of_lots * self.quantity_per_lot)

    def next_weekday(self, d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def next_thursday(self, d):
        days_ahead = 3 - d.weekday()
        if days_ahead < 0:
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def increment_date(self, d):
        if type(d) != datetime.date:
            d = datetime.date(d.split("-")[0], d.split("-")[1], d.split("-")[2])
        d = d + datetime.timedelta(1)
        # if d.weekday() == 5 or d.weekday() == 6 or d.weekday() == 4 or d.weekday() == 0 or d.weekday() == 1:
        if d.weekday() == 5 or d.weekday() == 6:
            d = self.increment_date(d)
        return d

    def increment_time(self, dt, interval):
        if type(dt) != datetime.time:
            strt = str(dt).split(":")
            dt = datetime.datetime(100,1,1,int(strt[0]),int(strt[1]),int(strt[2]))
        dt = dt + datetime.timedelta(minutes=interval)
        return dt.time()

    def find_strike_price(self, cur_price):
        return (round(int(cur_price)/100)*100)

    def deci2(self, value):
        return (round(value*100)/100)

    def create_date(self, d):
        if type(d) != datetime.date and type(d) == str:
            return datetime.date(int(d.split('-')[0]), int(d.split('-')[1]), int(d.split('-')[2]))
        elif type(d) == datetime.date:
            return d
        else:
            self.log.error("Date is not in the required format, follow the 'yyyy-mm-dd' format")

    def create_time(self, t):
        if type(t) != datetime.time and type(t) == str:
            return datetime.time(int(t.split(":")[0]), int(t.split(":")[1]), int(t.split(":")[2]))
        elif type(t) == datetime.time:
            return t
        else:
            self.log.error("Time is not in the required format, follow the 'hh:mm:ss' format")

    def create_date_time(self, d_t):
        d_t = d_t.split("")
        d = d_t[0]
        t = d_t[1]
        return datetime.datetime(int(d.split('-')[0]), int(d.split('-')[1]), int(d.split('-')[2]),
                                int(t.split(":")[0]), int(t.split(":")[1]), int(t.split(":")[2]))

    def get_price_for_nearest_time(self, df, t):
        if len(df.loc[df["time"] == t].values) == 1:
            return df.loc[df["time"] == t]["open"].values[0], t
        else:
            while len(df.loc[df["time"] == t].values) == 0 and str(t) < "16:00:00":
                t = str(self.increment_time(t, 1))
            return df.loc[df["time"] == t]["open"].values[0], t
        
    def create_monthly_result_dict(self):
        current_date_format = self.create_date(self.start_date)
        end_date_format = self.create_date(self.end_date)
        monthly_results = {}
        while (end_date_format - current_date_format).days >= 0:
            monthly_results[str(current_date_format)[:-3]] = 0
            current_date_format = self.increment_date(current_date_format)
        return monthly_results

    def read_csv_data(self, file_path = ""):
        if file_path:
            return pd.read_csv(file_path)
        else:
            return pd.read_csv(self.historical_data_path + str(self.current_date_format).replace("-", "") + ".csv")


