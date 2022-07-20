# from operator import index
import pandas as pd
import pandas_datareader as pdr
import datetime as dt

DEBUG = False

def load_stock_data(stock_ticker, set_index=False, index_column=''):
	"""load_stock_data() TODO: a summary of what this function does 
	
	TODO: add a detailed description if necessary
	
	Parameters
	----------
	TODO: update the list of parameters
	
	...use this format when listing parameters...
	<variable_name> : <variable_type> (required/optional)
		<variable_description_or_purpose>
	
	...for example...
	df : pandas.DataFrame (required)
		A OHLC dataframe containing the pricing data related to this order.
	
	Returns
	-------
	TODO: specify the return value
	"""

	stock_df = pd.read_csv(
		'data/'+stock_ticker+'.csv', 
	#	index_col='Date', 
		parse_dates=True,
		infer_datetime_format=True
	)
	if (set_index and index_column==''):
		assert(f'load_stock_data() index_column is blank, please provide a column name')
	if (set_index):
		stock_df.set_index(index_column,inplace=True)

	if DEBUG:
		print('---- symbol_df ----')
		print(stock_df.head())
		print(stock_df.tail())

	# ----- DELETE ME AFTER 2022 July 30 ---------------------------------------
	# # convert the first column to a datetime
	# symbol_data.index = pd.to_datetime(symbol_data.index, format='%Y-%m-%d')
	# --------------------------------------------------------------------------

	return stock_df

def download_stock_data(stock_tickers=['SPY'],start_date=dt.datetime(2000,1,1),end_date=dt.datetime.now()):
	"""download_stock_data() TODO: a summary of what this function does 
	
	TODO: add a detailed description if necessary
	
	Parameters
	----------
	TODO: update the list of parameters
	
	...use this format when listing parameters...
	<variable_name> : <variable_type> (required/optional)
		<variable_description_or_purpose>
	
	...for example...
	df : pandas.DataFrame (required)
		A OHLC dataframe containing the pricing data related to this order.
	
	Returns
	-------
	TODO: specify the return value
	"""

	# stock_tickers = ['SPY','QQQ','AAPL','AMZN','GOOG','META','MSFT']
	data = {}
	for ticker in stock_tickers :
		# download the stock data for this ticker
		data[ticker] = pdr.get_data_yahoo(ticker, start_date, end_date, ret_index=True)
		# reset the index so 'Date' becomes a column again
		data[ticker].reset_index(inplace=True)

	return data
