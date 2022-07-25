import sys
import os

IN_ROOT_DIR = False

if not IN_ROOT_DIR:
	# getting the name of the directory
	# where the this file is present.
	current = os.path.dirname(os.path.realpath(__file__))
	
	# Getting the parent directory name
	# where the current directory is present.
	parent = os.path.dirname(current)
	
	# adding the parent directory to 
	# the sys.path.
	sys.path.append(parent)
	
	# now we can import the module in the parent directory.

from utils import *
from plots import *






# -------------------------------------------------------------------------------------------------
# UNCOMMENT THIS TO PLOT A STRATEGY AGAINST PRIOR DATA
# -------------------------------------------------------------------------------------------------

ticker = 'SPY'

# strategy = 'donchian'
strategy = 'dreyfus'
# strategy = 'goldencross'

stock_plot_df = load_data(ticker+'_'+strategy+'_'+'plot_stock_data')
trade_plot_df = load_data(ticker+'_'+strategy+'_'+'plot_trade_data')
broke_plot_df = load_data(ticker+'_'+strategy+'_'+'plot_broke_data')

generate_graph(stock_plot_df, trade_plot_df, broke_plot_df)