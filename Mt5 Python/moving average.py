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


def get_hist_data_numeric_index(symbol, timeframe, start_pos=0, num_candles=200):
    #The numbering of bars goes from present to past. Thus, 
    # the zero bar means the current one. Required unnamed parameter.
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

hist1_data = get_hist_data_numeric_index("USDCAD", "TIMEFRAME_M30") #get data till current time
#print(hist1_data)

def SMA(ser, n=9):
    return ser.rolling(n).mean()

def EMA(ser, n=9):
    multiplier = 2/(n+1)    
    sma = ser.rolling(n).mean()
    ema = np.full(len(ser), np.nan)
    ema[len(sma) - len(sma.dropna())] = sma.dropna()[0]
    for i in range(len(ser)):
        if not np.isnan(ema[i-1]):
            ema[i] = ((ser.iloc[i] - ema[i-1])*multiplier) + ema[i-1]
    ema[len(sma) - len(sma.dropna())] = np.nan
    return ema

hist1_data["ema"] = EMA(hist1_data.close)



#_____________________________________________________________________________________________________________________________
#THIS IS A SIMPLER WAY TO GET THE SMA AND EMA USING THE BUILT IN PANDA FUNCTIONS

#FOR SMA
"""def get_hist_data(symbol, timeframe, num_candles=200):
    rates = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), 0, num_candles)
    mt5.shutdown()
    
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)

    # Efficient SMA calculation using rolling().mean()
    df["sma"] = df["close"].rolling(window=9).mean()  
    return df

hist_data = get_hist_data("USDCAD", "TIMEFRAME_H1")
print(hist_data.tail())"""


#FOR EMA
"""def get_hist_data(symbol, timeframe, num_candles=200):
    rates = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), 0, num_candles)
    mt5.shutdown()
    
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.set_index("time", inplace=True)
    df["ema"] = df["close"].ewm(span=9, adjust=False).mean()  # Built-in EMA calculation
    return df

hist_data = get_hist_data("USDCAD", "TIMEFRAME_H1")
print(hist_data.tail())"""