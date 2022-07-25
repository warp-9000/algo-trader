from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np

from utils import *
from plots import *
from broker import *
from strategies import *
from prompts import *
from plots import *

import _config

# ==================================================================================================
# global variables
# ==================================================================================================

DEFAULT_STARTING_CASH = 100000
DEFAULT_COMMISION = 0.002          # not currently used
DEFAULT_ORDER_SIZE = 1

stock_options = [
	'SPY','QQQ','AAPL','AMZN','GOOG','META','MSFT','NFLX'
]

stock = "SPY"
strategy = "Donchian's Four Weel Rule"



# ==================================================================================================
# core applicaiton functions
# ==================================================================================================

# --------------------------------------------------------------------------------------------------
# function to initialize the application
# returns the core dataframes that will be used
def initialize_application(stock_choice='SPY', strategy_choice="Donchian's Four Weel Rule", save_results_choice=False):

	if DEBUG:
		print(f'init app ------- stock choice: {stock_choice}, strat choice: {strategy_choice}, save result choice: {save_results_choice}')

	global stock
	stock = stock_choice

	if DEBUG:
		print(f'init app ------- stock is: {stock}')

	global strategy
	strategy = strategy_choice

	if DEBUG:
		print(f'init app ------- strat is: {strategy}')

	stock_data = load_data(stock)
	# stocks = download_stock_data('QQQ')

	# ----------------------------------------------------------------------------------------------
	SPY_COLUMNS = list(stock_data.columns)		# <-- saving this for general reference

	# ----------------------------------------------------------------------------------------------
	# convert a 'datetime' <string> to a python datetime 'timestamp' <float>
	stock_data['Date'] = stock_data.Date.apply(lambda x: datetime.fromisoformat(x).timestamp())

	# ------------------------------------------------------
	if DEBUG:
		print('STOCK')
		print('STOCK COLUMNS', SPY_COLUMNS)
		print(stock_data.head(10))
		print()
	# ------------------------------------------------------

	broker, orders, positions = initialize_broker(
		stock_data.Date[0],
		DEFAULT_STARTING_CASH,
		DEFAULT_STARTING_CASH)

	return broker, orders, positions, stock_data

# --------------------------------------------------------------------------------------------------
# function to build the  to prepare the strategy output for plotting
# returns plot-ready dataframes
def generate_plotting_data(broker, positions, stock_data, save_results_choice=False):
	'''
		TODO: isolate the stock data we want to graph, then
		TODO: re-convert the POSIX 'timestamp' <float> values back to the 'datetime' <string>s
	'''

	'''TODO: to get the stock data we want to graph, isolate the following...
	- date
	- stock price
	- high/low indicator, and
	- buy/sell signals'''

	# an explicit copy of everything but Volume
	stock_plot_df = stock_data[['Date','Open','High','Low','Close','Indicator_1','Indicator_2','BuySignal','SellSignal']].copy()
	
	# we could be calling this instead, but let's not bloat the CSV files right now
	# stock_plot_df = stock_data.copy()

	# convert a datetime POSIX 'timestamp' <float> back to a 'datetime' <string>
	stock_plot_df.Date = stock_plot_df.Date.apply(lambda x: datetime.fromtimestamp(x))

	'''TODO: to get the profit and loss for our trades, isolate the following...
		- date
		- realized gain
	'''
	# isolate the data we want to graph
	trade_plot_df = positions[['Date','Realized']].copy()
	# converte the datetime POSIX 'timestamp' <float> back to a 'datetime' <string>
	trade_plot_df.Date = trade_plot_df.Date.apply(lambda x: datetime.fromtimestamp(x))
	# separate the positive and negative trades
	trade_plot_df['Positive'] = trade_plot_df[trade_plot_df['Realized']>0].Realized
	trade_plot_df['Negative'] = trade_plot_df[trade_plot_df['Realized']<=0].Realized
	# drop the realized data
	trade_plot_df.drop('Realized',axis=1,inplace=True)

	'''TODO: to get the brokage cash and value over time, isolate the following...
		- Date,
		- TotalCash, 
		- TotalValue
		...which is what's in the broker dataframe anyway, so let's just copy it for now.
	'''
	# isolate the data we want to graph
	broke_plot_df = broker.copy()

	# converte the datetime POSIX 'timestamp' <float> back to a 'datetime' <string>
	broke_plot_df.Date = broke_plot_df.Date.apply(lambda x: datetime.fromtimestamp(x))

	# print 
	if DEBUG:
		print('------------------------------------------------------------')
		print('---- STOCK DATA ---------')
		print(stock_plot_df.tail(25))
		print('---- TRADING PROFIT -----')
		print(trade_plot_df.tail(25))
		print('---- BROKERAGE VALUE ----')
		print(broke_plot_df.tail(25))
		print('------------------------------------------------------------')

	# save the results if wanted
	if (save_results_choice):
		'''save the results for later review / reuse'''
		save_data(stock_plot_df, 'data', stock+'_'+STRATEGIES[strategy]['name']+'_plot_stock_data.csv')
		save_data(trade_plot_df, 'data', stock+'_'+STRATEGIES[strategy]['name']+'_plot_trade_data.csv')
		save_data(broke_plot_df, 'data', stock+'_'+STRATEGIES[strategy]['name']+'_plot_broke_data.csv')

	return broke_plot_df, trade_plot_df, stock_plot_df



# ==============================================================================================
# main loop
# ==============================================================================================
def main():

	contine_program_choice = True

	while contine_program_choice:
		
		'''
		1. display the welcome message
		2. ask the user what stock data to use
		3. ask the user what strategy to use
		4. ask the user to save the results
		5. then initialize the application
		6. execute the strategy on the stock data selected
		7. generate data to graph the results
		   ...and save the results if wanted
		8. display the graph
		9. ask the user to continue
		'''

		# print a welcome message for the user
		welcome_message()

		# get the user's stock choice
		stock_choice = prompt_multiple_choice(
			"Please select the stock data you wish to use:",
			stock_options
		)
		if DEBUG:
			print(f'Your stock choice was: {stock_choice}\n')

		strategy_options = list(STRATEGIES.keys())
		# get the user's strategy choice
		strategy_choice = prompt_multiple_choice(
			"Please select the strategy you wish to use:",
			strategy_options
		)
		if DEBUG:
			print(f'Your strategy choice was: {strategy_choice}\n')


		# ask the user to save their results or not
		save_results_choice = prompt_single_choice(
			"Would you like to save the results from running this strategy?"
		)
		if DEBUG:
			print(f'Your save results choice was: {save_results_choice}\n')

		# initialize the application
		broker, orders, positions, stock_data = initialize_application(stock_choice, strategy_choice, save_results_choice)

		# run the strategy on the stock data chosen
		# I know this could probably be clearned up but gonna leave it as is for now
		if strategy_choice == "Donchian's Four Weel Rule":
			broker, orders, positions, stock_data = execute_donchians_strategy(broker, orders, positions, stock_data)

		elif strategy_choice == "Dreyfus's 52 Week Rule":
			broker, orders, positions, stock_data = execute_dreyfus_strategy(broker, orders, positions, stock_data)

		elif strategy_choice == "Golden Cross 20v200 SMA":
			broker, orders, positions, stock_data = execute_golden_cross_strategy(broker, orders, positions, stock_data)

		else:
			print(f'Strategy \'{strategy_choice}\' does not exist, misspelled?')
			assert(f'Strategy \'{strategy_choice}\' is not implemented, please select the correct strategy. :)')

		# generate graph data from the output
		stock_plot_df, trade_plot_df, broke_plot_df = generate_plotting_data(
			broker, positions, stock_data, save_results_choice)

		# plot the data
		plot_graph(
			broke_plot_df, trade_plot_df, stock_plot_df, 
			stock, strategy, 
			STRATEGIES[strategy_choice]['ind_1'], 
			STRATEGIES[strategy_choice]['ind_2'],
			save_results_choice
		)

		# ask the user to continue running the program, or quit
		contine_program_choice = prompt_single_choice(
			"Would you like to continue?"
		)
	
	return None



# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
