from setTimeStraddleIndexSL import setTimeStraddleIndexSL
from consolidate_reports import consolidate_reports
from get_historical_data import get_historical_data

# Historical data curtosy of http://historical.maticalgos.com/
get_historical_data("banknifty", "email@email.com", "password", "2019-01-01", "2021-12-31")

trade1 = setTimeStraddleIndexSL(index="BANKNIFTY", start_date="2019-01-01", end_date="2021-12-31", entry_time="09:20:00", exit_time="15:24:00", stop_loss_p=0.009, historical_data_path="/home/prajwal/Documents/Repositories/kotak/historical_data/", number_of_lots=1, csv_out_file="trade1_report.csv", days_to_run=[2,3])
trade1.runBackTest()

trade2 = setTimeStraddleIndexSL(index="BANKNIFTY", start_date="2019-01-01", end_date="2021-12-31", entry_time="09:20:00", exit_time="15:24:00", stop_loss_p=0.007, historical_data_path="/home/prajwal/Documents/Repositories/kotak/historical_data/", number_of_lots=1, csv_out_file="trade1_report.csv", days_to_run=[2,3])
trade2.runBackTest()

consolidate_reports(csv_file_names=["trade1_report.csv", "trade2_report.csv"], consolidated_report="consolidated.csv")
