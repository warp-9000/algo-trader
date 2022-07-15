from datetime import datetime
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
class sma10v30cross(bt.Strategy):

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


class sma20v200cross(bt.Strategy):

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
				self.buy()                  # enter a new short position



# --------------------------------------------------------------------------------------------------
# 2. Create and setup an instance of Backtrader's 'cerebro' engine
# --------------------------------------------------------------------------------------------------

# create an instance of the 'cerebro' engine
cerebro = bt.Cerebro()

cerebro.broker.setcash(starting_funds)
cerebro.broker.setcommission(broker_commission)



# --------------------------------------------------------------------------------------------------
# 3. Pass cerebro some financial data
# --------------------------------------------------------------------------------------------------

# get stock data
stock_data = get_stock_data('MSFT')

datafeed = bt.feeds.PandasData(dataname=stock_data)

print('---- adding stock data -------------------------------------')
cerebro.adddata(datafeed)  # add the data to cerebro
print('-------- complete ------------------------------------------')



# --------------------------------------------------------------------------------------------------
# 4. Give cerebro a strategy to use
# --------------------------------------------------------------------------------------------------

print('---- adding trading strategy -------------------------------')
# cerebro.addstrategy(sma10v30cross)  # add the trading strategy
cerebro.addstrategy(sma20v200cross)  # add the trading strategy
print('-------- complete ------------------------------------------')



# --------------------------------------------------------------------------------------------------
# 5. Tell cerebro to run the strategy
# --------------------------------------------------------------------------------------------------

print('---- running cerebro ---------------------------------------')
cerebro.run()  # run it all
print('-------- complete ------------------------------------------')



# --------------------------------------------------------------------------------------------------
# 6. Plot the output of the strategy
# --------------------------------------------------------------------------------------------------

print('---- plotting the results ----------------------------------')
cerebro.plot()  # plot the results
print('-------- complete ------------------------------------------')
