from matplotlib.widgets import Slider
import matplotlib.ticker as tick
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

def profitsSplit(df):
    days = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0}
    for i in range(len(df)):
        if df.loc[i]["Net"] > 0:
            days[df.loc[i]["Day"]] = days[df.loc[i]["Day"]] + df.loc[i]["Net"]
    pie_day = []
    pie_profits = []
    for day, net in days.items():
        pie_day.append(day)
        pie_profits.append(net)
    plt.subplot(121)
    plt.pie(pie_profits, labels=pie_day, autopct='%1.2f%%')
    plt.subplot(122)
    bars = plt.barh(pie_day, pie_profits)
    plt.bar_label(bars)
    plt.title("Profits Pie Chart for weekdays")
    plt.show()

def lossesSplit(df):
    days = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0}
    for i in range(len(df)):
        if df.loc[i]["Net"] < 0:
            days[df.loc[i]["Day"]] = days[df.loc[i]["Day"]] + abs(df.loc[i]["Net"])
    pie_day = []
    pie_losses = []
    for day, net in days.items():
        pie_day.append(day)
        pie_losses.append(net)
    plt.subplot(121)
    plt.pie(pie_losses, labels=pie_day, autopct='%1.2f%%')
    plt.subplot(122)
    bars = plt.barh(pie_day, pie_losses)
    plt.bar_label(bars)
    plt.title("Losses Pie Chart for weekdays")
    plt.show()

def netSplit(df):
    days = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0}
    for i in range(len(df)):
        days[df.loc[i]["Day"]] = days[df.loc[i]["Day"]] + df.loc[i]["Net"]
    pie_day = []
    pie_net = []
    for day, net in days.items():
        pie_day.append(day)
        pie_net.append(net)
    plt.subplot(121)
    plt.pie(pie_net, labels=pie_day, autopct='%1.2f%%')
    plt.subplot(122)
    bars = plt.barh(pie_day, pie_net)
    plt.bar_label(bars)
    plt.title("Net Pie Chart for weekdays")
    plt.show()

def perWeekdayPieChart(df):
    days = {"Mon": [0,0],
            "Tue": [0,0],
            "Wed": [0,0],
            "Thu": [0,0],
            "Fri": [0,0]}
    for i in range(len(df)):
        if df.loc[i]["Net"] < 0:
            days[df.loc[i]["Day"]][1] = days[df.loc[i]["Day"]][1] + 1
        if df.loc[i]["Net"] > 0:
            days[df.loc[i]["Day"]][0] = days[df.loc[i]["Day"]][0] + 1
    labs = "Profit", "Loss"
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5)
    ax1.pie(days["Mon"], labels=labs, autopct='%1.1f%%')
    ax1.title.set_text("Mon")
    ax2.pie(days["Tue"], labels=labs, autopct='%1.1f%%')
    ax2.title.set_text("Tue")
    ax3.pie(days["Wed"], labels=labs, autopct='%1.1f%%')
    ax3.title.set_text("Wed")
    ax4.pie(days["Thu"], labels=labs, autopct='%1.1f%%')
    ax4.title.set_text("Thu")
    ax5.pie(days["Fri"], labels=labs, autopct='%1.1f%%')
    ax5.title.set_text("Fri")
    plt.show()

def m2mPlot(df):
    net = 0
    yaxis = []
    xaxis = []
    for i in range(len(df)):
        net = net + df.loc[i]["Net"]
        xaxis.append(df.loc[i]["Date"])
        yaxis.append(net)
    dump = fig, ax = plt.subplots()
    dump = ax.plot(xaxis, yaxis)
    dump = ax.get_yaxis().set_major_formatter(tick.FuncFormatter(lambda x, p: format(int(x), ',')))
    dump = plt.xlabel('Date')
    dump = plt.xticks(rotation = 90)
    dump = plt.ylabel('Net M2M')
    dump = plt.title('M2M graph')
    dump = plt.grid()
    plt.show()

def calculateDrawDown(df):
    net = 0
    yaxis = []
    xaxis = []
    for i in range(len(df)):
        net = net + df.loc[i]["Net"]
        xaxis.append(df.loc[i]["Date"])
        yaxis.append(net)
    dump = fig, ax = plt.subplots()
    dump = ax.plot(xaxis, yaxis)
    dump = ax.get_yaxis().set_major_formatter(tick.FuncFormatter(lambda x, p: format(int(x), ',')))
    dump = plt.xlabel('Date')
    dump = plt.xticks(rotation = 90)
    dump = plt.ylabel('Net M2M')
    dump = plt.title('M2M graph')
    xs = df["Net"].cumsum()
    i = np.argmax(np.maximum.accumulate(xs) - xs)
    j = np.argmax(xs[:i])
    # plt.plot(xs)
    plt.plot([i, j], [xs[i], xs[j]], 'o', color='Red', markersize=10)
    print("Max DD is", xs[j] - xs[i])
    plt.show()
    
def showAllGraphs(df):
    profitsSplit(df)
    lossesSplit(df)
    netSplit(df)
    perWeekdayPieChart(df)
    calculateDrawDown(df)

def main():
    file_name = sys.argv[1]
    df = pd.read_csv(file_name)
    showAllGraphs(df)

if __name__ == "__main__":
    main()