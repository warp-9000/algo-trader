from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
# import hvplot.pandas



# ==================================================================================================
# global variables
# ==================================================================================================

DEFAULT_STARTING_CASH = 100000
DEFAULT_COMMISION = 0.002          # not currently used
DEFAULT_ORDER_SIZE = 1

broker_cash = 0
broker_value = 0


# --------------------------------------------------------------------------------------------------
ORDER_COLUMNS = ['Date','Type','Size','Status']
orders = pd.DataFrame(
	columns = ORDER_COLUMNS
)
# orders.set_index('idx',inplace=True)

print('ORDERS')
print('ORDER COLUMNS', ORDER_COLUMNS)
print(orders.head())
print()
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
POSITION_COLUMNS = ['Date','Position','Price','Cost','Type','Status','Unrealized','Realized']
positions = pd.DataFrame(
	columns = POSITION_COLUMNS
)
# positions.set_index('Date',inplace=True)

print('POSITIONS')
print('POSITION COLUMNS', POSITION_COLUMNS)
print(positions.head())
print()
# --------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------
spy_df = pd.read_csv(
	Path('data/SPY.csv'),
	# index_col='Date', 
	parse_dates=True,
	infer_datetime_format=True
)
SPY_COLUMNS = list(spy_df.columns)

# convert a 'datetime' <string> to a python datetime 'timestamp' <float>
spy_df.Date = spy_df.Date.apply(lambda x: datetime.fromisoformat(x).timestamp())

print('SPY')
print('SPY COLUMNS', SPY_COLUMNS)
print(spy_df.head(10))
print()
# --------------------------------------------------------------------------------------------------

(# print(f'spy_df.Date[0] = {spy_df.Date[0]}')
# print(f'type(spy_df.Date[0]) = {type(spy_df.Date[0])}')

# --------------------------------------
# converting a datetime <string> to a Pandas Timestamp <object>
# print(f'pd.Timestamp() = {pd.Timestamp(spy_df.Date[0])}')
# print(f'type(pd.Timestamp(spy_df.Date[0])) = {type(pd.Timestamp(spy_df.Date[0]))}')
# --------------------------------------

# --------------------------------------
# convert a 'datetime' <string> to a python datetime 'timestamp' <float>
# spy_df.Date = spy_df.Date.apply(lambda x: datetime.fromisoformat(x).timestamp())

# display(spy_df.head())
# print(spy_df.Date[0])
# print( type (spy_df.Date[0]) )
# --------------------------------------

# --------------------------------------
# these functions only operate on Pandas Timestamp <object>s
# spy_df['Date'] = spy_df['Date'].dt.strftime('%Y-%m-%d')
# spy_df['Date'] = spy_df['Date'].dt.timestamp()
# --------------------------------------

# --------------------------------------
# convert a datetime <float> to a Pandas Timestamp <object>
# spy_df.Date = spy_df.Date.apply(lambda x: datetime.fromtimestamp(x))

# display(spy_df.head())
# print(spy_df.Date[0])
# print( type (spy_df.Date[0]) )
# --------------------------------------


# how to select a row using pandas.DataFrame.loc[] when using multiple conditions
# row = spy_df.loc[(spy_df['Volume']==8089800) & (spy_df['Date']==946972800.0)]
# print(row)
# row_idx = spy_df.loc[(spy_df['Volume']==8089800) & (spy_df['Date']==946972800.0)].index[0]
# print(row_idx)
# rows = spy_df.loc[(spy_df.Date==947059200.0) | (spy_df.Date==947232000.0) | (spy_df.Date==947664000.0)]
# rows = spy_df.loc[(spy_df.Date==0.0) | (spy_df.Date==0.0) | (spy_df.Date==0.0)]
# print(rows)
# print(len(rows))
# for i in range(0,len(rows)):
# 	print(rows.index[i])
)




# ==================================================================================================
# initializing data
# ==================================================================================================

spy_df['RollingHigh'] = spy_df['Close'].rolling(20).max()
spy_df['RollingLow'] = spy_df['Close'].rolling(20).min()
spy_df['BuySignal'] = np.NaN
spy_df['SellSignal'] = np.NaN
print(spy_df.head())




# ==================================================================================================
# key functions
# ==================================================================================================

def execute_order(execution_date,current_price,order_size,order_type):
	"""TODO: a summary fo what this function does
	
	TODO: add a detailed description if necessary
	
	Parameters
	----------
	TODO: update the list of parameters
	
	df : pandas.DataFrame (required)
		A OHLC dataframe containing the pricing data related to this order.
	i : int (required)
		'i' is the row in 'df' which contains price info relevant for this order.
	size : int (required)
		The size of the order / number of shares to be bought or sold.
	otype : str (required)
		The type of order to execute: "buy", "sell", or "close".
	
	Returns
	-------
	TODO: update the return value
	"""
	
	
	# ----------------------------------------------------------------------------------------------
	# TODO: we can probably add more comments in this code
	# TODO: we probably want to refactor this code because the 'buy' and 'sell' execution is
	#       completely different from the 'close' execution
	# TODO: include 'commision' so we can account for additional loss per trade execution
	# ----------------------------------------------------------------------------------------------
	
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display some details about this order execution
	print(f'execute order: {order_type}; date: {execution_date}; price: {current_price}; size: {order_size}')
	
	# DELETE ME -- these were the prior details I printed 
	# print('execute order =', otype, '; size =', size, '; i =', i)
	
	# DELETE ME -- I've stopped specifying an index for the dataframe
	# get the date from the provided dataframe
	# date = df.index.values[i]
	# date = df.Date[i]
	
	# TODO: do we want to keep this comment around?
	"""This function does two things
	1. it executes a 'buy' or 'sell' order - ie. it adds an 'open' position to the positions dataframe.
	2. it executes a 'close' order - ie. it modifies the 'open' position in the positions dataframe so that it's 'closed'
	"""
	
	# ----------------------------------------------------------------------------------------------
	# execute the 'buy' or 'sell' by adding a new 'long' or 'short' position
	if (order_type=='buy') or (order_type=='sell'):
		
		# set the position size and position type based on the order type
		
		if order_type=='buy':
			position=order_size
			position_type='long'
		else:
			position=order_size * -1
			position_type='short'
		
		# create the position data
		cost = current_price * order_size
		status = 'open'
		unrealized = 0.0
		realized = 0.0
		
		data = [
			execution_date,
			position,
			current_price,
			cost,
			position_type,
			status,
			unrealized,
			realized
		]
		
		# REPLACE ME -- this comment and print() should be a log statement
		# display the order data we just created
		print(f'execution data: [date: {execution_date}; position: {position}; price: {current_price}; cost: {cost}; type: {position_type}; status: {status}; unrealized: {unrealized}; realized: {realized}]')
		print(f'execution data: {data}')
		
		# DELETE ME -- save the new position in a dataframe
		# position = pd.DataFrame(
		# 	[data],
		# 	columns=POSITION_COLUMNS
		# )
		
		# DELETE ME -- I've stopped specifying an index for the dataframe
		# position.set_index('Date',inplace=True)
		
		# DELETE ME -- concatenate the new order to the orders dataframe
		# positions = pd.concat([positions, position])
		
		# insert the new position at the end of the current dataframe
		positions.loc[len(positions)] = data
	
	# ----------------------------------------------------------------------------------------------
	# execute the 'close' order
	elif (order_type=='close'):
		
		"""Steps Required to Close a Position
		1. update Value based on the current price of the stock
		2. set Position = 0 (because we 'sold'/'bought' all the stock)
		3. 
		
		Reminder: each position contains these fields
		columns=['Date','Position','Price','Cost','Type','Status','Unrealized','Realized']
		"""
		
		#------------------------------------------------------------
		# STUCK HERE 
		#------------------------------------------------------------
		
		# filter for all 'open' positions
		print('filtering open positions')
		open_positions = positions.loc[positions.Status=='open']
		
		print('# open positions', len(open_positions))
		print(open_positions)
		
		if len(open_positions) == 1 :
			print('there\'s one position \'open\'')
		elif len(open_positions) > 1 :
			#### THIS SHOULD NEVER HAPPEN ###
			print('there\'s multiple positions \'open\'')
		else :
			#### THIS SHOULD NEVER HAPPEN ###
			print('there\'s no positions \'open\'')
		
		# storing the index for the open position
		idx = open_positions.index[0]
		
		order_size = abs(positions.Position[idx])
		
		# reflect the number of shares closed
		
		# if positions.Type[idx]=='long' :
		# 	positions.Position[idx] = positions.Position[idx] - order_size
		# else :
		# 	positions.Position[idx] = positions.Position[idx] + order_size
		
		positions.iloc[idx,1] = 0		# <-- close the full position
		
		# 6 == Unrealized column
		positions.iloc[idx,6] = 0.0		# <-- Unrealized becomes zero

		# 7 == Realized column
		# 3 == Cost column
		# the Realized value = price * size - cost
		positions.iloc[idx,7] = current_price * order_size - positions.iloc[idx,3]
		
		#------------------------------------------------------------
		# STUCK HERE 
		#------------------------------------------------------------
		
		# positions.Status[idx] = 'closed'
		# 5 == Status column
		positions.iloc[idx,5] = 'closed'
	
	# display(positions)
	
	return None

def process_orders(df, df_idx):
	"""The function 'processes' each open order in order to 'fill' that order.
	
	This function filters the 'orders' dataframe for open orders. For every 'open' order, it calls the execute_order() function, and passes 'df' the current stock dataframe, 'i' the active row in that dataframe, the 'size' of the order, and the 'type' of that order. After that we then consider the order 'filled'.
	
	Parameters
	----------
	df : pandas.DataFrame (required)
	i : int (required)
	
	Returns
	-------
	None
	"""
	
	"""Steps Required to Close a Position
	1. filter the orders dataframe for 'open' orders
	2. call execute_order() for each order, passing appropriate information
	3. set the order 'status' field to 'filled'
	
	Reminders...
	- Positions require these fields
		columns=['Date','Position','Price','Cost','Type','Status','Unrealized','Realized']
	- execute_orders require these fields
		positions, execution_date, current_price, order_size, order_type
	
	"""
	
	# get all open orders
	open_orders = orders.loc[orders.Status=='open']
	
	if len(open_orders) < 1 :
		# print(f'no orders to process')
		return None
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display some details about this order execution
	print(f'processing orders; df_idx: {df_idx}; date: {spy_df.Date[df_idx]}; price: {spy_df.Open[df_idx]}; # orders: {len(open_orders)}')
	# display(open_orders)
	
	for i in range(0, len(open_orders)) :
		
		# get order index
		idx = open_orders.index[i]
		
		# REPLACE ME -- this comment and print() should be a log statement
		# print the Type of order we're processing
		print(f'order: {idx}; date: {spy_df.Date[df_idx]}; price: {spy_df.Open[df_idx]}; size: {orders.Size[idx]}; type: {orders.Type[idx]}')
		
		# execute the current order
		# positions = execute_order(spy_df,df_i,positions,orders.iloc[i,1],orders.iloc[i,0])
		# positions = execute_order(spy_df.Date[df_idx], spy_df.Open[df_idx], orders.Size[i], orders.iloc[i,1])
		
		execute_order(spy_df.Date[df_idx], spy_df.Open[df_idx], orders.Size[idx], orders.Type[idx])
		
		# set the current order's status to 'filled'
		# 3 = Status column
		orders.iloc[idx,3] = 'filled'
		
		# display(orders)
	
	return None

def create_order(order_date, order_type, order_size=DEFAULT_ORDER_SIZE):
	"""Creates an order and adds it to the orders dataframe provided.
	
	TODO: add a detailed description if necessary
	
	Parameters
	----------
	orders : <pandas.DataFrame>, required
		The dataframe where add new orders.
	order_date : <float>, required
		The 'datetime' <float> when the order was created.
	order_type : <str>, required
		Type of order: "buy", "sell", or "close".
	order_size : <int>, required
		Size of the order (ie. number of shares to purchase). Fractional shares are not supported.
		Defauls to "DEFAULT_ORDER_SIZE".
	
	Returns
	-------
	orders : <Pandas Dataframe>
		The dataframe which contains our new order.
	"""
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display the order type for this order
	print(f'create order: {order_type}')
	
	# combine the data required for the order
	data = [
		order_date,
		order_type,
		order_size,
		'open'
	]
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display the order data we just created
	print(f'order data: {data}')
	
	# save the new order in a dataframe
	# order = pd.DataFrame(
	# 	[data],
	# 	columns=ORDER_COLUMNS
	# )
	# DELETE ME -- I've stopped specifying an index for the dataframe
	# order.set_index('idx',inplace=True)
	
	# DELETE ME -- concatenate the new order to the orders dataframe
	# orders = pd.concat([orders, order])
	
	orders.loc[len(orders)] = data
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display the updated orders dataframe
	# display(orders)
	
	return None




# ==================================================================================================
# execute strategy
# ==================================================================================================

""" Iterate through len-1 rows
1. process orders
2. check the trading strategy for 'buy' or 'sell' indicators
"""

for i in range(1, len(spy_df)) :
	
	process_orders(spy_df, i)
	
	# get any currently open positions
	open_positions = positions.loc[positions.Status=='open']
	
	# REPLACE ME -- this comment and print() should be a log statement
	# print info about the STOCK_DF that we're processing
	print(f"row = {i}; # open positions = {len(open_positions)}; close: {spy_df.Close[i]}; rol_low: {spy_df.RollingLow[i]}; rol_high: {spy_df.RollingHigh[i]}; ")
	
	# ----------------------------------------------------------------------------------------------
	# Execute our Trading Strategy
	# ----------------------------------------------------------------------------------------------
	"""
		IF no open positions, THEN
			IF no recent buy signals, AND
			the Close price meets the Rolling High
				Create a buy order
				Set the Buy Signal to the Close price
			ELSE IF no recent sell signals, AND
			the Close price meets the Rolling Low
				Create a sell order
				Set the Sell Signal to the Close price
		Else If open positions exist, THEN
			Do the same as above, except
				Create a close order
				Create a buy/sell order (as appropriate)
				Set the Buy/Sell Signal to the Close price
	"""
	
	# ----------------------------------------------------------------------------------------------
	# IF there's NO open positions, THEN...
	if (len(open_positions) <= 0) :
		
		# Confirm there's NO prior buy signal, AND
		# Check if 'Close' has met the 'Rolling High'
		if (np.isnan(spy_df.BuySignal[i-1])) and \
		(spy_df.Close[i]==spy_df.RollingHigh[i]) :
			
			# create a buy order
			# create_order(orders, order_date, order_type, order_size=default_order_size):
			# orders = create_order(orders, spy_df.Date[i], 'buy')
			create_order(spy_df.Date[i], 'buy')
			
			# set Close price -> Buy Signal
			# 9 = BuySignal
			spy_df.iloc[i,9] = spy_df.Close[i]
		
		elif (np.isnan(spy_df.SellSignal[i-1])) and \
		(spy_df.Close[i]==spy_df.RollingLow[i]) :
			
			# create a sell order
			# orders = create_order(orders, spy_df.Date[i], 'sell')
			create_order(spy_df.Date[i], 'sell')
			
			# set Close price -> Sell Signal
			# 10 = SellSignal
			spy_df.iloc[i,10] = spy_df.Close[i]
		
	
	# ----------------------------------------------------------------------------------------------
	# ELSE IF there are open positions, THEN...
	elif (0 < len(open_positions) < 2) :
		
		# print('positions type =', positions.loc[positions['Status']=='open']['Type'])
		pos_idx = open_positions.index[0]

		if (open_positions.Type[pos_idx] is not 'long') and \
		(np.isnan(spy_df.BuySignal[i-1])) and \
		(spy_df.Close[i]==spy_df.RollingHigh[i]) :
			
			# create a close order
			# orders = create_order(orders, spy_df.Date[i], 'close')
			create_order(spy_df.Date[i], 'close')
			
			# create a buy order
			# orders = create_order(orders, spy_df.Date[i], 'buy')
			create_order(spy_df.Date[i], 'buy')
			
			# set Close price -> Buy Signal
			# 9 = BuySignal
			spy_df.iloc[i,9] = spy_df.Close[i]
			
		elif (open_positions.Type[pos_idx] is not 'short') and \
		(np.isnan(spy_df.SellSignal[i-1])) and \
		(spy_df.Close[i]==spy_df.RollingLow[i]) :
			
			# create a close order
			# orders = create_order(orders, spy_df.Date[i], 'close')
			create_order(spy_df.Date[i], 'close')
			
			# create a sell order
			# orders = create_order(orders, spy_df.Date[i], 'sell')
			create_order(spy_df.Date[i], 'sell')
			
			# set Close price -> Sell Signal
			# 10 = SellSignal
			spy_df.iloc[i,10] = spy_df.Close[i]
			
		
	elif (len(open_positions) > 1) :
		print('there\'s mutliple open positions - what do we do???')
	
	#---- end FOR loop



print(orders)
print(positions)
