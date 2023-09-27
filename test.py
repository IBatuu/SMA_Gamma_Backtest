import pandas as pd
from binance.spot import Spot 
from datetime import datetime
import time, itertools, data, random, requests, os
import plotly.graph_objects as chart
import seaborn as sns
from operator import itemgetter
import numpy as np
import plotly.graph_objects as chart
import os
import requests
import plotly.graph_objs as chart
from plotly.subplots import make_subplots

client = Spot(key=data.nanceSubApi, secret=data.secretSubApi)
#listenKey = client.new_isolated_margin_listen_key("BTCUSDT")

def buy(priceToBuy, date=None, reduceOnly=False, Id=None, size=None, tpsldate=None, tpOrSl=None, iv=None, tpmult=None, slmult=None):
    global purchasePrice, finalPortfolio, cashAvaliable
    randomNumber = random.randint(0,1000000)
    if reduceOnly == False:
        purchasePrice = priceToBuy
        addPosition(side="Long", price=priceToBuy, date=date, Id=randomNumber, size=size, tpsldate=tpsldate, tpmult=tpmult, slmult=slmult, iv=iv)
    else:
        for positionperp in positionsPerpetual:
            if positionperp["Id"] == Id:
                positionperp["tpSlDate"] = tpsldate
                positionperp["tpOrSl"] = tpOrSl
def sell(priceToSell, date=None, reduceOnly=False, Id=None, size=None, tpsldate=None, tpOrSl=None, iv=None, tpmult=None, slmult=None):
    global salePrice, finalPortfolio, cashAvaliable
    randomNumber = random.randint(0,1000000)
    if reduceOnly == False:
        salePrice = priceToSell
        addPosition(side="Short", price=priceToSell, date=date, Id=randomNumber, size=size, tpsldate=tpsldate, tpmult=tpmult, slmult=slmult, iv=iv)
    else:
        for positionperp in positionsPerpetual:
            if positionperp["Id"] == Id:
                positionperp["tpSlDate"] = tpsldate
                positionperp["tpOrSl"] = tpOrSl   
def addPosition(side, price, date, Id, size, tpsldate, tpOrSl=None, iv=None, tpmult=None, slmult=None):
    if side == "Long":
        positionsPerpetual.append({"Side": side, "Size": size, "Price": price, "Date": date, "Id": Id, "PriceToTakeProfit": round(price * tpmult), "PriceToStopLoss": round(price * slmult), "tpSlDate": tpsldate, "tpOrSl": tpOrSl, "iv":iv})
    if side == "Short":
        positionsPerpetual.append({"Side": side, "Size": size, "Price": price, "Date": date, "Id": Id, "PriceToTakeProfit": round(price * tpmult), "PriceToStopLoss": round(price * slmult), "tpSlDate": tpsldate, "tpOrSl": tpOrSl, "iv":iv})
def calculate_moving_average(data):
    window_size = 7  # change this to adjust the moving average window size
    moving_averages = []
    for i in range(window_size - 1):
        moving_averages.append(None)

    for i in range(window_size - 1, len(data)):
        window_sum = sum([d['Close'] for d in data[i - window_size + 1:i + 1]])
        moving_average = window_sum / window_size
        moving_averages.append(moving_average)

    for i, d in enumerate(data):
        d['Moving Average'] = moving_averages[i - window_size + window_size]

    return data
def calculate_moving_average200(data):
    window_size = 100  # change this to adjust the moving average window size
    moving_averages = []
    for i in range(window_size - 1):
        moving_averages.append(None)

    for i in range(window_size - 1, len(data)):
        window_sum = sum([d['Close'] for d in data[i - window_size + 1:i + 1]])
        moving_average = window_sum / window_size
        moving_averages.append(moving_average)

    for i, d in enumerate(data):
        d['Moving Average200'] = moving_averages[i - window_size + window_size]

    return data
def calculate_moving_average300(data):
    window_size = 300  # change this to adjust the moving average window size
    moving_averages = []
    for i in range(window_size - 1):
        moving_averages.append(None)

    for i in range(window_size - 1, len(data)):
        window_sum = sum([d['Close'] for d in data[i - window_size + 1:i + 1]])
        moving_average = window_sum / window_size
        moving_averages.append(moving_average)

    for i, d in enumerate(data):
        d['Moving Average300'] = moving_averages[i - window_size + window_size]

    return data

years = [1502798400000]# 1514764800000, 1546300800000, 1577836800000, 1609459200000,1640995200000
for year in years:
    yearEndingCash = []
    startTime = year
    blankTime = year 
    subDir = "MA-4h-V1"
    pct = "pct1"
    directoryYear = datetime.fromtimestamp(startTime/1000.0).strftime('%y')
    try:
        parent_dir = ""
        directory = f"{subDir}"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
    except Exception as e:
        print(e)
        pass
    try:
        parent_dir = f"\\{directory}"
        directory = f"Y{directoryYear}"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
    except Exception as e:
        print(e)
        pass
    try:
        parent_dir = f"\\{subDir}\\{directory}"
        directory = f"{pct}"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
    except Exception as e:
        print(e)
        pass
    def get1mLean():
        global positions, close, positionsPerpetual, pct, directoryYear, subDir, startTime, blankTime, ma300Touched
        for number in range(0, 1):
            dirTime = startTime 
            tp = 0
            sl = 0
            close = []
            positions = []
            positionsPerpetual = []
            directoryDate = datetime.fromtimestamp(dirTime/1000.0).strftime('%d-%m-%y')
            directory = f"{directoryDate}"
            # Parent Directory path
            parent_dir = f"\\{subDir}\\Y{directoryYear}\\{pct}"
            # Path
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)
            portfolioColumns = ["Date", "Starting Balance", "Profits Taken", "Stops Taken", "Ending Balance"]
            portfolioDf = pd.DataFrame(columns=portfolioColumns)

            tradesColumns = ['Side', 'Size', 'Price', 'Date', 'Id', 'PriceToTakeProfit', 'PriceToStopLoss', "TP or SL"]
            tradesDf = pd.DataFrame(columns=tradesColumns)
            timestamp = []
            high = []
            low = []
            open = []
            close = []
            volume = []
            ma = []
            ma2 = []
            ma3 = []
            dataDict = []
            ma300Touched = True
            openPosition = 0
            tradeIv = "85"
            ################################################################################################



            for numbers in range(0, 75):
                #datesToLoop.append(startTime)
                url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=180&startTime={startTime}"
                data = requests.get(url).json()
                for kline in data:
                    dictionary = {"Date": int(kline[0]), "Open": float(kline[1]), "High":float(kline[2]), "Low":float(kline[3]), "Close":float(kline[4]), "Volume":float(kline[5]), "Pump Score": 0, "Dump Score": 0, "Significance": None, "Index": None, "Traded": False}
                    dataDict.append(dictionary)
                    timestamp.append(str(datetime.fromtimestamp(int(kline[0])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S'))) #timestamp.append(str(datetime.fromtimestamp(int(kline[0])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                    open.append(float(kline[1]))
                    high.append(float(kline[2])) 
                    low.append(float(kline[3])) 
                    close.append(float(kline[4]))
                    volume.append(float(kline[5]))
                nextTime = 14400000 * 180 + startTime
                startTime = nextTime
            dataDict = calculate_moving_average(dataDict)
            dataDict = calculate_moving_average200(dataDict)
            dataDict = calculate_moving_average300(dataDict)
            for avg in dataDict:
                ma.append(avg["Moving Average"])
                ma2.append(avg["Moving Average200"])
                ma3.append(avg["Moving Average300"])

            cash_values = []
            cash_timestamps = []

            figure1 = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.8, 0.2], vertical_spacing=0.01,
                subplot_titles=("BTCUSDT 15m Candlestick Chart", "Cash Value"))
            figure1.add_trace(chart.Candlestick(x=timestamp, open=open, high=high, low=low, close=close), row=1, col=1)
            figure1.add_trace(chart.Scatter(x=timestamp, y=ma, line=dict(color='red', width=1)), row=1, col=1)
            figure1.add_trace(chart.Scatter(x=timestamp, y=ma2, line=dict(color='lightgrey', width=1)), row=1, col=1)
            figure1.add_trace(chart.Scatter(x=timestamp, y=ma3, line=dict(color='white', width=1)), row=1, col=1)

            
            figure1.update_layout(
                title="BTCUSDT 15m Candlestick Chart",
                yaxis_title="Price",
                plot_bgcolor="black",
                paper_bgcolor="black",
                xaxis_rangeslider_visible=False,
                xaxis=dict(
                    tickmode="auto",
                    nticks=30,
                    gridcolor="rgba(0, 0, 0, 0)",
                    tickfont=dict(color="white"),
                    title_font=dict(color="white")
                ),
                yaxis=dict(
                    gridcolor="rgba(0, 0, 0, 0)",
                    tickfont=dict(color="white"),
                    title_font=dict(color="white")
                ),
                xaxis2=dict(
                    tickmode="auto",
                    nticks=30,
                    gridcolor="rgba(0, 0, 0, 0)",
                    tickfont=dict(color="white"),
                    title_font=dict(color="white")
                ),
                yaxis2=dict(
                    gridcolor="rgba(0, 0, 0, 0)",
                    tickfont=dict(color="white"),
                    title_font=dict(color="white")
                ),
                title_font=dict(color="white"),
                legend=dict(font=dict(color="white")),
                margin=dict(t=50, b=50, l=50, r=50)
            )


            score = 0
            priceIndex = 0
            for minute in dataDict:
                minute["Index"] = priceIndex
                priceIndex += 1
                if (minute["Moving Average"] != None) and (minute["Moving Average200"] != None) and (minute["Moving Average300"] != None):
                    if (minute["Moving Average200"] * 0.085) >= abs(minute["Moving Average200"] - minute["Moving Average"]) >= (minute["Moving Average200"] * 0.07) and (minute["Moving Average300"] * 0.3) >= abs(minute["Moving Average300"] - minute["Moving Average"]):
                        size = round((1000000 * 1)/round(minute["Close"]))
                        if minute["High"] < minute["Moving Average200"] and minute["Moving Average200"] < minute["Moving Average300"]:#and ma300Touched == True
                            sell(priceToSell=round(minute["Close"]), date=minute["Date"], size=size, iv=tradeIv, tpmult=0.9, slmult=1.1)
                        if minute["Low"] > minute["Moving Average200"]  and minute["Moving Average200"] > minute["Moving Average300"]:#and ma300Touched == True
                            buy(priceToBuy=round(minute["Close"]), date=minute["Date"], size=size, iv=tradeIv, tpmult=1.1, slmult=0.9)

                if positionsPerpetual != []:
                    for position in positionsPerpetual:
                        if position["Side"] == "Long":
                            if position["tpOrSl"] == None:
                                if minute["Open"] > minute["Close"]:
                                    if (position["PriceToTakeProfit"] <= minute["High"]) and (minute["Date"] > position["Date"]):                    
                                        sell(priceToSell=position["PriceToTakeProfit"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="tp")
                                    else:
                                        if (position["PriceToStopLoss"] >= minute["Low"]) and (minute["Date"] >= position["Date"]):
                                            sell(priceToSell=position["PriceToStopLoss"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="sl")
                                else:
                                    if (position["PriceToStopLoss"] >= minute["Low"]) and (minute["Date"] > position["Date"]):
                                        sell(priceToSell=position["PriceToStopLoss"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="sl")
                                    else:
                                        if (position["PriceToTakeProfit"] <= minute["High"]) and (minute["Date"] >= position["Date"]):       
                                            sell(priceToSell=position["PriceToTakeProfit"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="tp")
                        if position["Side"] == "Short":
                            if position["tpOrSl"] == None:
                                if minute["Open"] < minute["Close"]:
                                    if (position["PriceToTakeProfit"] >= minute["Low"]) and (minute["Date"] > position["Date"]):
                                        buy(priceToBuy=position["PriceToTakeProfit"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="tp")
                                    else:
                                        if (position["PriceToStopLoss"] <= minute["High"]) and (minute["Date"] >= position["Date"]):
                                            buy(priceToBuy=position["PriceToStopLoss"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="sl")
                                else:
                                    if (position["PriceToStopLoss"] <= minute["High"]) and (minute["Date"] > position["Date"]):
                                        buy(priceToBuy=position["PriceToStopLoss"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="sl")
                                    else:
                                        if (position["PriceToTakeProfit"] >= minute["Low"]) and (minute["Date"] >= position["Date"]):
                                            buy(priceToBuy=position["PriceToTakeProfit"], Id=position["Id"], reduceOnly=True, size=position["Size"], tpsldate=minute["Date"], tpOrSl="tp")
            perpIndex = 0
            openPositions = 0
            positionsPerpetualSorted = sorted(positionsPerpetual, key=lambda d: (d['Date'], -d['Price'] if d['Side'] == 'Long' else d['Price']))
            for num in range(len(positionsPerpetualSorted)):
                for i in range(len(positionsPerpetualSorted)):
                    if positionsPerpetualSorted[i]["Date"] <= blankTime:
                        del positionsPerpetualSorted[i]
                        break
            for perp in positionsPerpetualSorted: 
                for closedP in positionsPerpetualSorted[perpIndex:]:
                    try:
                        if perp["tpSlDate"] >= closedP["Date"]:
                            openPositions += 1
                            if openPositions > 1:
                                positionsPerpetualSorted.remove(closedP)
                        else:
                            openPositions = 0
                            break
                    except Exception as e:
                        print(e)
                        positionsPerpetualSorted.remove(closedP)
                        pass
                perpIndex += 1
            cash = 1000000
            portfolioDf.at[0, "Starting Balance"] = cash 
            for perp in positionsPerpetualSorted:
                if perp["Side"] == "Short":
                    cash = cash + (perp["Size"] * perp["Price"])
                    cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                    cash_values.append(cash)
                    figure1.add_trace(chart.Scatter(
                        x=[str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S'))],
                        y=[perp["Price"]],
                        mode="markers+text",
                        marker=dict(symbol='star-triangle-down-open', size= 25, color= 'red')))
                    if perp["tpOrSl"] == "sl":
                        sl += 1
                        cash = cash - (perp["Size"] * perp["PriceToStopLoss"])
                        cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                        cash_values.append(cash)
                        figure1.add_trace(chart.Scatter(
                            x=[str(datetime.fromtimestamp(int(perp["tpSlDate"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S'))],
                            y=[perp["PriceToStopLoss"]],
                            mode="markers+text",
                            marker=dict(symbol='x', size= 25, color= 'red')))
                    if perp["tpOrSl"] == "tp":
                        tp += 1
                        cash = cash - (perp["Size"] * perp["PriceToTakeProfit"])
                        cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                        cash_values.append(cash)
                        figure1.add_trace(chart.Scatter(
                            x=[str(datetime.fromtimestamp(int(perp["tpSlDate"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S'))],
                            y=[perp["PriceToTakeProfit"]],
                            mode="markers+text",
                            marker=dict(symbol='cross', size= 25, color= 'green')))
                    if perp["tpOrSl"] == None:
                        cash = cash - (perp["Size"] * close[-1])
                        cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                        cash_values.append(cash)
                if perp["Side"] == "Long":
                    cash = cash - (perp["Size"] * perp["Price"])
                    cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                    cash_values.append(cash)
                    figure1.add_trace(chart.Scatter(
                        x=[str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S'))],
                        y=[perp["Price"]],
                        mode="markers+text",
                        marker=dict(symbol='star-triangle-up-open', size= 25, color= 'green')))
                    if perp["tpOrSl"] == "sl":
                        sl += 1
                        cash = cash + (perp["Size"] * perp["PriceToStopLoss"])
                        cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                        cash_values.append(cash)
                        figure1.add_trace(chart.Scatter(
                            x=[str(datetime.fromtimestamp(int(perp["tpSlDate"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S'))],
                            y=[perp["PriceToStopLoss"]],
                            mode="markers+text",
                            marker=dict(symbol='x', size= 25, color= 'red')))
                    if perp["tpOrSl"] == "tp":
                        tp += 1
                        cash = cash + (perp["Size"] * perp["PriceToTakeProfit"])
                        cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                        cash_values.append(cash)
                        figure1.add_trace(chart.Scatter(
                            x=[str(datetime.fromtimestamp(int(perp["tpSlDate"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S'))],
                            y=[perp["PriceToTakeProfit"]],
                            mode="markers+text",
                            marker=dict(symbol='cross', size= 25, color= 'green')))
                    if perp["tpOrSl"] == None:
                        cash = cash + (perp["Size"] * close[-1])
                        cash_timestamps.append(str(datetime.fromtimestamp(int(perp["Date"])/1000, tz=None).strftime('%Y-%m-%d %H.%M.%S')))
                        cash_values.append(cash)
                tradesDf.loc[len(tradesDf.index)] = [perp["Side"], perp["Size"], perp['Price'] , perp['Date'], perp['Id'], perp['PriceToTakeProfit'], perp['PriceToStopLoss'], perp['tpOrSl']]
            print(cash)
            # Add the cash value trace
            figure1.add_trace(chart.Scatter(x=cash_timestamps, y=cash_values, line=dict(color='orange', width=1)), row=2, col=1)
            figure1.update_yaxes(showgrid=False, row=2, col=1)  # Removes horizontal grid lines for the subplot at row 2, col 1
            figure1.update_xaxes(showgrid=False, row=2, col=1)  # Removes vertical grid lines for the subplot at row 2, col 1

            portfolioDf.at[0, "Ending Balance"] = cash 
            portfolioDf.at[0, "Profits Taken"] = tp 
            portfolioDf.at[0, "Stops Taken"] = sl
            portfolioFile = 'Portfolio.csv'
            tradesFile = 'Trades.csv'
            figureFile = f'Candlestick{year}.html'
            portfolioDf.to_csv(rf"{parent_dir}\{directory}\{portfolioFile}", index=False)
            tradesDf.to_csv(rf"{parent_dir}\{directory}\{tradesFile}", index=False)
            figure1.write_html(rf"{parent_dir}\{directory}\{figureFile}")
            yearEndingCash.append(cash-1000000)
            print("Year Ending Profits:", sum(yearEndingCash))
    get1mLean()
