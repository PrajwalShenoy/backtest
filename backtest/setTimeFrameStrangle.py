from backtest.backtester import Backtester
from pprint import pprint
import pandas as pd

class setTimeFrameStraddle(Backtester):
    def __init__(self, index, start_date, end_date, entry_time, exit_time, point_deviation, stop_loss_p, **kwargs):
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.stop_loss_p = stop_loss_p
        self.point_deviation = point_deviation
        super(setTimeFrameStraddle, self).__init__(index, start_date, end_date, **kwargs)
        self.get_additional_vars(kwargs)

    def get_additional_vars(self, kwargs):
        self.historical_data_path = kwargs.get("historical_data_path", "./hostoricalData/")
        self.number_of_lots = kwargs.get("number_of_lots", 1)
        self.csv_out_file = kwargs.get("csv_out_file", "backtestFromCsv.csv")
        self.max_loss_per_lot = kwargs.get("max_loss_per_lot", -10000000000)
        if kwargs.get("quantity_per_lot", False):
            self.quantity_per_lot = kwargs.get("quantity_per_lot")
        elif self.index == "BANKNIFTY":
            self.quantity_per_lot = 25
        elif self.index == "NIFTY":
            self.quantity_per_lot = 50
    
    def initialise_for_csv_backtest(self):
        current_date = str(self.current_date_format)
        index_df = self.df.loc[self.df["symbol"] == self.index].sort_values(by = "time")
        self.index_price, self.banknifty_time = self.get_price_for_nearest_time(index_df, self.entry_time)
        index_strike_price = self.find_strike_price(self.index_price)
        print(index_strike_price, current_date)
        thursday = self.next_thursday(self.current_date_format)
        self.ce_symbol = self.create_scrip_symbol("CE", index_strike_price + self.point_deviation, self.index)
        self.pe_symbol = self.create_scrip_symbol("PE", index_strike_price - self.point_deviation, self.index)
        print(self.ce_symbol, self.pe_symbol)
        self.ce_df = self.df.loc[self.df["symbol"] == self.ce_symbol].sort_values(by = "time")
        self.ce_price, self.ce_initial_time = self.get_price_for_nearest_time(self.ce_df, self.entry_time)
        self.pe_df = self.df.loc[self.df["symbol"] == self.pe_symbol].sort_values(by = "time")
        self.pe_price, self.pe_initial_time = self.get_price_for_nearest_time(self.pe_df, self.entry_time)
        self.ce_sl = self.ce_price * self.stop_loss_p
        self.pe_sl = self.pe_price * self.stop_loss_p
        print(self.ce_symbol, self.ce_price, self.ce_sl, self.ce_initial_time)
        print(self.pe_symbol, self.pe_price, self.pe_sl, self.pe_initial_time)

    def csv_backtest_for_day(self):
        ce_sl_hit = False
        pe_sl_hit = False
        self.ce_df = self.ce_df.sort_values(by = "time")
        self.pe_df = self.pe_df.sort_values(by = "time")
        for i in range(len(self.ce_df)):
            if self.create_time(self.entry_time) <= self.create_time(self.ce_df.iloc[i]["time"]) <= self.create_time(self.exit_time):
                if not ce_sl_hit:
                    self.current_ce_price, self.current_ce_time = self.ce_df.iloc[i]["high"], self.ce_df.iloc[i]["time"]
                    if self.current_ce_price >= self.ce_sl:
                        ce_sl_hit = True
                        self.current_ce_price = self.ce_sl
                        print("\033[1;91mstoploss hit for CE\033[0m")
                if not pe_sl_hit:
                    self.current_pe_price, self.current_pe_time = self.pe_df.iloc[i]["high"], self.pe_df.iloc[i]["time"]
                    if self.current_pe_price >= self.pe_sl:
                        pe_sl_hit = True
                        self.current_pe_price = self.pe_sl
                        print("\033[1;91mstoploss hit for PE\033[0m")
                if self.calculate_result(self.ce_price, self.current_ce_price, self.pe_price, self.current_pe_price) < self.max_loss_per_lot * self.number_of_lots:
                    break
        self.sl_hit = ce_sl_hit + pe_sl_hit
        self.result = self.calculate_result(self.ce_price, self.current_ce_price, self.pe_price, self.current_pe_price)

    def runBackTest(self):
        self.success = 0
        self.failure = 0
        self.max_profit = 0
        self.total_profit = 0
        self.total_profit_days = 0
        self.max_days_with_profit = 0
        self.max_days_with_profit_temp = 0
        self.max_loss = 0
        self.total_loss = 0
        self.total_loss_days = 0
        self.max_days_with_loss = 0
        self.max_days_with_loss_temp = 0
        self.overall_result = 0
        self.monthly_results = self.create_monthly_result_dict()
        self.csvFile = open(self.csv_out_file, "w")
        self.buffer = "Date,Day,Index,CE,CE Time,CE Price,CE SL,CE LTP,PE,PE Time,PE Price,PE SL,PE LTP,SL hit,Net\n"
        self.csvFile.write(self.buffer)
        self.current_date_format = self.create_date(self.start_date)
        self.end_date_format = self.create_date(self.end_date)
        failed_backtests = {}
        while (self.end_date_format - self.current_date_format).days >= 0:
            while self.create_date(self.current_date_format).weekday() not in self.days_to_run:
                self.current_date_format = self.increment_date(self.current_date_format)
            if str(self.current_date_format) not in self.public_holidays:
                try:
                    self.df = self.read_csv_data()
                    self.initialise_for_csv_backtest()
                    self.csv_backtest_for_day()
                    self.overall_result += self.result
                    self.monthly_results[str(self.current_date_format)[:-3]] += self.result
                    print("==========================================")
                    if self.result >= 0:
                        self.max_days_with_loss = max(self.max_days_with_loss, self.max_days_with_loss_temp)
                        self.max_days_with_loss_temp = 0
                        self.max_days_with_profit_temp = self.max_days_with_profit_temp + 1
                        self.total_profit_days = self.total_profit_days + 1
                        self.total_profit = self.total_profit + self.result
                        self.max_profit = max(self.max_profit, self.result)
                        print("\033[1;92m",self.deci2(self.result), "\n\033[0m")
                    else:
                        self.max_days_with_profit = max(self.max_days_with_profit, self.max_days_with_profit_temp)
                        self.max_days_with_profit_temp = 0
                        self.max_days_with_loss_temp = self.max_days_with_loss_temp + 1
                        self.total_loss_days = self.total_loss_days + 1
                        self.total_loss = self.total_loss + self.result
                        self.max_loss = min(self.max_loss, self.result)
                        print("\033[1;91m",self.deci2(self.result), "\n\033[0m")
                    self.buffer = [str(self.current_date_format), self.get_day(self.current_date_format), str(float(self.index_price)), self.ce_symbol, self.ce_initial_time, str(self.ce_price), str(self.ce_sl), str(self.current_ce_price), \
                                    self.pe_symbol, self.pe_initial_time, str(self.pe_price), str(self.pe_sl), str(self.current_pe_price), str(self.sl_hit), str(self.deci2(self.result))]
                    self.csvFile.write(",".join(self.buffer) + "\n")
                    self.success = self.success + 1
                except Exception as e:
                    self.log.error(str(e))
                    self.log.error("Could not backtest for " + str(self.current_date_format) + "\n")
                    if "No such file or directory" not in str(e):
                        self.failure = self.failure + 1
                        failed_backtests[str(self.current_date_format)] = str(e)
            else:
                pass
            self.current_date_format = self.increment_date(self.current_date_format)
        self.csvFile.close()
        self.max_days_with_profit = max(self.max_days_with_profit, self.max_days_with_profit_temp)
        self.max_days_with_loss = max(self.max_days_with_loss, self.max_days_with_loss_temp)
        print("Entry time:", self.entry_time, "Exit time:", self.exit_time, "Sl:", self.stop_loss_p)
        print("Overall result", self.overall_result)
        print("Average result", self.overall_result/(self.success + self.failure))
        print("Max profit was", self.max_profit)
        print("Average profit on profit making days was", self.total_profit/self.total_profit_days)
        print("Winning streak:", self.max_days_with_profit)
        print("Win percentage", self.total_profit_days/self.success)
        print("Max loss was", self.max_loss)
        print("Average loss on loss making days was", self.total_loss/self.total_loss_days)
        print("Loosing streak:", self.max_days_with_loss)
        print("Win percentage", self.total_loss_days/self.success)
        print("Successfull back tests:", self.success)
        print("Failed back tests:", self.failure)
        print("Monthly wise resport is given below")
        for i, j in self.monthly_results.items():
            print(i, ": ", j)
