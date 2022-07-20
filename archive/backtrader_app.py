
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# from datetime import datetime
import backtrader as bt
from utils import get_stock_data

# --------------------------------------------------------------------------------------------------
# 0. Global Variables
# --------------------------------------------------------------------------------------------------

DEBUG = True

starting_funds = 100000.0        # $100K in starting funds
broker_commission = 0.00         # $0 commission fees

# --------------------------------------------------------------------------------------------------
# 1. Creating the trading strategies we want to use
# --------------------------------------------------------------------------------------------------

# Create a subclass of Strategy to define the indicators and logic

# Donchian’s Four Week Rule (1960)
"""
Indicators
	Graph highest weekly high for past 4 weeks
	Graph lowest weekly low for past 4 weeks
Long Rules
	Entry	= Buy when price breaks the weekly high (past 4 weeks)
	Exit	= Sell when price breaks the weekly low (past 4 weeks)
Short Rules
	Entry	= Sell when price breaks the weekly low (past 4 weeks)
	Exit	= Buy when price breaks the weekly high (past 4 weeks)
"""

# class SimpleMovingAverage1(Indicator):
#     lines = ('sma',)
#     params = (('period', 20),)

#     def next(self):
#         datasum = math.fsum(self.data.get(size=self.p.period))
#         self.lines.sma[0] = datasum / self.p.period

class WeeklyHigh(bt.Indicator):
	lines = ('high',)
	params = (('period', 20),)
	
	def __init__(self):
		
		"""
		get last <n> periods of data
		high = maximum value in <n> periods of data
		"""
		self.lines.high = bt.Max(self.lines.high, self.data)

class WeeklyLow(bt.Indicator):
	lines = ('low',)
	params = (('period', 10),)

	def __init__(self):
		self.lines.low = bt.Min(self.lines.low, self.data)


class donchians_four_week_strategy(bt.Strategy):

	def log(self, txt, dt=None):
			"""Logging function for this strategy"""
			dt = dt or self.datas[0].datetime.date(0)
			print('%s, %s' % (dt.isoformat(), txt))

	def __init__(self, phigh=20, plow=10):
		# initializing the SMAs and crossover
		self.rolling_high = WeeklyHigh(self.datas[0].close, period=phigh)			# rolling high
		self.rolling_low = WeeklyLow(self.datas[0].close, period=plow)				# rolling low
		self.cross_high = bt.ind.CrossOver(self.datas[0].close, self.rolling_high)	# price meets high
		self.cross_low = bt.ind.CrossOver(self.datas[0].close, self.rolling_low)	# price meets low

		self.data_close = self.datas[0].close


	def next(self):
		
		self.log('Close, %.2f' % self.data_close[0])
		self.log('Position, %.2f' % self.position.price)
		self.log('Cross High, %.2f' % self.cross_high)
		
		if not self.position:           # not in the market
#			print(f'---- out of market, date: {self.data}, crosses_high: {self.crosses_high}, crosses_low: {self.crosses_low}')
			if self.cross_high > 0:	# if price crosses the rolling high to the upside
				self.buy()					# enter long
			elif self.cross_low > 0:	# if price crosses the rolling low to the downside
				self.sell()                 # enter short

		else:                           # we are in the market
#			print(f'---- in market, date: {self.data}, crosses_high: {self.crosses_high}, crosses_low: {self.crosses_low}')
			if self.cross_high > 0:      # if fast crosses slow to the upside
				self.close()                # close our current position
				self.buy()                  # enter a new long position
			elif self.cross_low > 0:    # if fast crosses slow to the downside
				self.close()                # close our current position
				self.sell()                  # enter a new short position


# Dreyfus’s 52 Week Rule (1960)
"""
Indicators
	Graph highest weekly high for past 52 weeks
	Graph lowest weekly low for past 52 weeks
Long Rules
	Entry	= Buy when price breaks the weekly high (past 52 weeks)
	Exit	= Sell when price breaks the weekly low (past 52 weeks)
Short Rules
	Entry	= Sell when price breaks the weekly low (past 52 weeks)
	Exit	= Buy when price breaks the weekly high (past 52 weeks)
"""

# Turtle Trading (1983)
"""
Indicators to Graph
	Highest weekly high for past 4 weeks
	Lowest weekly low for past 2 weeks
Filter Rules
	Only trade if last trade was at a loss
Long rules
	Entry	= Buy when price breaks weekly high (past 4 weeks)
	Exit	= Sell when price breaks weekly low (past 2 weeks)
Short rules
	Entry	= Buy when price breaks weekly low (past 4 weeks)
	Exit	= Sell when price breaks weekly high (past 2 weeks)
"""


class sma_cross_10v30(bt.Strategy):

	def __init__(self, pfast=10, pslow=30):

		# initializing the SMAs and crossover
		self.sma_fast = bt.ind.SMA(self.data.close, period=pfast)  # fast moving average
		self.sma_slow = bt.ind.SMA(self.data.close, period=pslow)  # slow moving average
		self.crossover = bt.ind.CrossOver(self.sma_fast, self.sma_slow)  # crossover signal

	def next(self):

		if not self.position:           # not in the market
			if self.crossover > 0:      # if fast crosses slow to the upside
				self.buy()                  # enter long
		
		elif self.crossover < 0:        # in the market & cross to the downside
			self.close()                    # close long position


class sma_cross_20v200(bt.Strategy):

	def __init__(self, pfast=20, pslow=200):

		# initializing the SMAs and crossover
		self.sma_fast = bt.ind.SMA(self.data.close, period=pfast)    # fast moving average
		self.sma_slow = bt.ind.SMA(self.data.close, period=pslow)    # slow moving average
		self.crossover = bt.ind.CrossOver(self.sma_fast, self.sma_slow)   # crossover signal


	def next(self):

		if not self.position:           # not in the market
			if self.crossover > 0:      # if fast crosses slow to the upside
				self.buy()                  # enter long
			elif self.crossover < 0:    # if fast crosses slow to the downside
				self.sell()                 # enter short

		else:                           # we are in the market
			if self.crossover > 0:      # if fast crosses slow to the upside
				self.close()                # close our current position
				self.buy()                  # enter a new long position
			elif self.crossover < 0:    # if fast crosses slow to the downside
				self.close()                # close our current position
				self.sell()                  # enter a new short position



# --------------------------------------------------------------------------------------------------
# 2. Create and setup an instance of Backtrader's 'cerebro' engine
# --------------------------------------------------------------------------------------------------

# create an instance of the 'cerebro' engine
cerebro = bt.Cerebro()

cerebro.broker.setcash(starting_funds)
cerebro.broker.setcommission(broker_commission)

cerebro.addsizer(bt.sizers.SizerFix, stake=25)


# --------------------------------------------------------------------------------------------------
# 3. Pass cerebro some financial data
# --------------------------------------------------------------------------------------------------

# get stock data
stock_data = get_stock_data('SPY')

# convert the pandas dataframe to a feed digestible by cerebro
datafeed = bt.feeds.PandasData(dataname=stock_data)

if DEBUG:
	print('---- adding stock data --------------------------------------------')
cerebro.adddata(datafeed)  # add the data to cerebro
if DEBUG:
	print('-------- complete -------------------------------------------------')



# --------------------------------------------------------------------------------------------------
# 4. Give cerebro a strategy to use
# --------------------------------------------------------------------------------------------------

print('---- adding trading strategy ------------------------------------------')
# cerebro.addstrategy(sma_cross_10v30)  # add the trading strategy
# cerebro.addstrategy(sma_cross_20v200)  # add the trading strategy
cerebro.addstrategy(donchians_four_week_strategy)
print('-------- complete -----------------------------------------------------')



# --------------------------------------------------------------------------------------------------
# 5. Tell cerebro to run the strategy
# --------------------------------------------------------------------------------------------------



print('---- running cerebro --------------------------------------------------')
cerebro.run()  # run it all
print('-------- complete -----------------------------------------------------')

# get the current value, cash, and position from the broker to see how we've done
portfolio_value = cerebro.broker.get_value()
portfolio_funds = cerebro.broker.get_cash()

print('---- portfolio value, cash, and open positions --------------------------------------------')
print(f'---- current value: ${portfolio_value :.2f}')
print(f'---- current funds: ${portfolio_funds :.2f}')
print('-------------------------------------------------------------------------------------------')


# --------------------------------------------------------------------------------------------------
# 6. Plot the output of the strategy
# --------------------------------------------------------------------------------------------------

print('---- plotting the results ----------------------------------')
cerebro.plot()  # plot the results
print('-------- complete ------------------------------------------')


