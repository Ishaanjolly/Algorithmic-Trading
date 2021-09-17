# Functions to process transactions.
import numpy as np

def log_transaction(transaction_type, date, stock, number_of_shares, price, fees, ledger_file):
    '''
    Record a transaction in the file ledger_file. If the file doesn't exist, create it.
    
    Input:
        transaction_type (str): 'buy' or 'sell'
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we buy or sell (the column index in the data array)
        number_of_shares (int): the number of shares bought or sold
        price (float): the price of a share at the time of the transaction
        fees (float): transaction fees (fixed amount per transaction, independent of the number of shares)
        ledger_file (str): path to the ledger file
    
    Output: returns None.
        Writes one line in the ledger file to record a transaction with the input information.
        This should also include the total amount of money spent (negative) or earned (positive)
        in the transaction, including fees, at the end of the line.
        All amounts should be reported with 2 decimal digits.

    Example:
        Log a purchase of 10 shares for stock number 2, on day 5. Share price is 100, fees are 50.
        Writes the following line in 'ledger.txt':
        buy,5,2,10,100.00,-1050.00
            >>> log_transaction('buy', 5, 2, 10, 100, 50, 'ledger.txt')
    '''
    #calculate the money earned or spent(since it is a or situation we use a if loop)  
    if number_of_shares == 0:
            amount_spent_earned =0
    else: 
        if transaction_type == 'buy':
            amount_spent_earned = -(number_of_shares * price) - fees # amount will be negative if transaction is buy 
        else:
            amount_spent_earned = (number_of_shares * price) - fees  # amount will not be negative if the transaction is not bbuy 
        # write the transaction details in the legder.txt(as suggested in the prompt) 
    with open(ledger_file, 'a') as new_ledger_file: # to append to the file 
        new_ledger_file.write(f'{transaction_type},{date},{stock},{number_of_shares},{price:.2f},{amount_spent_earned:.2f}\n') 
    
    return None
def buy(date, stock, available_capital, stock_prices, fees, portfolio, ledger_file):
    
    '''
    Buy shares of a given stock, with a certain amount of money available.
    Updates portfolio in-place, logs transaction in ledger.
    
    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to buy
        available_capital (float): the total (maximum) amount to spend,
            this must also cover fees
        stock_prices (ndarray): the stock price data
        fees (float): total transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file
    
    Output: None

    Example:
        Spend at most 1000 to buy shares of stock 7 on day 21, with fees 30:
            >>> buy(21, 7, 1000, sim_data, 30, portfolio,'ledger.txt')
    '''
     #find the price of stock given the date and stock prices 
    price = stock_prices[date,stock]
    if np.isnan(price):
        return None
    #calculate the amount of shares to buy
    number_of_shares = int((available_capital - fees) // price)
    #update the portfolio and include the amount of stares 
    portfolio[stock] += number_of_shares
    #log the transaction in the ledger file :) 
    log_transaction('buy', date, stock, number_of_shares, price,fees,ledger_file)
    return None 
    
def sell(date, stock, stock_prices, fees, portfolio, ledger_file):
    '''
    Sell all shares of a given stock.
    Updates portfolio in-place, logs transaction in ledger.
    
    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to sell
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file
    
    Output: None

    Example:
        To sell all our shares of stock 1 on day 8, with fees 20:
            >>> sell(8, 1, sim_data, 20, portfolio,'ledger.txt')
    '''
    #find the pruce of stock given the date and stock prices(just like when you buy) 
    price = stock_prices[date,stock] 
    #get the number of shares to sell 
    number_of_shares = portfolio[stock] 
    #update the portfolio because we sell all of them, so we would be left with 0 
    portfolio[stock] = 0 
    #log transactions in the ledger file 
    log_transaction('sell', date, stock, number_of_shares, price, fees, ledger_file)
    
    return None
    
def create_portfolio(available_amounts, stock_prices, fees, ledger_file):
    '''
    Create a portfolio by buying a given number of shares of each stock.
    
    Input:
        available_amounts (list): how much money we allocate to the initial
            purchase for each stock (this should cover fees)
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
        ledger_file (str): path to the ledger file
    
    Output:
        portfolio (list): our initial portfolio

    Example:
        Spend 1000 for each stock (including 40 fees for each purchase):
        >>> N = sim_data.shape[1]
        >>> portfolio = create_portfolio([1000] * N, sim_data, 40, 'ledger.txt')
    '''
    #for the length of the stock price create a variable length_stock 
    length_stock = len(stock_prices[0])
    portfolio = [0 for i in range (length_stock)]  # define portfolio based on the length of the stock price 
    for i in range (length_stock):
        buy(0,i, available_amounts[i], stock_prices, fees, portfolio, ledger_file)      
    return portfolio
    