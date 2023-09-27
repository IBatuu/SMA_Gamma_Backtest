# SMA_Gamma_Backtest

This is a backtesting script that doesn't utilize any backtesting libraries (quantconnect etc.) and instead has its own backtesting engine. This is primarily to avoid data restriction, faster backtesting without spending money, and to be able to use plotly. Free backtesting engines tend to not have long-term support so relying on them can bring problems in the future. The best alternative would be the quantconnect backtesting engine but to have a reliable and fast service, you need to pay multiple subscription fees monthly as well as you need to use their own charting methods.

###How the script works

This script has two different branches:
1) One is a general backtesting part that includes the buy, sell, and addPosition functions. Using these functions, some part of the script backtestest the outcomes of the positions and returns them into csv files, and creates a graph for that period as well as a position's csv file. Additionally, there is a loop for gathering the historical prices for the backtesting. This is not recommended as it significantly increases the duration of a backtest. Instead, creating your own database would be suggested.

2) The second and project-specific part of this script is the trigger functions such calculation of moving averages and when to trigger them.

Notes

Although the backtesting script works flawlessly, it needs to be arranged and beautified (using classes and more functions etc.) and added a db support instead of the api fetching.

