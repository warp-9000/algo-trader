import sys
import os
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
  
# now we can import the module in the parent
# directory.

from utils import *

data = download_stock_data()

for i in data:
	data[i].reset_index(inplace=True)

print(data['SPY'])

slice = data['SPY'][['Date','Close','Volume']]

print(slice)