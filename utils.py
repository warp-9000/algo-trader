import pandas as pd

DEBUG = True

def get_stock_data(stock):

	stock_df = pd.read_csv(
		'data/'+stock+'.csv', 
		index_col='Date', 
		parse_dates=True,
		infer_datetime_format=True
	)

	if DEBUG:
		print('---- symbol_df ----')
		print(stock_df.head())
		print(stock_df.tail())

	# ----- DELETE ME AFTER 2020 July 30 ---------------------------------------
	# # convert the first column to a datetime
	# symbol_data.index = pd.to_datetime(symbol_data.index, format='%Y-%m-%d')
	# --------------------------------------------------------------------------

	return stock_df
