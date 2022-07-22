**Building an Algorithmic Trader
Project Approach:

**Goals and Objectives:**

      - Learn about successful Trend Trading Methodologies
      - Research Sector Exchange Trading Funds (ETFs)
      - Research and download varying APIs
      - Writing Python code using Jupyterlab, Pandas, yfinance and Plotly
      - Test code against data to determine which methodologies are the most successful historically
      - Finally, to create the basic structure for and algorithmic trader

**Strategies Used for Testing:**

- Tested against the SPY
- Potential to test strategies against anything with the ticker symbol
1. Individual stocks
2. Sector ETFs
- Investigated what we can test these strategies against
- Potential to test against different sectors


**Data Collection and Cleaning:**
Data collection involves various CSV files from various sources:

- Pandas data reader library
- Yahoo finance
- Investigated the alpaca market. Didn't use it due to historical data restrictions(3-5 years only)
- Downloaded stock data which were already cleaned
- Additional data was generated and cleaned


**Successful Trading Strategies:**


![Donchian](https://user-images.githubusercontent.com/105619339/180354817-8f77e71b-7196-452e-8415-ec411196089d.png)

![Dreyfus](https://user-images.githubusercontent.com/105619339/180354826-7c7a9ad9-cdbf-4c1f-933f-b71c39b8c00f.png)
![Golden Cross](https://user-images.githubusercontent.com/105619339/180354831-1f51f710-d167-4ed9-8317-f22083befcc0.png)


**APIs We Used:**

- Plotly: Used Plotly to implement a visual representation of the output of our strategies.
- yfinance: This library let us download the historical data from [https://finance.yahoo.com/](url).
- pandas_datareader(pdr): We discovered this library later and replaced the yfinance API. Pdr can be used to download historic stock data from many different services/APIs.

**APIs We Almost Used:**

- Alpaca: Initially tried downloading data from Alpaca; abandoned because historic stock data is resricted to ~ 4 years.
- Backtrader: A feature-rich Python framework for back testing and trading; can be used to write reusable trading strategies, indicators and analyzers. Abandoned because the framework uses object-oriented programing (aka classes). Was difficult to implement some trading strategies. 
- backtesting.py: Similar to backtrader; required further investigation.


**Data Collection:**

1. Data Collection
Historic stock data is quite prevalent; the most difficult choice is where to store the data. We started with Alpaca, and then settled on yfinance and later pandas_datareader for ease-of-use of their APIs. Settled on pandas_datareader for the future ability to download data from sources other than Yahoo Finance.

2. Data Cleaning
Historic stock data is pretty clean to begin with. The biggest thing to watch out for are differently spelled column names, and their order. Difficult was mostly avoided by downloading data from a single source.


**Application Framework:**

app.py
- Holds all important staements, initializes core variables, and runs the program from start to finish (plotting a graph).

broker.py
- Initializes a simple broker; has create_orders(), process_orders(), and execute_orders() functions.
- The execute_orders() funtion supports Buy, Sell and Close order types.
- Stores all Oders and Position data generated for later use when plotting the results.

strategies.py
- Holds a function for each strategy we created.
- Each strategy executes appropriate broker functions at the appropriate time.

utils.py
- A set of helper functions for downloading, loading and saving stock data.

plots.py
- Plots the output of the strategy and stock data selected.
