# -*- coding: utf-8 -*-
"""
MetaTrader5 - MT5 python API utility functions

@author: Mayank
"""

import datetime as dt
import pandas as pd
import numpy as np
import pytz
import smtplib

    
def get_current_price(mt5, symbol):
    return (mt5.symbol_info_tick(symbol).bid + mt5.symbol_info_tick(symbol).ask)/2

def get_pip(mt5, symbol):
    return 10*mt5.symbol_info(symbol).point  
  
#extract historical data
def get_hist_data(mt5, symbol, timeframe, time_till=None, num_candles=200):
    """
    Parameters
    ----------
    symbol : TYPE str - e.g "USDCAD"
    timeframe : TYPE str - e.g. "TIMEFRAME_M15"
    time_till : TYPE str -e.g. "YYYY-MM-DD HH:MM:SS"
    num_candles : TYPE int

    Returns
    -------
    historical data dataframe

    """
    #pytz.all_timezones
    current_tz = pytz.timezone("Asia/Kolkata") #change this based on your location
    eet_tz = pytz.timezone("Europe/Kyiv")
    required_tz = pytz.timezone("Etc/UTC")
    
    if time_till == None:
        time_till = current_tz.localize(dt.datetime.now()).replace(tzinfo=required_tz)
    else:
        time_till = eet_tz.localize(dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")).replace(tzinfo=required_tz)
    
    hist_data = mt5.copy_rates_from(symbol, getattr(mt5, timeframe), time_till, num_candles)   
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df

def get_hist_data_numeric_index(mt5, symbol, timeframe, start_pos=0, num_candles=200):
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

def get_hills_valleys(df,pip=0.0001):
    hist_data_df = df.copy()
    hist_data_df["hill_valley"] = np.where(np.logical_and((np.logical_and((hist_data_df.low < hist_data_df.low.shift(1) - 3*pip),
                                                                          (hist_data_df.low < hist_data_df.low.shift(2) - 3*pip)
                                                                         )
                                                           ),  
                                                          (np.logical_and((hist_data_df.low < hist_data_df.low.shift(-1) - 3*pip),
                                                                          (hist_data_df.low < hist_data_df.low.shift(-2) - 3*pip)
                                                                          )
                                                           )
                                                          ),
                                           "valley",
                                           np.where(np.logical_and((np.logical_and((hist_data_df.high > hist_data_df.high.shift(1) + 3*pip),
                                                                                   (hist_data_df.high > hist_data_df.high.shift(2) + 3*pip)
                                                                                  )
                                                                    ),  
                                                                    (np.logical_and((hist_data_df.high > hist_data_df.high.shift(-1) + 3*pip),
                                                                                    (hist_data_df.high > hist_data_df.high.shift(-2) + 3*pip)
                                                                                   )
                                                                     )
                                                                    ),
                                                    "hill",""
                                                    ),
                                           )
    
    return hist_data_df["hill_valley"]


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
    for indx,low in enumerate(list_of_lows):
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
    
    if list_of_lows.index(min(list_of_lows)) > int(0.7*len(list_of_lows)): #if a major trough occured recently then that becomes the support
        return min(list_of_lows)
    
    elif len(support_levels) == 0:
        return min(list_of_lows)
    
    else:
        return sorted(support_levels, reverse=True)[0] #by default return the closest frequently touched support level

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
        minimum occurance of a low to be considered important enough level. The default is 2.

    Returns
    -------
    support_levels : list
        list of all support levels.

    """
    resistence_levels = [] #to store all resistence levels
    remove_index = [] #to store all the indices that have already been used to calculate a resistence level
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
            resistence_levels.append(sum(highs)/len(highs)) if (sum(highs)/len(highs)) > current_price else resistence_levels
            #remove all points which were used to calculate the above resistence level
            for k in highs:
                remove_index.append(list_of_highs.index(k)) if list_of_highs.index(k) not in remove_index else remove_index
                
    
    if len(resistence_levels) == 0:
        if max(list_of_highs) > current_price:
            return max(list_of_highs)
        else:
            return current_price
        
    elif list_of_highs.index(max(list_of_highs)) > int(0.7*len(list_of_highs)): #if a major peak occured recently then that becomes the resistence
        return max(list_of_highs)
    
    else:
        return sorted(resistence_levels)[0] #by default return the closest frequently touched resistence level
  
                                          