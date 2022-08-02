# back-test
Repository to perform backtest on CSV datasets of indian indexes

## Installation

### Pre requisites
* Python version 3.6 or above is required

### Getting the code / Cloning the repository
* Clone the repository from github.com
Git is required if you want to clone the repository
```
git clone https://github.com/PrajwalShenoy/backtest.git
```
or 
* Download the zip file from https://github.com/PrajwalShenoy/backtest  
To download the zip file click on the green `Code` and click on `Download ZIP`

### Install required modules and libraries
* Make sure you are in the directory where `requirements.txt` is present (backtest/)
* Open a terminal in that location and run the following command
```bash
pip install .
```

With this the code should be ready to use

## Fetching historical data
* Open a python terminal and run the following command with your custom values.
* If you do not have a account on maticalgos, you can follow the following link to create an account http://historical.maticalgos.com/
* `index` can be given the value of `banknifty` or `nifty`
* Make sure the directory mentioned in `file_path` is created before running the commands
```python
from backtest.get_historical_data import get_historical_data

get_historical_data(index="banknifty", email="abc@xyz.com", password="password", start_date="2020-01-01", end_date="2020-01-31", file_path="/home/user/Desktop/historicalData")
```

## Running Index Spot based SL straddle with specified entry and exit time
* Open a python terminal and run the following command with your custom values.
```python
from backtest.setTimeStraddleIndexSL import setTimeStraddleIndexSL

trade1 = setTimeStraddleIndexSL(index="BANKNIFTY", start_date="2020-01-01", end_date="2020-01-10", entry_time="09:20:00", exit_time="15:24:00", stop_loss_p=0.009, historical_data_path="/home/prajwal/Desktop/backtest-documentation/back/backtest/", number_of_lots=1, csv_out_file="trade1_report.csv", days_to_run=[2,3])
trade1.runBackTest()
```

## How to create consolidated reports
* Open a python terminal and run the following command with your custom values.
```python
from backtest.consolidate_reports import consolidate_reports

trade1 = setTimeStraddleIndexSL(index="BANKNIFTY", start_date="2019-01-01", end_date="2021-12-31", entry_time="09:20:00", exit_time="15:24:00", stop_loss_p=0.009, historical_data_path="/home/prajwal/Documents/Repositories/kotak/historical_data/", number_of_lots=1, csv_out_file="trade1_report.csv", days_to_run=[2,3])
trade1.runBackTest()

trade2 = setTimeStraddleIndexSL(index="BANKNIFTY", start_date="2019-01-01", end_date="2021-12-31", entry_time="09:20:00", exit_time="15:24:00", stop_loss_p=0.007, historical_data_path="/home/prajwal/Documents/Repositories/kotak/historical_data/", number_of_lots=1, csv_out_file="trade2_report.csv", days_to_run=[0,1,2,3,4])
trade2.runBackTest()

# The above commands generate trade1_report.csv and trade2_report.csv. The next command creates the consolidated report
consolidate_reports(csv_file_names=["trade1_report.csv", "trade2_report.csv"], consolidated_report="consolidated.csv")
```

## How to use the analysis tool
* Open a python terminal and run the following command with your custom csv file
```python
from backtest.analyseReport import m2mPlot, perWeekdayPieChart, lossesSplit, profitsSplit
import pandas as pd

df = pd.read_csv("Path to report file")
profitsSplit(df)
lossesSplit(df)
perWeekdayPieChart(df)
m2mPlot(df)
```

## Refer to examples.py for more examples on how to use these tools in a python script

## Additional information
* `days_to_run` indicate the days on which the back test will run. The mapping is as follows
```
0 - Monday
1 - Tuesday
2 - Wednesday
3 - Thursday
4 - Friday
5 - Saturday
6 - Sunday
```
* Even when specified, backtest will not run on `5` and `6`. (Afterall backtest also needs a holiday XD)
* `Formula_generator.xlsm` is a community developed excel sheet to help you guys get the respective `python` command to run the respective straddles.

Special thanks to Himanshu for helping test this new tool

