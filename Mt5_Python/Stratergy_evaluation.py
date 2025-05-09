import MetaTrader5 as mt5
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THW CODE WE ARE GOING TO USE FOR THE STRATEGY WIN RATE AND DRAW DOWN 
def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point

def win_rate(trade_stats):
    win_count = 0
    lose_count = 0
    for ts in trade_stats:
        if ts['dir']=="long":
            if ts['close_price'] >= ts['open_price']:
                win_count += 1
            else:
                lose_count+=1
                
        elif ts['dir']=="short":
            if ts['close_price'] <= ts['open_price']:
                win_count += 1
            else:
                lose_count+=1

    return (win_count/(win_count+lose_count))*100

def mean_ret_winner_pip(trade_stats,symbol):
    win_ret = []
    for ts in trade_stats:
        if ts['dir']=="long":
            if ts['close_price'] >= ts['open_price']:
                win_ret.append((ts['close_price'] - ts['open_price'])/get_pip(symbol))
                
        elif ts['dir']=="short":
            if ts['close_price'] <= ts['open_price']:
                win_ret.append((ts['open_price'] - ts['close_price'])/get_pip(symbol))
    
    return sum(win_ret)/len(win_ret)

def mean_ret_loser_pip(trade_stats,symbol):
    win_ret = []
    for ts in trade_stats:
        if ts['dir']=="long":
            if ts['close_price'] < ts['open_price']:
                win_ret.append((ts['close_price'] - ts['open_price'])/get_pip(symbol))
                
        elif ts['dir']=="short":
            if ts['close_price'] > ts['open_price']:
                win_ret.append((ts['open_price'] - ts['close_price'])/get_pip(symbol))
        
    return sum(win_ret)/len(win_ret)

def max_drawdown(candle_data):
    "function to calculate max drawdown"
    df = candle_data.copy()
    df["cum_return"] = df["returns"].cumsum()
    df["cum_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_max"] - df["cum_return"]
    return df["drawdown"].max()

