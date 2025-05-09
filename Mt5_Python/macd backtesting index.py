import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import datetime as dt

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

def get_current_price(symbol):
    return (mt5.symbol_info_tick(symbol).bid + mt5.symbol_info_tick(symbol).ask)/2

def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  

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

#hist_data = get_hist_data_numeric_index("USDCAD", "TIMEFRAME_H1")


#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL INDICATOR WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

def EMA(ser, n=9):
    ema = ser.ewm(n, adjust=False).mean()  # Built-in EMA calculation
    return ema


def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["ma_fast"] = EMA(df["close"],a)
    df["ma_slow"] = EMA(df["close"],b)
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = EMA(df["macd"],c)
    df["histogram"] = df["macd"] - df["signal"]
    return df[["macd","signal","histogram"]]



#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THW CODE WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING


symbol = "EURUSD"
# The code `backtest_timeframe` is likely a variable or function name in Python. Without seeing the
# actual implementation of `backtest_timeframe`, it is not possible to determine exactly what it is
# doing. It could be used to specify a timeframe for backtesting financial data or performing some
# other related task.
backtest_timeframe = "TIMEFRAME_M30"
#supp_res_timeframe = "TIMEFRAME_H4"
candle_data = get_hist_data_numeric_index(symbol,backtest_timeframe,start_pos=0,num_candles=17520)

candle_data[["macd","signal","histogram"]] = MACD(candle_data)



signal = None
candle_data["returns"] = 0.0
trade_stats = []
macd_index = candle_data.columns.to_list().index("macd")
op_index = candle_data.columns.to_list().index("open")
cp_index = candle_data.columns.to_list().index("close")
hi_index = candle_data.columns.to_list().index("high")
lo_index = candle_data.columns.to_list().index("low")
returns_index = candle_data.columns.to_list().index("returns")

# Define Forex sessions outside the loop
FOREX_SESSIONS = {
    "Sydney": {"start": 22, "end": 7},    # 10 PM - 7 AM UTC
    "Tokyo": {"start": 0, "end": 9},      # 12 AM - 9 AM UTC
    "London": {"start": 7, "end": 16},    # 7 AM - 4 PM UTC
    "New York": {"start": 12, "end": 21}  # 12 PM - 9 PM UTC
}

def get_active_session(current_time_utc):
    """Determine active Forex sessions for a given UTC time."""
    current_hour = current_time_utc.hour
    active = []
    for session, hours in FOREX_SESSIONS.items():
        start, end = hours["start"], hours["end"]
        if start <= end:
            if start <= current_hour < end:
                active.append(session)
        else:
            if current_hour >= start or current_hour < end:
                active.append(session)
    return active

for i in range(8,len(candle_data)-1):
    
    current_time_utc = candle_data.index[i].to_pydatetime().replace(tzinfo=timezone.utc)
    active_sessions = get_active_session(current_time_utc)
    
    if signal == None and ( "London" in active_sessions ) :
        if candle_data.iloc[i,macd_index]>0 and candle_data.iloc[i-1,macd_index]>0 and (candle_data.iloc[i-8:i-1,macd_index] < 0).all():
            signal = 'long'
            #[supp, res] = find_support_res(symbol,supp_res_timeframe,time_till=candle_data.index[i].strftime('%Y-%m-%d %H:%M:%S'),current_price=candle_data.iloc[i+1,op_index])
            # Ensure time_till is always a string
            #print(f"time_till1 type: {type(time_till1)}, value: {time_till1}"
            trade_stats.append({"time":candle_data.index[i],
                                "dir":"long",
                                "open_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]), #factor slippage
                                "close_price": None,
                                "sl_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]) - 30*get_pip(symbol),
                                "tp_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]) + 60*get_pip(symbol)})
            """
            if trade_stats[-1]["open_price"] <= trade_stats[-1]["sl_price"]:
                trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"] - 80*get_pip(symbol)
            if trade_stats[-1]["open_price"] >= trade_stats[-1]["tp_price"]:
                trade_stats[-1]["tp_price"] = trade_stats[-1]["open_price"] + 80*get_pip(symbol)
            """
        elif candle_data.iloc[i,macd_index]<0 and candle_data.iloc[i-1,macd_index]<0 and (candle_data.iloc[i-8:i-1,macd_index] > 0).all():
            signal = 'short'
            trade_stats.append({"time":candle_data.index[i],
                                "dir":"short",
                                "open_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]),
                                "close_price": None,
                                "sl_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]) + 30*get_pip(symbol),
                                "tp_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]) - 60*get_pip(symbol)})  
            
    
    elif signal == "long" and ( "London" in active_sessions) :
        #check if stop loss got triggered
        if trade_stats[-1]["sl_price"] > candle_data.iloc[i,lo_index]:
            signal = None
            trade_stats[-1]["close_price"] = trade_stats[-1]["sl_price"]
            #candle_data.iloc[i,"return"] = (trade_stats[-1]["close_price"] - candle_data.iloc[i,op_index])/get_pip(mt5, symbol) #update return
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"] - trade_stats[-1]["open_price"])/get_pip(symbol)
        #check if the MACD based signal reversed which would imply exiting position even though SL may not have reached
        elif (candle_data.iloc[i-2:,macd_index] < 0).all():
            signal = None
            trade_stats[-1]["close_price"] = candle_data.iloc[i+1,op_index]
            #candle_data.iloc[i,"return"] = (trade_stats[-1]["close_price"] - candle_data.iloc[i,op_index])/get_pip(mt5, symbol)
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"] - trade_stats[-1]["open_price"])/get_pip(symbol)
        #check if take profit got triggered
        elif trade_stats[-1]["tp_price"] < candle_data.iloc[i,hi_index]:
            signal = None
            trade_stats[-1]["close_price"] = trade_stats[-1]["tp_price"]
            #candle_data.iloc[i,"return"] = (trade_stats[-1]["close_price"] - candle_data.iloc[i,op_index])/get_pip(mt5, symbol)
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"] - trade_stats[-1]["open_price"])/get_pip(symbol)
        elif candle_data.iloc[i,hi_index] > (trade_stats[-1]["open_price"] + 45*get_pip(symbol)):
            trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"]
        #else:
            #candle_data.iloc[i,returns_index] = (candle_data.iloc[i,cp_index] - candle_data.iloc[i,op_index])/get_pip(symbol)
            
    elif signal == "short" and ( "London" in active_sessions ):
        if trade_stats[-1]["sl_price"] < candle_data.iloc[i,hi_index]:
            signal = None
            trade_stats[-1]["close_price"] = trade_stats[-1]["sl_price"]
            #candle_data.iloc[i,"return"] = (candle_data.iloc[i,op_index] - trade_stats[-1]["close_price"])/get_pip(mt5, symbol)
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"] - trade_stats[-1]["close_price"])/get_pip(symbol)
        elif (candle_data.iloc[i-2:,macd_index] > 0).all():
            signal = None
            trade_stats[-1]["close_price"] = candle_data.iloc[i+1,op_index]
            #candle_data.iloc[i,"return"] = (candle_data.iloc[i,op_index] - trade_stats[-1]["close_price"])/get_pip(mt5, symbol)
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"] - trade_stats[-1]["close_price"])/get_pip(symbol)            
        elif trade_stats[-1]["tp_price"] > candle_data.iloc[i,lo_index]:
            signal = None
            trade_stats[-1]["close_price"] = trade_stats[-1]["tp_price"]
            #candle_data.iloc[i,"return"] = (candle_data.iloc[i,op_index] - trade_stats[-1]["close_price"])/get_pip(mt5, symbol)
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"] - trade_stats[-1]["close_price"])/get_pip(symbol)
        elif candle_data.iloc[i,lo_index] < (trade_stats[-1]["open_price"] - 45*get_pip(symbol)):
            trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"]
        #else:
            #candle_data.iloc[i,returns_index] = (candle_data.iloc[i,op_index] - candle_data.iloc[i,cp_index])/get_pip(symbol)
            
#print("Trade Stats:", trade_stats)  # Check if any trades exist


if trade_stats and trade_stats[-1]["close_price"] == None:
    trade_stats[-1]["close_price"] = candle_data.iloc[-1,cp_index] 


retun = candle_data['returns'][(candle_data['returns'] > 0) | (candle_data['returns'] < 0)].to_list()
print(retun)

for indx,trades in enumerate( trade_stats):
    print(f"{trades} ")
    print()

print("Number of trades taken:", len(trade_stats))
print()
print("Number of trades taken(candle data):", len(retun))
print()
print("Candle Data Length:", len(candle_data))  # Check if data exists
print()
count1 = 0
count2 = 0
positive = 0.0
negative = 0.0
for t in retun:
    if t < 0:
        count1 +=1
        negative +=t
    if t > 0:
        count2 +=1
        positive +=t

sum1 = count1 + count2 
percentage_gain = (100 * count2)/sum1
percentage_loss = (100 * count1)/sum1
print(f"\n percentage gain: {percentage_gain:.2f}% | percentage loss: {percentage_loss:.2f}%")
print()
print(f"\n you gained: {positive:.2f}pips | you lost: {negative:.2f}pips")
"""
print(candle_data['returns'])
# Sum all returns (in pips)
total_returns_pips = candle_data['returns'].sum()

# Convert to percentage (assuming 1 pip = 1% of capital, adjust multiplier as needed)
# Example: If 1 pip = 0.1% risk, use total_returns_pips * 0.1
risk_per_pip = 0.1  # Adjust based on your risk model
total_returns_percent = total_returns_pips * risk_per_pip

print(f"\nTotal Returns: {total_returns_pips:.2f} pips | {total_returns_percent:.2f}%")
print(f"\n percentage gain: {percentage_gain:.2f}% | percentage loss: {percentage_loss:.2f}%")
print(f"\n you gained: {positive:.2f}pips | you lost: {negative:.2f}pips")

print()
"""

