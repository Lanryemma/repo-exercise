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


#NOW WE CALCULATE THE MACD 
#extract historical data
def get_hist_data_numeric_index(symbol, timeframe, start_pos=0, num_candles=200):
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

def SMA(ser, n=9):
    return ser.rolling(n).mean()

def EMA(ser, n=9):
    multiplier = 2/(n+1)
    sma = SMA(ser, n)
    ema = np.full(len(ser),np.nan)
    ema[len(sma) - len(sma.dropna())] = sma.dropna()[0]
    for i in range(len(ser)):
        if not np.isnan(ema[i-1]):
            ema[i] = ((ser.iloc[i] - ema[i-1])*multiplier) + ema[i-1]
    return ema


def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["ma_fast"] = EMA(df["close"], a)
    df["ma_slow"] = EMA(df["close"], b)
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = EMA(df["macd"], c)
    df["histogram"] = df["macd"] - df["signal"]
    return df[["macd","signal","histogram"]]
    
hist_data[["macd","signal","histogram"]] = MACD(hist_data)
print(hist_data)


#________________________________________________________________________________________________________________________________
#THIS IS A SIMPLER METHOD OF CODING THE MACD
"""def calculate_macd(df, short_span=12, long_span=26, signal_span=9):
    #Compute MACD line, Signal line, and Histogram.
    df["macd"] = df["close"].ewm(span=short_span, adjust=False).mean() - df["close"].ewm(span=long_span, adjust=False).mean()
    df["signal"] = df["macd"].ewm(span=signal_span, adjust=False).mean()
    df["histogram"] = df["macd"] - df["signal"]
    return df

# Fetch historical data and calculate MACD
hist_data = get_hist_data("USDCAD", "TIMEFRAME_H1")
macd_data = calculate_macd(hist_data)

print(macd_data.tail())  # Display last few rows with MACD values"""