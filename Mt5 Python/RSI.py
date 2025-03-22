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

def RMA(ser, n=9):
    multiplier = 1/n    
    sma = ser.rolling(n).mean()
    ema = np.full(len(ser), np.nan)
    ema[len(sma) - len(sma.dropna())] = sma.dropna()[0]
    for i in range(len(ser)):
        if not np.isnan(ema[i-1]):
            ema[i] = ((ser.iloc[i] - ema[i-1])*multiplier) + ema[i-1]
    ema[len(sma) - len(sma.dropna())] = np.nan
    return ema

def RSI(DF, n=5):
    df = DF.copy()
    df["change"] = df["close"] - df["close"].shift(1)#".shift(1)" indicates the close of the previous candle
    df["gain"] = np.where(df["change"]>0,df["change"],0)
    df["loss"] = np.where(df["change"]<=0,-1*df["change"],0)
    df["avgGain"] = RMA(df["gain"],n)
    df["avgLoss"] = RMA(df["loss"],n)
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["rsi"] = 100 - (100/(1+df["rs"]))
    return df["rsi"]

hist_data["rsi"] = RSI(hist_data)



#________________________________________________________________________________________________________________________________
#THIS IS A SIMPLER METHOD OF CODING THE RSI
"""def RMA(series, period):
    #  Calculate the Relative Moving Average (RMA) using Pandas.
    return series.ewm(alpha=1/period, adjust=False).mean()

def RSI(series, period=14):
    #Calculate the RSI using RMA for smoothing.
    delta = np.diff(series, prepend=series[0])  # Compute price changes(prepend=series[0] means 
    that the first difference will be 0 (since it's first value - first value).)
    gain = pd.Series(np.where(delta > 0, delta, 0))  # Keep only gains
    loss = pd.Series(np.where(delta < 0, -delta, 0))  # Keep only losses

    avg_gain = RMA(gain, period)
    avg_loss = RMA(loss, period)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Example usage:
data = pd.DataFrame({"close": [10, 20, 30, 40, 50, 40, 30, 20, 10, 15, 25, 35]})
data["rsi"] = RSI(data["close"].values, period=14)

print(data)"""