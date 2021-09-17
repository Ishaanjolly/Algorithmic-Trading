import numpy as np   # import module numpy 
def generate_stock_price(days, initial_price, volatility):
    '''
    Generates daily closing share prices for a company,
    for a given number of days.
    '''
    # Set stock_prices to be a zero array with length days
    stock_prices = np.zeros(days)
    # Set stock_prices in row 0 to be initial_price
    stock_prices[0] = initial_price
    # Set total_drift to be a zero array with length days
    total_drift= np.zeros(days)
    # Set up the default_rng from Numpy
    rng = np.random.default_rng() # can use different values of seed to check the function
    
   # define a function for news   
    def news(chance, volatility):  # We took it out of the orginal for loop *change in code structure*
            '''
            Simulate the news with % chance
            '''
            # Choose whether there's news today
            news_today = rng.choice([0,1], p=chance)
            duration = 0  # set the initial duration to 0 
            if news_today ==1:
                # Calculate m and drift
                m=rng.normal(0,2)   # add 2 as the standard deviation 
                drift = m * volatility
                #randomly choose the duration by using rng.integers
                duration = rng.integers(3,14)  # we are essentially changing days 
                final = np.zeros(duration)
                for i in range(duration):
                    final[i] = drift
                return final
            else:
                return np.zeros(duration)
    # Loop over a range(1, days)
    for day in range(1, days):     # *change in code structure* 
        # Get the random normal increment
        inc = rng.normal(0, volatility)
        # Add stock_prices[day-1] to inc to get NewPriceToday
        new_price_today=stock_prices[day-1]+inc   # add a s to stock_price so it becomes stock_price"s"
         # Get the drift from the news
        d = news([0.99,0.01], volatility) 
        # Get the duration
        duration = len(d)
        # Add the drift to the next days
        total_drift[day:day+duration] +=d
        # Add today's drift to today's price
        new_price_today += total_drift[day]
        # Set the stock prices[day] to new_price_today or to NaN if it's negative 
        if new_price_today <=0:
            stock_prices[day] = np.nan
        else:
            stock_prices[day] = new_price_today
    return stock_prices
  
#Test1 we get the same result with 3 plots, if we set the set value to seed to 10002)
#fig, ax = plt.subplots(3, 1)

#prices = [100, 100, 100]
#vols = [0.5, 0.5, 0.5]
#sim_data = np.zeros([5*365, 3])
#for i in range(3):
    #sim_data[:, i] = generate_stock_price(5*365, 100, 0.5)
    #ax[i].plot(sim_data[:, i])
#plt.show()  
   
# function get_data for task 2.0
def get_data(method = 'read', initial_price = None, volatility =None): 
    '''
    Generates or reads simulation data for one or more stocks over 5 years,
    given their initial share price and volatility.
    
    Input:
        method (str): either 'generate' or 'read' (default 'read').
            If method is 'generate', use generate_stock_price() to generate
                the data from scratch.
            If method is 'read', use Numpy's loadtxt() to read the data
                from the file stock_data_5y.txt.
            
        initial_price (list): list of initial prices for each stock (default None)
            If method is 'generate', use these initial prices to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                starting price to each value in the list, and display an appropriate message.
        
        volatility (list): list of volatilities for each stock (default None).
            If method is 'generate', use these volatilities to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                volatility to each value in the list, and display an appropriate message.

        If no arguments are specified, read price data from the whole file.
        
    Output:
        sim_data (ndarray): NumPy array with N columns, containing the price data
            for the required N stocks each day over 5 years.
    
    Examples:
        Returns an array with 2 columns:
            >>> get_data(method='generate', initial_price=[150, 250], volatility=[1.8, 3.2])
            
        Displays a message and returns None:
            >>> get_data(method='generate', initial_price=[150, 200])
            Please specify the volatility for each stock.
            
        Displays a message and returns None:
            >>> get_data(method='generate', volatility=[3])
            Please specify the initial price for each stock.
        
        Returns an array with 2 columns and displays a message:
            >>> get_data(method='read', initial_price=[210, 58])
            Found data with initial prices [210, 100] and volatilities [1.2, 3.4].
        
        Returns an array with 1 column and displays a message:
            >>> get_data(volatility=[5.1])
            Found data with initial prices [380] and volatilities [5.2].
        
        If method is 'read' and both initial_price and volatility are specified,
        volatility will be ignored (a message is displayed to indicate this):
            >>> get_data(initial_price=[210, 58], volatility=[5, 7])
            Found data with initial prices [210, 100] and volatilities [1.2, 3.4].
            Input argument volatility ignored.
    
        No arguments specified, all default values, returns price data for all stocks in the file:
            >>> get_data()
    '''

    #create empty lists 
    sim_initial_price = [] 
    sim_volatility = [] 
    sim_loaded_data = np.loadtxt('stock_data_5y.txt',dtype=float, delimiter = ' ')
    
    if method == 'read'  :    
        if (initial_price is None and volatility is None):  
          sim_data = np.array(sim_loaded_data) 
          return sim_data          # return sim_data when nothing is specified 
           
        elif initial_price !=None and volatility !=None:  #when both initial_price and volality is present
            sim_data = np.zeros([1826, len(initial_price)]) #create an array sim_data
            for i in range(0, len(initial_price)):
                closest_stock_value =(np.abs(sim_loaded_data[1] - initial_price[i])).argmin() # we find the closest stock value 
                sim_initial_price.append(sim_loaded_data[1,closest_stock_value]) #add to initial price list 
                sim_volatility.append(sim_loaded_data[0,closest_stock_value]) # add to the volatility list
                sim_data[:,i] = sim_loaded_data[:, closest_stock_value] #update the sim_data with the closet stock value 
            
            print(f'Found data with initial prices {sim_initial_price} and volatilities {sim_volatility}')
            print(f'Input argument volatility is ignored')
       
        elif initial_price !=None:    # when the initial price is not given 
            sim_data = np.zeros([1826, len(initial_price)]) # create an empty array sim_data
            for i in range(0, len(initial_price)):
                closest_stock_value =(np.abs(sim_loaded_data[1] - initial_price[i])).argmin() # we find the closest stock value 
                sim_initial_price.append(sim_loaded_data[1,closest_stock_value]) #add to initial price list 
                sim_volatility.append(sim_loaded_data[0,closest_stock_value]) # add to the volatility list
                sim_data[:,i] = sim_loaded_data[:, closest_stock_value] #update the sim_data with the closet stock value
            
            print(f'Found data with initial prices {sim_initial_price} and volatilities {sim_volatility} ')                  
            
        elif initial_price == None and volatility != None:  #when initial price is given and volaitlity is not given 
            sim_data = np.zeros([1826, len(volatility)])
            for i in range(0, len(volatility)): 
                closest_stock_value =(np.abs(sim_loaded_data[0] - volatility[i])).argmin() # we find closest stock value 
                sim_initial_price.append(sim_loaded_data[1,closest_stock_value]) #add to initial price list 
                sim_volatility.append(sim_loaded_data[0,closest_stock_value]) # add to the volatility list
                sim_data[:,i] = sim_loaded_data[:, closest_stock_value]       # update the sim_data with the closest stock value
            print(f'Found data with initial price{sim_initial_price} and volatility {sim_volatility}')
            
            
    elif method == 'generate': # this was built arround the specifications of the doc string 
    
            if initial_price is None:  
                print("please specify the initial price for each stock")
                return None
          
            if volatility is None: 
                print("please specify the volatility for each stock")
                return None
            
            elif(initial_price != None and volatility != None):  #when the initial price and volatiltiy is not given 
                sim_data = np.zeros([1826, len(initial_price)])  # create an empty array sim data
                for i in range(len(initial_price)):
                    sim_data[:,i] = generate_stock_price(1826, initial_price[i], volatility[i])   #generate sim_data             
    return sim_data

        
