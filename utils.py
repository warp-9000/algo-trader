import datetime as dt
import pandas as pd
import pandas_datareader as pdr
from pathlib import Path



# ==================================================================================================
# global variables
# ==================================================================================================

DEBUG = True



# ==================================================================================================
# core functions
# ==================================================================================================
def initialize_df(column_names, set_index=False, index_column=''):

	df = pd.DataFrame(
		columns=column_names
	)
	if (set_index and index_column==''):
		assert(f'load_data() -> index_column is blank, please provide the correct column name')
	if (set_index):
		df.set_index(index_column,inplace=True)

	return df

# --------------------------------------------------------------------------------------------------
def download_stock_data(
	ticker='SPY',
	start_date=dt.datetime(2000,1,1),
	end_date=dt.datetime.now()):

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
	# stock_df = {}
	# for ticker in stock_tickers :
	# 	# download the stock data for this ticker
	# 	stock_df[ticker] = pdr.get_data_yahoo(ticker, start_date, end_date, ret_index=True)
	# 	# reset the index so 'Date' becomes a column again
	# 	stock_df[ticker].reset_index(inplace=True)

	stock = pdr.get_data_yahoo(ticker, start_date, end_date, ret_index=True)
	# reset the index so 'Date' becomes a column again
	stock.reset_index(inplace=True)

	if DEBUG:
		print()
		print(stock.head(20))
	
	#  stock.to_csv(Path('data/'+ticker+'.csv'))

	return stock


# --------------------------------------------------------------------------------------------------
def load_data(data, set_index=False, index_column=''):
	"""load_data() TODO: a summary of what this function does 
	
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

	data_df = pd.read_csv(
		'data/'+data+'.csv', 
	#	index_col='Date', 
		parse_dates=True,
		infer_datetime_format=True
	)
	if (set_index and index_column==''):
		assert(f'load_data() -> index_column is blank, please provide the correct column name')
	if (set_index):
		data_df.set_index(index_column,inplace=True)

	if DEBUG:
		print('---- symbol_df ----')
		print(data_df.head())
		print(data_df.tail())

	return data_df


# --------------------------------------------------------------------------------------------------
def save_data(df, dir='data', filename='file.csv'):
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

	result = df.to_csv(Path(dir+'/'+filename))
	print(f'save_data ------ result: {result}')

	return None

