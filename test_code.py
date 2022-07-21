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



stock_plot_df = load_data('plot_stock_data')
trade_plot_df = load_data('plot_trade_data')
broke_plot_df = load_data('plot_broke_data')

generate_graph(stock_plot_df, trade_plot_df, broke_plot_df)