from setTimeFrameStraddle import setTimeFrameStraddle
# a = setTimeFrameStraddle(index="BANKNIFTY", start_date="2020-01-01", end_date="2021-12-31", entry_time="11:55:00", exit_time="14:55:00", stop_loss_p=1.3, historical_data_path="/home/prajwal/Documents/Repositories/kotak/historical_data/", number_of_lots=2, max_loss_per_lot=-3000)
a = setTimeFrameStraddle(index="BANKNIFTY", start_date="2020-01-01", end_date="2021-12-31", entry_time="11:55:00", exit_time="14:55:00", stop_loss_p=1.3, historical_data_path="/home/prajwal/Documents/Repositories/kotak/historical_data/", number_of_lots=2)

# a = setTimeFrameStraddle(index="BANKNIFTY", start_date="2021-11-22", end_date="2021-11-30", entry_time="11:55:00", exit_time="14:55:00", stop_loss_p=1.3, historical_data_path="/home/prajwal/Documents/Repositories/kotak/historical_data/", number_of_lots=2)
a.runBackTest()