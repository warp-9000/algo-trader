"""
TODO: describe the purpose of this file
"""

import pandas as pd



# ==================================================================================================
# global variables
# ==================================================================================================

DEBUG = False


# ==================================================================================================
# broker functions
# ==================================================================================================

def initialize_broker(broker, initial_date, cash, value):

	if DEBUG:
		print(f'init broker ---- date: {initial_date}, TotalCash: {cash}, TotalValue: {value}')

	broker.loc[len(broker)] = [initial_date, cash, value]

	return broker


# ==================================================================================================
# core functions
# ==================================================================================================

def execute_order(broker, positions, execution_date, current_price, order_size, order_type):
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
	if DEBUG:
		print(f'execute order -- type: {order_type}, date: {execution_date}, price: {current_price}, size: {order_size}')
	
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
		if DEBUG:
			print(f'execute order -- created position data = [date: {execution_date}, position: {position}, price: {current_price}, cost: {cost}, type: {position_type}, status: {status}, unrealized: {unrealized}, realized: {realized}]')
		# print(f'execute order -- data = {data}')
		
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
		if DEBUG:
			print(f"execute order -- appended position [data]")
		
		# -1 == last row in the dataframe
		# 1 == TotalCash colum
		# 2 == TotalValue column
		# update the brokerage account's cash with the cost of this purchase
		broker.iloc[-1].TotalCash -= cost
		if DEBUG:
			print(f"execute order -- updated broker -- TotalCash: {broker.iloc[-1].TotalCash}")
		# we don't need to update the brokerage account's value because the value of the new
		# position offsets the cash draw down
		# broker.iloc[-1, 2] = broker.iloc[-1, 1] + cost

		return broker, positions

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
		
		# filter for all 'open' positions
		open_positions = positions.loc[positions.Status=='open']
		open_pos_len = len(open_positions)
		if DEBUG:
			print(f'execute order -- filtered open positions')
			print(open_positions)
		
		if open_pos_len == 1 :
			if DEBUG:
				print(f'execute order -- 1 open position')
		elif open_pos_len > 1 :
			#### THIS SHOULD NEVER HAPPEN ###
			if DEBUG:
				print(f'execute order -- {open_pos_len} open positions')
			assert(f'{open_pos_len} open positions - THIS SHOULD NEVER HAPPEN!')
		else :
			#### THIS SHOULD NEVER HAPPEN ###
			if DEBUG:
				print(f'execute order -- {open_pos_len} open positions')
			assert(f'{open_pos_len} open positions - THIS SHOULD NEVER HAPPEN!')
		
		# storing the index for the open position
		idx = open_positions.index[0]
		
		order_size = abs(positions.Position[idx])
		
		# 1 == Position column
		positions.iloc[idx,1] = 0		# <-- close the full position
		
		# 6 == Unrealized column
		positions.iloc[idx,6] = 0.0		# <-- Unrealized becomes zero

		# 7 == Realized column
		# 3 == Cost column
		# the Realized(gain) = (Price * Size) - Cost
		positions.iloc[idx,7] = (current_price * order_size) - positions.iloc[idx].Cost
		
		# 5 == Status column
		positions.iloc[idx,5] = 'closed'

		# -1 == last row in the dataframe
		# 1 == TotalCash colum
		# 2 == TotalValue column
		# update the brokerage account's TotalCash and TotalValue from the proceeds of this transaction
		broker.iloc[-1,1] += positions.Cost[idx] + positions.Realized[idx]
		broker.iloc[-1,2] = broker.iloc[-1].TotalCash
		if DEBUG:
			print(f'execute order -- updated broker -- TotalCash: {broker.iloc[-1].TotalCash}, TotalValue: {broker.iloc[-1].TotalValue}')
		
		# DELETE ME -- NOTE: using .Status[#] creates a copy of the dataframe, so if we assign a value there with "=" then we get a pandas warning printed to the screen
		# positions.Status[idx] = 'closed'
		# DELETE ME ^^^^
		
		return broker, positions
	
	else:
		assert(f'unknown execute order type: {order_type}')

	return broker, positions
	

def process_orders(broker, orders, positions, stocks, stock_idx):
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
	
	# get a copy of all open orders
	open_orders = orders.loc[orders.Status=='open']
	
	# if there's no open orders, then return as there's nothing more to do
	if len(open_orders) < 1 :
		# print(f'no orders to process')
		return broker, orders, positions
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display some details about this order execution
	if DEBUG:
		print(f'process order -- stock idx: {stock_idx}, date: {stocks.Date[stock_idx]}, price: {stocks.Open[stock_idx]}, # orders: {len(open_orders)}')
	# display(open_orders)
	# REPLACE ME --
	
	for i in range(0, len(open_orders)) :
		
		# get order index
		idx = open_orders.index[i]
		
		# REPLACE ME -- this comment and print() should be a log statement
		# print the Type of order we're processing
		if DEBUG:
			print(f'process order -- orders idx: {idx}, date: {spy_df.Date[stock_idx]}, price: {stocks.Open[stock_idx]}, size: {orders.Size[idx]}, type: {orders.Type[idx]}')
		
		# DELETE ME -- we now operate directly on the dataframe instead of passing copies of the dataframe back and forth
		# execute the current order
		# positions = execute_order(spy_df,df_i,positions,orders.iloc[i,1],orders.iloc[i,0])
		# positions = execute_order(spy_df.Date[df_idx], spy_df.Open[df_idx], orders.Size[i], orders.iloc[i,1])
		# DELETE ME --
		
		broker, positions = execute_order(broker, positions, stocks.Date[stock_idx], stocks.Open[stock_idx], orders.Size[idx], orders.Type[idx])
		
		# after we execute the order we then set the current order's status to 'filled'
		# 3 = Status column
		orders.iloc[idx,3] = 'filled'
		
		# display(orders)
	
	return broker, orders, positions

def create_order(orders, order_date, order_type, order_size=1):
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
	if DEBUG:
		print(f'create order --- {order_type}')
	
	# combine the data required for the order
	data = [
		order_date,
		order_type,
		order_size,
		'open'
	]
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display the order data we just created
	if DEBUG:
		print(f'create order --- data = {data}')


	# add the new order as a row at the bottom of the orders dataframe
	orders.loc[len(orders)] = data
	if DEBUG:
		print(f'create order --- appended [data]')
	
	# REPLACE ME -- this comment and print() should be a log statement
	# display the updated orders dataframe
	# display(orders)
	
	return orders

