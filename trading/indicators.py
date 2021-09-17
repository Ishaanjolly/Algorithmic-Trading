import numpy as np

import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    '''
    if len(weights) == 0 or len(weights) == n:
        
        # General Moving average. If the moving average is unweighted, fill the 
        # weights list with 1's to use the weighted moving average form. But it's
        # not going to do any harm

        if len(weights) == 0:
            weights = [1/n] * n
        else:
            weights = weights

        # the convolution computes the weighted sum divided by the size of the window (length of the weights)
        return np.convolve(stock_price, weights, 'same')
    else:
        print("The number of weights does not match the n period for the average. Try again")
        return
    
def oscillator(stock_price, n=7, osc_type='stochastic'): 
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.
    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.
    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    '''
    
    ''' 
    Requirments of the oscillator function for stochastic 
    To calculate the level of the stochastic oscillator on a given day:
    Find the highest and lowest prices over the past 𝑛days.
    Compute the difference between today's price and the lowest price, call it Δ.
    Compute the difference between the highest price and the lowest price, call it Δmax.
    The level of the oscillator on this day is the ratio Δ/Δmax.
    '''
    days = len(stock_price) #find days from the stock price 
    osc = [np.nan]*days 
    
    if osc_type == "stochastic": 
        for i in range(n-1, days): # for n days 
           
            if np.isnan(stock_price[i]):  
                break 
            # we will find the highest and lowest price, which is maximum and minimum respectively
            
            highest_price = np.max(stock_price[i-n+1:i+1])
            lowest_price = np.min(stock_price[i-n+1:i+1])
            
            #compute the difference between todays price and lowest price as delta 
            
            if stock_price[i] - lowest_price >0: 
               delta =stock_price[i] - lowest_price
            else: 
                delta = 0 
                
            #find the difference between the highest price and lowest price as delta maz 
            delta_max = highest_price - lowest_price 
            
            
            level_of_oscillator = delta/delta_max  
            osc[i] = level_of_oscillator
    
    elif osc_type == "RSI": 
        for i in range(n-1,days): 
        # we break the loop if the the value at index i is nan 
            if np.isnan(stock_price[i]):
               break 
        #create a list of the stock prices over days 
            stock_price_ndays = stock_price[i-n+1:i+1]  
        
        #create a list of price differences on past n consecutive days 
            consecutive_days_diff  = np.diff(stock_price_ndays)
        
            #we seperate the positive and negative difference by locating the index of positive and negative 
            #it should return a list based on the condition being true 
            p_index = np.where(consecutive_days_diff > 0)
            n_index = np.where(consecutive_days_diff < 0)
            
            #calculate the average of all positive difference 
            if len(p_index[0]) ==0:
                avg_gain = 0 
            else:
                avg_gain = sum(consecutive_days_diff[p_index])/len(p_index[0])
            #calculate the absolute value of the average of all negative differences 
            if len(n_index[0]) ==0: 
                avg_loss =0
            else: 
                avg_loss = abs(sum (consecutive_days_diff[n_index])/len(n_index[0]))      
            
            #Caculate RS and RSI 
            
            if avg_loss ==0 and avg_gain ==0:
                RSI = 0.5 
            elif avg_gain ==0:
                RSI = 0  
            elif avg_loss ==0: 
                RSI = 1
            else: 
                RS = avg_gain/avg_loss
                RSI = (1 -(1/(1 +RS)))     
            #replace today's RSI value with that of osc[i]     
                osc[i] = RSI
    return osc
            
            
            
            
            
        
            
        
