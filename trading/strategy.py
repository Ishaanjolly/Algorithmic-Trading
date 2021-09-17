# Functions to implement our trading strategy.
import numpy as np
import trading.process as proc
import trading.indicators as indicators 
from random import randint

def random(stock_prices, period=7, amount=5000, fees=20, ledger='ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    
    the function 
    '''
    # we will first define days and stocks
    days = len(stock_prices)
    stocks = len(stock_prices [0])
    N = stock_prices.shape[1]
    rng = np.random.default_rng()
    portfolio = proc.create_portfolio ([amount]*N,stock_prices,fees,ledger)
    
    # we will now make a decision variable that takes 3 values = 0,1,2
    #if the decision variable is 0, we do nothing
    #if the decision variable is 1, we call the buy function 
    #if the decision variable is 2, we call the sell function 
    for day in range(0, days, period):
        for stock in range(stocks):
            decision = rng.choice([0,1,2], p = [1/3,1/3,1/3])
            if decision == 0:
                continue # we are doing nothing, going on to next iteration 
            elif decision == 1: 
                date = day                
                proc.buy(date, stock, amount, stock_prices, fees, portfolio, ledger)
            elif decision == 2: 
                date = day
                proc.sell(date, stock, stock_prices, fees, portfolio, ledger) 
    return None



def crossing_averages(stock_price, m=50, n=200):
    '''
    Input: 
    stock_price(ndarray): single column with the shares prices over time for one stock
    m: period for the first moving average 
    n: period for the slow moving average 

    Output: list of decisions based on crossing_averages
    ''' 
    #create numpy array for  FMA and SMA 
    fma = np.array(indicators.moving_average(stock_price, m))
    sma = np.array(indicators.moving_average(stock_price, n))

    days = len(stock_price) 
    difference = fma - sma
    print(difference.shape)
    diffs = np.where(np.diff(fma - sma > 0))
    return diffs
    
    
def momentum(stock_price, period = 7, oscillator = 'stochastic', lowThreshold = 0.25, highThreshold = 0.75, waitingTime = 3, amount = 5000, fees = 20, ledger = "ledger_momentum.txt"): 
    #take osc from the oscillator in indicator 
    osc = indicators.oscillator(stock_price, n = period, osc_type = oscillator)  
    length = len(stock_prices)
    portfolio = [0 for i in range (len(stock_price.shape[1]))]
    for i in range(0, length): 
        if(osc[i] > highThreshold):
            proc.sell(i, 0, stock_price, fees, portfolio, ledger)
        elif(osc[i] < lowThreshold):
            proc.buy(i, 0, amount, stock_price, fees, portfolio, ledger)
    return 