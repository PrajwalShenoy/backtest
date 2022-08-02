# TODO
- [x] add days on when the code needs to run - Done
- [x] combined report for all trades - Done
- [ ] adding a GUI
- [ ] enable github 
- [ ] check data quality
- [ ] Create a GUI charter to create charts for specific days
- [ ] Create tool to analyse the results



## BUG FIXES (Aug 1st 2022, 3:10 AM)
* Fixed the commands present in examples.py (trade1.run() was replaced with trade1.runBackTest())
* Fixed the issues with "backtest execution date"
* Fixed the issue with the "first date"/"start_date" being present in all reports (This was causing problems in consolidated reports)
* Consolidated reports are now sorted by default. Previously the date order was jumbled
* Added historical_data_script, made additions to examples.py as well.
* Added Formula_generator.xlsm for convenience of non coders

## UPDATES AND BUG FIXES (Aug 2ns 2022, 3:16 AM)
* Brought in a few breaking changes. Going forward the tool will have to be installed before being used. This was done as using it with relative reference was causing issues with fetching hitstorical data.
* Updated requirements.txt
* Added README.md for usage instructions
* Updated the examples.py with the new usage
* Fixed the bug in consolidated_report.py where previously string was being sorted, now the respective dataframe will be sorted
* Chnaged backtest.py to backtester.py to conform with python packaging norms
