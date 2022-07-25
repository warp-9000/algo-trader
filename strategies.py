import numpy as np
from broker import *

from _config import *


# ==================================================================================================
# global variables
# ==================================================================================================

''' moved to _config.py
DEBUG = True
'''

STRATEGIES = {
	"Donchian's Four Weel Rule" : {
		'name' : 'donchian',
		'text' : "Donchian's Four Weel Rule",
		'ind_1' : '4 Week High', 
		'ind_2' : '4 Week Low',
	},
	"Dreyfus's 52 Week Rule" : {
		'name' : 'dreyfus',
    	'text' : "Dreyfus's 52 Week Rule",
		'ind_1' : '52 Week High', 
		'ind_2' : '52 Week Low',
	},
	"Golden Cross 20v200 SMA" : {
		'name' : 'goldencross',
    	'text' : "Golden Cross 20v200 SMA",
		'ind_1' : 'Fast SMA', 
		'ind_2' : 'Slow SMA',
	},
}




# ==================================================================================================
# define one function per strategy
# ==================================================================================================

""" Iterate through len-1 rows
1. process orders
2. check the trading strategy for 'buy' or 'sell' indicators
"""

'''    STRATEGY 1    '''
def execute_donchians_strategy(broker, orders, positions, stocks):

	weekly_rolling_high = 20 # 20 periods is ~4 weeks
	weekly_rolling_low  = 20 # same as above

	# generate rolling highs and lows
	stocks['Indicator_1'] = stocks['Close'].rolling(weekly_rolling_high).max()
	stocks['Indicator_2'] = stocks['Close'].rolling(weekly_rolling_low).min()

	# generate buy / sell signal columns
	stocks['BuySignal'] = np.NaN
	stocks['SellSignal'] = np.NaN

	# iterate over the dataframe starting with the second row
	for i in range(1, len(stocks)) :

		# ------------------------------------------------------------------------------------------
		# update the brokerage acount total value and cash value so we're prepared for any trading
		yesterday = stocks.Date[i-1]
		today = stocks.Date[i]
		# initialize today's total value and total cash based on yesterday's values
		broker_idx = len(broker)
		broker.loc[broker_idx] = [today, broker.iloc[broker_idx-1,1], broker.iloc[broker_idx-1,2]]
		# doing this so we KNOW our brokerage account contains an entry for today
		# ------------------------------------------------------------------------------------------

		# process any open orders

		broker, orders, positions = process_orders(broker, orders, positions, stocks, i)
		
		# get any open positions
		open_positions = positions.loc[positions.Status=='open']
		
		# REPLACE ME -- this comment and print() should be a log statement
		# print info about the STOCK_DF that we're processing
		if DEBUG:
			print(f'strategy ------- stock idx: {i}, # open positions = {len(open_positions)}, close: {stocks.Close[i]}, rolling low: {stocks.Indicator_2[i]}, rolling high: {stocks.Indicator_1[i]}, ')
		
		# ------------------------------------------------------------------------------------------
		# Execute our Trading Strategy
		# ------------------------------------------------------------------------------------------
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
		
		# ------------------------------------------------------------------------------------------
		# IF there's NO open positions, THEN...
		if (len(open_positions) <= 0) :
			
			# Confirm there's NO prior buy signal, AND
			# Check if 'Close' has met the 'Rolling High'
			if (np.isnan(stocks.BuySignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_1[i]) :
				
				# create a buy order
				orders = create_order(orders, stocks.Date[i], 'buy')
				
				# set Close price -> Buy Signal
				stocks.loc[i,'BuySignal'] = stocks.Close[i]
			
			elif (np.isnan(stocks.SellSignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_2[i]) :
				
				# create a sell order
				orders = create_order(orders, stocks.Date[i], 'sell')
				
				# set Close price -> Sell Signal
				stocks.loc[i,'SellSignal'] = stocks.Close[i]
			
		
		# ------------------------------------------------------------------------------------------
		# ELSE IF there are open positions, THEN...
		elif (0 < len(open_positions) < 2) :
			
			# REPLACE ME -- this comment and print() should be a log statement
			# print info about the STOCK_DF that we're processing
			# print('positions type =', positions.loc[positions['Status']=='open']['Type'])
			
			# get the index for the open position
			pos_idx = open_positions.index[0]

			if (open_positions.Type[pos_idx] is not 'long') and \
			(np.isnan(stocks.BuySignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_1[i]) :
				
				# create a close order
				orders = create_order(orders, stocks.Date[i], 'close')
				
				# create a buy order
				orders = create_order(orders, stocks.Date[i], 'buy')
				
				# set Close price -> Buy Signal
				stocks.loc[i,'BuySignal'] = stocks.Close[i]
				
			elif (open_positions.Type[pos_idx] is not 'short') and \
			(np.isnan(stocks.SellSignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_2[i]) :
				
				# create a close order
				orders = create_order(orders, stocks.Date[i], 'close')
				
				# create a sell order
				orders = create_order(orders, stocks.Date[i], 'sell')
				
				# set Close price -> Sell Signal
				stocks.loc[i,'SellSignal'] = stocks.Close[i]
				
		# ------------------------------------------------------------------------------------------
		elif (len(open_positions) > 1) :
			if DEBUG:
				print(f'strategy ------- there\'s mutliple open positions - what do we do???')
		
		# ------------------------------------------------------------------------------------------
		# update the positions's unrealized value and the brokerage account's total value
		if (len(positions) > 0) and (positions.iloc[-1].Status=='open'):

			# POSITION_COLUMNS = ['Date','Position','Price','Cost','Type','Status','Unrealized','Realized']
			# Unrealized = 6
			# update the open position's Unrealized(gain)
			# Unrealized(gain) = Cost - (Position * Closing Price)
			positions.iloc[-1,6] = positions.iloc[-1].Cost - (abs(positions.iloc[-1].Position) * stocks.iloc[i].Close)

			# REPLACE ME -- this comment and print() should be a log statement
			# print info from BROKER_DF
			if DEBUG:
				print(f'strategy ------- update positions - row: {positions.index[-1]}, date: {broker.iloc[-1].Date}, cost: {positions.iloc[-1].Cost}, unrlz: {positions.iloc[-1].Unrealized}, rlizd: {positions.iloc[-1].Realized} ')

			# BROKER_COLUMNS = ['Date','TotalCash','CashValue']
			# update the brokerage account's total value
			broker.iloc[-1].TotalValue = broker.iloc[-1].TotalCash + positions.iloc[-1].Cost + positions.iloc[-1].Unrealized

		# REPLACE ME -- this comment and print() should be a log statement
		# print info from BROKER_DF
		if DEBUG:
			print(f'strategy ------- update broker -- row: {broker.index[-1]}, date: {broker.iloc[-1].Date}, cash: {broker.iloc[-1].TotalCash}, value: {broker.iloc[-1].TotalValue}, ')
		
		#---- end FOR loop

	if DEBUG:
		print('--------------------------------------------------------------------------------')
		print(stocks.tail(50))
		print(orders.tail(20))
		print(positions.tail(20))
		print(broker.tail(50))
		print('--------------------------------------------------------------------------------')

	return broker, orders, positions, stocks

'''    STRATEGY 2    '''
def execute_dreyfus_strategy(broker, orders, positions, stocks):

	weekly_rolling_high = 250 # 250 periods is ~52 weeks
	weekly_rolling_low  = 250 # same as above

	# generate rolling highs and lows
	stocks['Indicator_1'] = stocks['Close'].rolling(weekly_rolling_high).max()
	stocks['Indicator_2'] = stocks['Close'].rolling(weekly_rolling_low).min()

	# generate buy / sell signal columns
	stocks['BuySignal'] = np.NaN
	stocks['SellSignal'] = np.NaN

	# iterate over the dataframe starting with the second row
	for i in range(1, len(stocks)) :

		# ------------------------------------------------------------------------------------------
		# update the brokerage acount total value and cash value so we're prepared for any trading
		yesterday = stocks.Date[i-1]
		today = stocks.Date[i]
		# initialize today's total value and total cash based on yesterday's values
		broker_idx = len(broker)
		broker.loc[broker_idx] = [today, broker.iloc[broker_idx-1,1], broker.iloc[broker_idx-1,2]]
		# doing this so we KNOW our brokerage account contains an entry for today
		# ------------------------------------------------------------------------------------------

		# process any open orders
		broker, orders, positions = process_orders(broker, orders, positions, stocks, i)
		
		# get any open positions
		open_positions = positions.loc[positions.Status=='open']
		
		# REPLACE ME -- this comment and print() should be a log statement
		# print info about the STOCK_DF that we're processing
		if DEBUG:
			print(f'strategy ------- stock idx: {i}, # open positions = {len(open_positions)}, close: {stocks.Close[i]}, rolling low: {stocks.Indicator_2[i]}, rolling high: {stocks.Indicator_1[i]}, ')
		
		# ------------------------------------------------------------------------------------------
		# Execute our Trading Strategy
		# ------------------------------------------------------------------------------------------
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
		
		# ------------------------------------------------------------------------------------------
		# IF there's NO open positions, THEN...
		if (len(open_positions) <= 0) :
			
			# Confirm there's NO prior buy signal, AND
			# Check if 'Close' has met the 'Rolling High'
			if (np.isnan(stocks.BuySignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_1[i]) :
				
				# create a buy order
				orders = create_order(orders, stocks.Date[i], 'buy')
				
				# set Close price -> Buy Signal
				stocks.loc[i,'BuySignal'] = stocks.Close[i]
			
			elif (np.isnan(stocks.SellSignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_2[i]) :
				
				# create a sell order
				orders = create_order(orders, stocks.Date[i], 'sell')
				
				# set Close price -> Sell Signal
				stocks.loc[i,'SellSignal'] = stocks.Close[i]
			
		
		# ------------------------------------------------------------------------------------------
		# ELSE IF there are open positions, THEN...
		elif (0 < len(open_positions) < 2) :
			
			# REPLACE ME -- this comment and print() should be a log statement
			# print info about the STOCK_DF that we're processing
			# print('positions type =', positions.loc[positions['Status']=='open']['Type'])
			
			# get the index for the open position
			pos_idx = open_positions.index[0]

			if (open_positions.Type[pos_idx] is not 'long') and \
			(np.isnan(stocks.BuySignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_1[i]) :
				
				# create a close order
				orders = create_order(orders, stocks.Date[i], 'close')
				
				# create a buy order
				orders = create_order(orders, stocks.Date[i], 'buy')
				
				# set Close price -> Buy Signal
				stocks.loc[i,'BuySignal'] = stocks.Close[i]
				
			elif (open_positions.Type[pos_idx] is not 'short') and \
			(np.isnan(stocks.SellSignal[i-1])) and \
			(stocks.Close[i]==stocks.Indicator_2[i]) :
				
				# create a close order
				orders = create_order(orders, stocks.Date[i], 'close')
				
				# create a sell order
				orders = create_order(orders, stocks.Date[i], 'sell')
				
				# set Close price -> Sell Signal
				stocks.loc[i,'SellSignal'] = stocks.Close[i]
				
		# ------------------------------------------------------------------------------------------
		elif (len(open_positions) > 1) :
			if DEBUG:
				print(f'strategy ------- there\'s mutliple open positions - what do we do???')
		
		# ------------------------------------------------------------------------------------------
		# update the positions's unrealized value and the brokerage account's total value
		if (len(positions) > 0) and (positions.iloc[-1].Status=='open'):

			# POSITION_COLUMNS = ['Date','Position','Price','Cost','Type','Status','Unrealized','Realized']
			# Unrealized = 6
			# update the open position's Unrealized(gain)
			# Unrealized(gain) = Cost - (Position * Closing Price)
			positions.iloc[-1,6] = positions.iloc[-1].Cost - (abs(positions.iloc[-1].Position) * stocks.iloc[i].Close)

			# REPLACE ME -- this comment and print() should be a log statement
			# print info from BROKER_DF
			if DEBUG:
				print(f'strategy ------- update positns - row: {positions.index[-1]}, date: {broker.iloc[-1].Date}, cost: {positions.iloc[-1].Cost}, unrlz: {positions.iloc[-1].Unrealized}, rlizd: {positions.iloc[-1].Realized} ')

			# BROKER_COLUMNS = ['Date','TotalCash','CashValue']
			# update the brokerage account's total value
			broker.iloc[-1].TotalValue = broker.iloc[-1].TotalCash + positions.iloc[-1].Cost + positions.iloc[-1].Unrealized

		# REPLACE ME -- this comment and print() should be a log statement
		# print info from BROKER_DF
		if DEBUG:
			print(f'strategy ------- update broker -- row: {broker.index[-1]}, date: {broker.iloc[-1].Date}, cash: {broker.iloc[-1].TotalCash}, value: {broker.iloc[-1].TotalValue}, ')
		
		#---- end FOR loop

	if DEBUG:
		print('--------------------------------------------------------------------------------')
		print(stocks.tail(50))
		print(orders.tail(20))
		print(positions.tail(20))
		print(broker.tail(50))
		print('--------------------------------------------------------------------------------')

	return broker, orders, positions, stocks

'''    STRATEGY 3    '''
def execute_golden_cross_strategy(broker, orders, positions, stocks):

	fast_sma = 20 # 20 periods is ~4 weeks / 1 month
	slow_sma = 200 # 200 periods is most of the year

	# generate fast and slow SMAs
	stocks['Indicator_1'] = stocks['Close'].rolling(fast_sma).mean()
	stocks['Indicator_2'] = stocks['Close'].rolling(slow_sma).mean()

	# generate buy / sell signal columns
	stocks['BuySignal'] = np.NaN
	stocks['SellSignal'] = np.NaN

	# iterate over the dataframe starting with the second row
	for i in range(1, len(stocks)) :

		# ------------------------------------------------------------------------------------------
		# update the brokerage acount total value and cash value so we're prepared for any trading
		yesterday = stocks.Date[i-1]
		today = stocks.Date[i]
		# initialize today's total value and total cash based on yesterday's values
		broker_idx = len(broker)
		broker.loc[broker_idx] = [today, broker.iloc[broker_idx-1,1], broker.iloc[broker_idx-1,2]]
		# doing this so we KNOW our brokerage account contains an entry for today
		# ------------------------------------------------------------------------------------------

		# process any open orders
		broker, orders, positions = process_orders(broker, orders, positions, stocks, i)
		
		# get any open positions
		open_positions = positions.loc[positions.Status=='open']
		
		# REPLACE ME -- this comment and print() should be a log statement
		# print info about the STOCK_DF that we're processing
		if DEBUG:
			print(f'strategy ------- stock idx: {i}, # open positions = {len(open_positions)}, close: {stocks.Close[i]}, slow sma: {stocks.Indicator_2[i]}, fast sma: {stocks.Indicator_1[i]}, ')
		
		# ------------------------------------------------------------------------------------------
		# Execute our Trading Strategy
		# ------------------------------------------------------------------------------------------
		"""
			IF no open positions, THEN
				IF no recent buy signals, AND
				the Fast SMA crosses the Slow SMA to the upside
					Create a buy order
					Set the Buy Signal to the Close price
				ELSE IF no recent sell signals, AND
				the Fast SMA crosses the Slow SMA to the downside
					Create a sell order
					Set the Sell Signal to the Close price
			Else If open positions exist, THEN
				Do the same as above, except
					Create a close order
					Create a buy/sell order (as appropriate)
					Set the Buy/Sell Signal to the Close price
		"""
		
		# ------------------------------------------------------------------------------------------
		# IF there's NO open positions, THEN...
		if (len(open_positions) <= 0) :
			
			# Confirm there's NO prior BUY signal, AND
			# Check if the Fast SMA (Indicator_1) has crossed Slow SMA (Indicator_2) to the updside
			if (np.isnan(stocks.BuySignal[i-1])) and \
			(stocks.Indicator_1[i]>=stocks.Indicator_2[i]) :
				
				# create a buy order
				orders = create_order(orders, stocks.Date[i], 'buy')
				
				# set Close price -> Buy Signal
				stocks.loc[i,'BuySignal'] = stocks.Close[i]
			
			# Confirm there's NO prior SELL signal, AND
			# Check if the Fast SMA (Indicator_1) has crossed Slow SMA (Indicator_2) to the downside
			elif (np.isnan(stocks.SellSignal[i-1])) and \
			(stocks.Indicator_1[i]<=stocks.Indicator_2[i]) :
				
				# create a sell order
				orders = create_order(orders, stocks.Date[i], 'sell')
				
				# set Close price -> Sell Signal
				stocks.loc[i,'SellSignal'] = stocks.Close[i]
			
		
		# ------------------------------------------------------------------------------------------
		# ELSE IF there are open positions, THEN...
		elif (0 < len(open_positions) < 2) :
			
			# get the index for the open position
			pos_idx = open_positions.index[0]

			# Confirm the current open position is SHORT, AND
			# that there's NO recent BUY signal, AND
			# that Fast SMA (Indicator_1) has crossed Slow SMA (Indicator_2) to the updside
			if (open_positions.Type[pos_idx] is not 'long') and \
			(np.isnan(stocks.BuySignal[i-1])) and \
			(stocks.Indicator_1[i]>=stocks.Indicator_2[i]) :
				
				# create a close order
				orders = create_order(orders, stocks.Date[i], 'close')
				
				# create a buy order
				orders = create_order(orders, stocks.Date[i], 'buy')
				
				# set Close price -> Buy Signal
				stocks.loc[i,'BuySignal'] = stocks.Close[i]
				
			# Confirm the current open position is LONG, AND
			# that there's NO recent SELL signal, AND
			# that Fast SMA (Indicator_1) has crossed Slow SMA (Indicator_2) to the downside
			elif (open_positions.Type[pos_idx] is not 'short') and \
			(np.isnan(stocks.SellSignal[i-1])) and \
			(stocks.Indicator_1[i]<=stocks.Indicator_2[i]) :
				
				# create a close order
				orders = create_order(orders, stocks.Date[i], 'close')
				
				# create a sell order
				orders = create_order(orders, stocks.Date[i], 'sell')
				
				# set Close price -> Sell Signal
				stocks.loc[i,'SellSignal'] = stocks.Close[i]
				
		# ------------------------------------------------------------------------------------------
		elif (len(open_positions) > 1) :
			if DEBUG:
				print(f'strategy ------- there\'s mutliple open positions - what do we do???')
		
		# ------------------------------------------------------------------------------------------
		# update the positions's unrealized value and the brokerage account's total value
		if (len(positions) > 0) and (positions.iloc[-1].Status=='open'):

			# POSITION_COLUMNS = ['Date','Position','Price','Cost','Type','Status','Unrealized','Realized']
			# Unrealized = 6
			# update the open position's Unrealized(gain)
			# Unrealized(gain) = Cost - (Position * Closing Price)
			positions.iloc[-1,6] = positions.iloc[-1].Cost - (abs(positions.iloc[-1].Position) * stocks.iloc[i].Close)

			# REPLACE ME -- this comment and print() should be a log statement
			# print info from BROKER_DF
			if DEBUG:
				print(f'strategy ------- update positns - row: {positions.index[-1]}, date: {broker.iloc[-1].Date}, cost: {positions.iloc[-1].Cost}, unrlz: {positions.iloc[-1].Unrealized}, rlizd: {positions.iloc[-1].Realized} ')

			# BROKER_COLUMNS = ['Date','TotalCash','CashValue']
			# TotalValue = 2
			# update the brokerage account's total value
			broker.iloc[-1].TotalValue = broker.iloc[-1].TotalCash + positions.iloc[-1].Cost + positions.iloc[-1].Unrealized

		# REPLACE ME -- this comment and print() should be a log statement
		# print info from BROKER_DF
		if DEBUG:
			print(f'strategy ------- update broker -- row: {broker.index[-1]}, date: {broker.iloc[-1].Date}, cash: {broker.iloc[-1].TotalCash}, value: {broker.iloc[-1].TotalValue}, ')
		
		#---- end FOR loop

	if DEBUG:
		print('--------------------------------------------------------------------------------')
		print(stocks.tail(50))
		print(orders.tail(20))
		print(positions.tail(20))
		print(broker.tail(50))
		print('--------------------------------------------------------------------------------')

	return broker, orders, positions, stocks

