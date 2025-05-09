import MetaTrader5 as mt5
import os
import datetime as dt 
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np

# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# establish MetaTrader 5 connection to a specified trading account
"""if not mt5.initialize(login=25115284, server="MetaQuotes-Demo",password="4zatlbqx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()"""

#an easier way to establish connection is buy reading the login details from another file
#"os.chdir"--- to change file directory
file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5 Python\\keyfusionmarket.txt"
#file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5 Python\\key.txt"
key = open(file_path,"r").read().split()
path1 = "C:\\Users\\user\\AppData\\Roaming\\MetaTrader 5\\terminal64.exe"#For the executable path when we run the code

#since we are importing the user id we must convert it to an integer int(key[0])
if not mt5.initialize(path = path1, login= int(key[0]),password=key[1], server=key[2]):
    #print("initialize() failed, error code =",mt5.last_error())
    print("connection not established")
else:
    print("connection established")

#extract historical data
def get_hist_data_numeric_index(symbol, timeframe, start_pos=0, num_candles=100):
    """
    Parameters
    ----------
    symbol : TYPE str - e.g "USDCAD"
    timeframe : TYPE str - e.g. "TIMEFRAME_M15"
    start_pos : TYPE int -e.g. 0 means data till current time
    num_candles : TYPE int

    Returns
    -------
    historical data dataframe

    """
    
    
    hist_data = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), start_pos, num_candles)   
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df

hist_data = get_hist_data_numeric_index("USDCAD", "TIMEFRAME_H1") #get data till current time


#now we create a code for resistance and support
def get_hills_valleys(df, pip=0.0001):
    """
    Identifies 'hills' (local highs) and 'valleys' (local lows) in the price data.

    Parameters:
    df (DataFrame): The input DataFrame containing 'high' and 'low' price columns.
    pip (float): The pip value to define significant price movements.

    Returns:
    Series: A pandas Series indicating 'hill', 'valley', or an empty string.
    """
    df = df.copy()  # Create a copy to avoid modifying the original DataFrame

    # Define Valley (Local Low)
    is_valley = (
        (df["low"] < df["low"].shift(1) - 3 * pip) &
        (df["low"] < df["low"].shift(2) - 3 * pip) &
        (df["low"] < df["low"].shift(-1) - 3 * pip) &
        (df["low"] < df["low"].shift(-2) - 3 * pip)
    )

    # Define Hill (Local High)
    is_hill = (
        (df["high"] > df["high"].shift(1) + 3 * pip) &
        (df["high"] > df["high"].shift(2) + 3 * pip) &
        (df["high"] > df["high"].shift(-1) + 3 * pip) &
        (df["high"] > df["high"].shift(-2) + 3 * pip)
    )

    # Assign labels
    df["hill_valley"] = np.where(is_valley, "valley", np.where(is_hill, "hill", ""))

    return df["hill_valley"]

hist_data["hill_valley"] = get_hills_valleys(hist_data)

#print(support_resistance)


def get_support(list_of_lows,current_price,level_range=20,pip=0.0001,min_occurance=2):
    """
    
    Parameters
    ----------
    list_of_lows : list
        list of all the lows/valleys identified in a chart.
    current_price : float
        current price of the asset
    level_range : int, optional
        approximation range. The default is 20 pips.
    pip : float, optional
        pip unit for the given currency pair. The default is 0.0001.
    min_occurance : int, optional
        minimum occurance of a low to be considered important enough level. The default is 2.

    Returns
    -------
    support_levels : list
        list of all support levels.

    """
    support_levels = [] #to store all support levels
    remove_index = [] #to store all the indices that have already been used to calculate a support level
    for indx,low in enumerate(list_of_lows):#enumerate function provides both the idex and the element of a list when iterating
        if indx in remove_index:
            continue
        count = 0
        lows = []
        for j in list_of_lows[indx:]:
            if abs(low - j) < level_range*pip:
                count+=1
                lows.append(j)
        #print(lows)
        if count > min_occurance:
            support_levels.append(sum(lows)/len(lows)) if (sum(lows)/len(lows)) < current_price else support_levels
            #remove all points which were used to calculate the above support level
            for k in lows:
                remove_index.append(list_of_lows.index(k)) if list_of_lows.index(k) not in remove_index else remove_index          
    
    if len(support_levels) == 0:
        if min(list_of_lows) < current_price:
            return min(list_of_lows)
        else:
            return current_price
    
    elif list_of_lows.index(min(list_of_lows)) > int(0.7*len(list_of_lows)): #if a major trough occured recently then that becomes the support
        return min(list_of_lows)
    
    else:
        return sorted(support_levels, reverse=True)[0] #by default return the closest (wrt current price) frequently touched support level

current_p = (mt5.symbol_info_tick('USDCAD').bid + mt5.symbol_info_tick('USDCAD').ask)/2
valleys = hist_data[hist_data["hill_valley"]=="valley"].low.to_list()
while hist_data["hill_valley"]=="valley":
    valley = hist_data.low.to_list()
support = get_support(valleys,current_p)
print(support)


def get_resistence(list_of_highs,current_price,level_range=20,pip=0.0001,min_occurance=2):
    """
    
    Parameters
    ----------
    list_of_highs : list
        list of all the highs/hills identified in a chart.
    current_price : float
        current price of the asset
    level_range : int, optional
        approximation range. The default is 20 pips.
    pip : float, optional
        pip unit for the given currency pair. The default is 0.0001.
    min_occurance : int, optional
        minimum occurance of a highs to be considered important enough level. The default is 2.

    Returns
    -------
    support_levels : list
        list of all support levels.

    """
    resistance_levels = [] #to store all resistance levels
    remove_index = [] #to store all the indices that have already been used to calculate a resistance level
    for indx,high in enumerate(list_of_highs):
        if indx in remove_index:
            continue
        count = 0
        highs = []
        for j in list_of_highs[indx:]:
            if abs(high - j) < level_range*pip:
                count+=1
                highs.append(j)
        #print(highs)
        if count > min_occurance:
            resistance_levels.append(sum(highs)/len(highs)) if (sum(highs)/len(highs)) > current_price else resistance_levels
            #remove all points which were used to calculate the above resistance level
            for k in highs:
                remove_index.append(list_of_highs.index(k)) if list_of_highs.index(k) not in remove_index else remove_index
                
    
    if len(resistance_levels) == 0:
        if max(list_of_highs) > current_price:
            return max(list_of_highs)
        else:
            return current_price
        
    elif list_of_highs.index(max(list_of_highs)) > int(0.7*len(list_of_highs)): #if a major peak occurred recently then that becomes the resistance
        return max(list_of_highs)
    
    else:
        return sorted(resistance_levels, reverse=True)[0] #by default return the closest (wrt current price) frequently touched resistance level
