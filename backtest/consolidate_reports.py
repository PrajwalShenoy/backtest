import pandas as pd
import numpy as np

def consolidate_reports(csv_file_names = [], consolidated_report = "consolidated.csv"):
    report_df = pd.DataFrame(np.empty((0, 3)))
    report_df.columns = ["Date", "Day", "Net"]
    for csv_report in csv_file_names:
        csv_df = pd.read_csv(csv_report)
        for i in range(len(csv_df)):
            if csv_df["Date"][i] in list(report_df["Date"]):
                report_df.loc[report_df["Date"] == csv_df["Date"][i], "Net"] = report_df.loc[report_df["Date"] == csv_df["Date"][i], "Net"] + csv_df["Net"][i]
            else:
                temp_df = pd.DataFrame({"Date":[csv_df["Date"][i]], "Day":[csv_df["Day"][i]], "Net":[csv_df["Net"][i]]})
                report_df = pd.concat([report_df, temp_df], ignore_index = True, axis=0)
    report_df.to_csv(consolidated_report.sort_values(by=['Date'])[['Date', 'Day', 'Net']])
