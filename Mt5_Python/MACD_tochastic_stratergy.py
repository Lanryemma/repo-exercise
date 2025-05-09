import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import datetime as dt
import pytz
from Stratergy_evaluation import win_rate,mean_ret_winner_pip,mean_ret_loser_pip,max_drawdown


# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

# establish MetaTrader 5 connection to a specified trading account
"""if not mt5.initialize(login=25115284, server="MetaQuotes-Demo",password="4zatlbqx"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()"""

#an easier way to establish connection is buy reading the login details from another file
#"os.chdir"--- to change file directory
file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5_Python\\keyfusionmarket.txt"
#file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5 Python\\key.txt"
key = open(file_path,"r").read().split()
path1 = "C:\\Users\\user\\AppData\\Roaming\\MetaTrader 5\\terminal64.exe"#For the executable path when we run the code

#since we are importing the user id we must convert it to an integer int(key[0])
if not mt5.initialize(path = path1, login= int(key[0]),password=key[1], server=key[2]):
    #print("initialize() failed, error code =",mt5.last_error())
    print("connection not established")
else:
    print("connection established")

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL INDICATOR WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  

def SMA(DF, n=200):
    df = DF.copy()
    df["sma"] = df["close"].rolling(n).mean()
    return df["sma"]
    

def stochastic(DF, lookback=14, k=3, d=3):
    """function to calculate Stochastic Oscillator
    lookback = lookback period
    k and d = moving average window for %K and %D"""
    df = DF.copy()
    df["HH"] = df["high"].rolling(lookback).max()
    df["LL"] = df["low"].rolling(lookback).min()
    df["%k"] = (100 * (df["close"] - df["LL"])/(df["HH"]-df["LL"])).rolling(k).mean()
    df["%d"] = df["%k"].rolling(d).mean()
    return df[["%k","%d"]]

def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["ma_fast"] = EMA(df["close"],a)
    df["ma_slow"] = EMA(df["close"],b)
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = EMA(df["macd"],c)
    df["histogram"] = df["macd"] - df["signal"]
    return df[["macd","signal","histogram"]]

def EMA(ser, n=9):
    ema = ser.ewm(n, adjust=False).mean()  # Built-in EMA calculation
    return ema
"""
def get_hist_data(symbol, timeframe,num_candles, time_till=None ):

    #pytz.all_timezones
    current_tz = pytz.timezone("Africa/Lagos") #change this based on your location
    eet_tz = pytz.timezone("Europe/Kyiv")
    #required_tz = pytz.timezone("Etc/UTC")
    
    
    required_tz = pytz.timezone("Etc/UTC")  # UTC timezone

    if time_till == None:
        time_till = current_tz.localize(dt.datetime.now()).replace(tzinfo=required_tz)
    else:
        if isinstance(time_till, (int, float)):
            time_till = dt.datetime.fromtimestamp(time_till, tz=required_tz)
        elif isinstance(time_till, str):
            time_till = eet_tz.localize(dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S").replace(tzinfo=required_tz))
        else:
            raise ValueError("Invalid time_till format. Use Unix timestamp (int/float) or string.")
    
    print(f"Fetching data for: {symbol}")
    print(f"Timeframe: {timeframe}")
    print(f"Time till (UTC): {time_till}")
    print(f"Requested candles: {num_candles}")
    
    hist_data = mt5.copy_rates_from(symbol, getattr(mt5, timeframe), time_till, num_candles) 
    if hist_data is None:
        print(f"Failed to fetch data. MT5 Error: {mt5.last_error()}")
        return pd.DataFrame()
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df

    
        if time_till == None:
            time_till = current_tz.localize(dt.datetime.now()).replace(tzinfo=required_tz)
        else:
            time_till = eet_tz.localize(dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")).replace(tzinfo=required_tz)
    """
def get_hist_data_numeric_index(symbol, timeframe, start_pos=0, num_candles=None):
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

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THE CODE WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

symbol = "USDCAD"
backtest_timeframe = "TIMEFRAME_H1"
#candle_data = get_hist_data(symbol,backtest_timeframe,num_candles=70080, time_till=None)
candle_data = get_hist_data_numeric_index(symbol,backtest_timeframe, start_pos=0, num_candles=22000)

#add technical indicators
candle_data["sma"] = SMA(candle_data)       
candle_data[["macd","signal","histogram"]] = MACD(candle_data)
candle_data[["%k","%d"]] = stochastic(candle_data) 
candle_data.dropna(inplace=True)

def stochastic_bullish_cross_within_n_period(candle_data, curr_idx, n=3):
    k_index = candle_data.columns.to_list().index("%k")
    d_index = candle_data.columns.to_list().index("%d")
    #range(start, stop, step)
    for i in range(curr_idx,curr_idx-n,-1):
        if candle_data.iloc[i,k_index]>candle_data.iloc[i,d_index] and \
           (candle_data.iloc[i-5:i,k_index] - candle_data.iloc[i-5:i,d_index] < 0).all():
               return True
    return False


def stochastic_bearish_cross_within_n_period(candle_data, curr_idx, n=3):
    k_index = candle_data.columns.to_list().index("%k")
    d_index = candle_data.columns.to_list().index("%d")
    for i in range(curr_idx,curr_idx-n,-1):
        if candle_data.iloc[i,k_index]<candle_data.iloc[i,d_index] and \
           (candle_data.iloc[i-5:i,k_index] - candle_data.iloc[i-5:i,d_index] > 0).all():
               return True
        
    return False
    

signal = None
candle_data["returns"] = 0
trade_stats = []
sma_index = candle_data.columns.to_list().index("sma")
macd_index = candle_data.columns.to_list().index("macd")
signal_index = candle_data.columns.to_list().index("signal")
hstgrm_index = candle_data.columns.to_list().index("histogram")
k_index = candle_data.columns.to_list().index("%k")
d_index = candle_data.columns.to_list().index("%d")
op_index = candle_data.columns.to_list().index("open")
cp_index = candle_data.columns.to_list().index("close")
hi_index = candle_data.columns.to_list().index("high")
lo_index = candle_data.columns.to_list().index("low")
returns_index = candle_data.columns.to_list().index("returns")

for i in range(5,len(candle_data)-1):
    if signal == None:
        if candle_data.iloc[i,cp_index] > candle_data.iloc[i,sma_index] and \
           candle_data.iloc[i,hstgrm_index]>0 and \
           (candle_data.iloc[i-5:i,hstgrm_index] < 0).all()and \
           stochastic_bullish_cross_within_n_period(candle_data, i):
               signal = 'long'
               trade_stats.append({"time":candle_data.index[i],
                                "dir":"long",
                                "open_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]), #factor slippage
                                "close_price": None,
                                "sl_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]) - 31*get_pip(symbol),
                                "tp_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]) + 60*get_pip(symbol)})

        elif candle_data.iloc[i,cp_index] < candle_data.iloc[i,sma_index] and \
             candle_data.iloc[i,hstgrm_index]<0 and \
             (candle_data.iloc[i-5:i,hstgrm_index] > 0).all() and \
             stochastic_bearish_cross_within_n_period(candle_data, i):
               signal = 'short'
               trade_stats.append({"time":candle_data.index[i],
                                "dir":"short",
                                "open_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]),
                                "close_price": None,
                                "sl_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]) + 31*get_pip(symbol),
                                "tp_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]) - 60*get_pip(symbol)})  
                 
                        
    elif signal == "long":
        #check if the MACD based signal reversed which would imply exiting position even though SL may not have reached
        if candle_data.iloc[i,hstgrm_index]<0 and (candle_data.iloc[i-5:i,hstgrm_index] > 0).all():
            signal = None
            trade_stats[-1]["close_price"] = candle_data.iloc[i+1,op_index]
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"] - trade_stats[-1]["open_price"])/get_pip(symbol)
            #candle_data.iloc[i,-1] = (trade_stats[-1]["close_price"] - candle_data.iloc[i,op_index])/get_pip(symbol)
        elif candle_data.iloc[i,hi_index] > trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif candle_data.iloc[i,lo_index] < trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif candle_data.iloc[i,hi_index] > (trade_stats[-1]["open_price"] + 45*get_pip(symbol)):
            trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"]
        #else:
            #candle_data.iloc[i,returns_index] = (candle_data.iloc[i,cp_index] - candle_data.iloc[i,op_index])/get_pip(symbol)
            
    elif signal == "short":
        if candle_data.iloc[i,hstgrm_index]>0 and (candle_data.iloc[i-5:i,hstgrm_index] < 0).all():
            signal = None
            trade_stats[-1]["close_price"] = candle_data.iloc[i+1,op_index]
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"] - trade_stats[-1]["close_price"])/get_pip(symbol) 
            #candle_data.iloc[i,-1] = (candle_data.iloc[i,op_index] - trade_stats[-1]["close_price"])/get_pip(symbol) 
            
        elif candle_data.iloc[i,lo_index] < trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        elif candle_data.iloc[i,hi_index] > trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
            
        #else:
            #candle_data.iloc[i,returns_index] = (candle_data.iloc[i,op_index] - candle_data.iloc[i,cp_index])/get_pip(symbol)
            
if trade_stats and trade_stats[-1]["close_price"] == None:
    trade_stats[-1]["close_price"] = candle_data.iloc[-1,cp_index] #update the cp of last trade as the current price

#plot equity curve in terms of pip

for indx,trades in enumerate( trade_stats):
    print(f"{trades} ")

#print backtesting results
print("cumulative return in pips = ",candle_data["returns"].cumsum()[-1])
print("win rate of the strategy = {:.2f}%".format(win_rate(trade_stats)))
print("average pip return per winning trade = {:.2f}".format(mean_ret_winner_pip(trade_stats, symbol)))
print("average pip return per losing trade = {:.2f}".format(mean_ret_loser_pip(trade_stats, symbol)))
print("maximum drawdown in pips = {:.2f}".format(max_drawdown(candle_data)))

print("Number of trades taken:", len(trade_stats))

candle_data["returns"].cumsum().plot()