def connection_test():
    "Testing the connection between files"
    a = "working"
    print('working...')
    return a

def get_historical_data(coin,vs_curr,start_date,end_date):
    """
    Returns historical data from the coingecko API in dataframe form
    
    coin :lower_case name (e.g 'bitcoin')
    vs_curr : lower case ticker symbol (e.g 'btc')
    start_date : day/month/year date format (e.g 01/01/2021)
    end_date : day/month/year date format (e.g 01/01/2021)
    
    ex: get_historical_data(coin = 'bitcoin', vs_curr='usd', 
    start_date='01/01/2020', end_date = '01,02,2021')
    
    """
    import time 
    import datetime
    import pandas as pd
    from pycoingecko import CoinGeckoAPI
    import numpy as np
    cg = CoinGeckoAPI()
    start = int(datetime.datetime.strptime(start_date, '%d/%m/%Y').strftime("%s"))
    end = int(datetime.datetime.strptime(end_date, '%d/%m/%Y').strftime("%s"))
    hist_data= cg.get_coin_market_chart_range_by_id(id=coin,vs_currency='usd',from_timestamp=start,to_timestamp=end)
    prices_dict = hist_data['prices']
    data = pd.DataFrame.from_dict(prices_dict)
    data[0]=(pd.to_datetime(data[0],unit='ms'))
    data.columns = ['date', 'price']
    data['returns'] = data['price'].pct_change()
    data['cum_returns'] = np.cumprod(1 + data['returns']) - 1
    return data

def plot_returns(asset1, asset2):
    """
    Returns a time series of returns for 2 assets
    asset1 : a df returned by get_historical_data over a time period
    asset2 : a df returned by get_historical_data over same time period
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    plt.plot(asset1['date'],asset1['cum_returns'])
    plt.plot(asset2['date'],asset2['cum_returns'])
    plt.show()
    
    
def plot_ratio(asset1, asset2):
    """
    Returns a time series of ratio of 2 assets
    asset1 : a df returned by get_historical_data over a time period
    asset2 : a df returned by get_historical_data over same time period
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    
    Y = asset1['price']
    X = asset2['price']
    (Y/X).plot(figsize=(15,7)) 
    plt.axhline((Y/X).mean(), color='red', linestyle='-') 
    plt.axhline((Y/X).mean() + (Y/X).std(), color= 'black', linestyle = '--')
    plt.axhline((Y/X).mean() + (Y/X).std(), color= 'black', linestyle = '--')
    plt.axhline((Y/X).mean() - (Y/X).std(), color= 'black', linestyle = '--')
    plt.axhline((Y/X).mean() + 2*(Y/X).std(), color= 'black', linestyle = ' ')
    plt.axhline((Y/X).mean() - 2*(Y/X).std(), color= 'black', linestyle = ' ')
    plt.xlabel('Time')
    plt.legend(['Price Ratio', 'Mean'])
    plt.show()
    
    #fig = plt.figure(figsize=(8,4), dpi=100)
    #axes1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    
    #axes1.plot(asset1['date'],Y/X, 'b')

def get_pair_stats(asset1, asset2):
    """
    This method takes in the dataframes produced by the get_historical_data and gives statistics for the return series including: 
    1.basic: mean, standard_deviation, max, min
    
    """
    from statsmodels.tsa.stattools import coint
    import numpy as np
    coint_test = coint(asset1['returns'].fillna(value=0),asset2['returns'].fillna(value=0))
    X = asset1['returns']
    Y = asset2['returns']
    
    asset1_stats = [X.mean(),X.std(),X.max(),X.min()]
    asset2_stats = [Y.mean(),Y.std(),Y.max(),Y.min()]
    
    print( "\n Asset1 mean:", asset1_stats[0],
          "\n Asset1 standard deviation:", asset1_stats[1],
          "\n Asset1 max:", asset1_stats[2],
          "\n Asset1 min:", asset1_stats[3],
          "\n Asset2 mean:", asset2_stats[0],
          "\n Asset2 standard deviation:", asset2_stats[1],
          "\n Asset2 max:", asset2_stats[2],
          "\n Asset2 min:", asset2_stats[3],
          "\n Cointergation p_value:", coint_test[1],
          "\n Cointegrated?", (coint_test[1]<0.05)
         )
    
    return

def get_coins_list():
    cg.get_coins_list()
    
"""
cg.get_price(ids='bitcoin', vs_currencies='usd')
cg.get_price(ids=['bitcoin', 'ethereum','litecoin'], vs_currencies='usd')
data = cg.get_coin_history_by_id(id='bitcoin',date='25-06-2021', localization='false')

"""