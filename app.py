from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np

from utils import *
from plots import *
from broker import *
from strategies import *
from plots import *



# ==================================================================================================
# global variables
# ==================================================================================================

DEFAULT_STARTING_CASH = 100000
DEFAULT_COMMISION = 0.002          # not currently used
DEFAULT_ORDER_SIZE = 1

BROKER_COLUMNS = ['Date','TotalCash','TotalValue']
ORDER_COLUMNS = ['Date','Type','Size','Status']
POSITION_COLUMNS = ['Date','Position','Price','Cost','Type','Status','Unrealized','Realized']

DEBUG = True



# ==================================================================================================
# initializing data
# ==================================================================================================

broker = initialize_df(BROKER_COLUMNS)
orders = initialize_df(ORDER_COLUMNS)
positions = initialize_df(POSITION_COLUMNS)

ticker = 'SPY'

# ----
strategy = 'donchian'			# <----- RollingHigh / Rolling Low
# strategy = 'dreyfus'			# <----- RollingHigh / Rolling Low
# ----
# strategy = 'goldencross'      # <----- FastSMA / SlowSMA

stocks = load_data(ticker)
# stocks = download_stock_data('QQQ')

# --------------------------------------------------------------------------------------------------
SPY_COLUMNS = list(stocks.columns)		# <-- saving this for general reference

# --------------------------------------------------------------------------------------------------
# convert a 'datetime' <string> to a python datetime 'timestamp' <float>
stocks['Date'] = stocks.Date.apply(lambda x: datetime.fromisoformat(x).timestamp())

# --------------------------------------------------------------------------------------------------
if DEBUG:
	print('BROKER')
	print('BROKER COLUMNS', BROKER_COLUMNS)
	print(broker.head())
	print()
# --------------------------------------------------------------------------------------------------
	print('ORDERS')
	print('ORDER COLUMNS', ORDER_COLUMNS)
	print(orders.head())
	print()
# --------------------------------------------------------------------------------------------------
	print('POSITIONS')
	print('POSITION COLUMNS', POSITION_COLUMNS)
	print(positions.head())
	print()
# --------------------------------------------------------------------------------------------------
	print('STOCK')
	print('STOCK COLUMNS', SPY_COLUMNS)
	print(stocks.head(10))
	print()
# --------------------------------------------------------------------------------------------------



# ==================================================================================================
# initialize broker
# ==================================================================================================

broker = initialize_broker(broker, stocks.Date[0], DEFAULT_STARTING_CASH, DEFAULT_STARTING_CASH)



# ==================================================================================================
# execute strategy functions
# ==================================================================================================

if strategy == 'donchian':
	broker, orders, positions, stocks = execute_donchians_strategy(broker, orders, positions, stocks, 'RollingHigh', 'RollingLow')

elif strategy == 'dreyfus':
	broker, orders, positions, stocks = execute_dreyfus_strategy(broker, orders, positions, stocks, 'RollingHigh', 'RollingLow')

elif strategy == 'goldencross':
	broker, orders, positions, stocks = execute_golden_cross_strategy(broker, orders, positions, stocks, 'FastSMA', 'SlowSMA')

else:
	print(f'Strategy \'{strategy}\' does not exist, misspelled?')
	assert(f'Strategy \'{strategy}\' is not implemented, please select the correct strategy. :)')

# ==================================================================================================
# prepare the strategy output for plotting
# ==================================================================================================

'''
	TODO: isolate the stock data we want to graph, then
	TODO: re-convert the POSIX 'timestamp' <float> values back to the 'datetime' <string>s
'''

'''TODO: to get the stock data we want to graph, isolate the following...
- date
- stock price
- high/low indicator, and
- buy/sell signals'''

# isolate the data we want to graph -- USE FOR OTHER STRATEGIES --
# stock_plot_df = stocks[['Date','Open','High','Low','Close','RollingHigh','RollingLow','BuySignal','SellSignal','Volume']]

# isolate the data we want to graph -- USE FOR GOLDEN CROSS --


# stock_plot_df = stocks[['Date','Open','High','Low','Close','FastSMA','SlowSMA','BuySignal','SellSignal','Volume']]
stock_plot_df = stocks.copy()

# convert a datetime POSIX 'timestamp' <float> back to a 'datetime' <string>
stock_plot_df.loc[:,'Date'] = stock_plot_df.Date.apply(lambda x: datetime.fromtimestamp(x))

'''TODO: to get the profit / loss for our trades, isolate the following...
- date
- realized gain'''
# isolate the data we want to graph
trade_plot_df = positions[['Date','Realized']]
# converte the datetime POSIX 'timestamp' <float> back to a 'datetime' <string>
trade_plot_df.loc[:,'Date'] = trade_plot_df.Date.apply(lambda x: datetime.fromtimestamp(x))
# separate the positive and negative trades
trade_plot_df.loc[:,'Positive'] = trade_plot_df[trade_plot_df['Realized']>0].Realized
trade_plot_df.loc[:,'Negative'] = trade_plot_df[trade_plot_df['Realized']<=0].Realized
# drop the realized data
trade_plot_df.drop('Realized',axis=1,inplace=True)

'''TODO: to get the brokage cash and value over time, isolate the following...
- Date, TotalCash, TotalValue
...which is all that's in the broker dataframe anyway, so we might as well copy it.
'''
# isolate the data we want to graph
broke_plot_df = broker.copy()
# converte the datetime POSIX 'timestamp' <float> back to a 'datetime' <string>
broke_plot_df.Date = broke_plot_df.Date.apply(lambda x: datetime.fromtimestamp(x))

print('--------------------------------------------------------------------------------')
print('---- STOCK DATA ---------')
print(stock_plot_df.tail(50))
print('---- TRADING PROFIT -----')
print(trade_plot_df.tail(20))
print('---- BROKERAGE VALUE ----')
print(broke_plot_df.tail(50))
print('--------------------------------------------------------------------------------')




# ==================================================================================================
# save / store the results?
# ==================================================================================================

'''TODO: save the results for later review / reuse'''

save_data(stock_plot_df, 'data', ticker+'_'+strategy+'_plot_stock_data.csv')
save_data(trade_plot_df, 'data', ticker+'_'+strategy+'_plot_trade_data.csv')
save_data(broke_plot_df, 'data', ticker+'_'+strategy+'_plot_broke_data.csv')


# ==================================================================================================
# plot the results of the strategy
# ==================================================================================================

if strategy == 'donchian':
	generate_graph(stock_plot_df, trade_plot_df, broke_plot_df, '4 Week High', '4 Week Low')

elif strategy == 'dreyfus':
	generate_graph(stock_plot_df, trade_plot_df, broke_plot_df, '52 Week High', '52 Week Low')

elif strategy == 'goldencross':
	generate_graph(stock_plot_df, trade_plot_df, broke_plot_df, 'Fast SMA', 'Slow SMA')

else:
	print(f'Strategy \'{strategy}\' does not exist, misspelled?')
	assert(f'Strategy \'{strategy}\' is not implemented, please select the correct strategy. :)')


