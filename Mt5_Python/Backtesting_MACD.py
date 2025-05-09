import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import pytz
import datetime as dt
import matplotlib.pyplot as plot
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
"""
symbol = "USDCAD"
timeframe = mt5.TIMEFRAME_D1
time_till = dt.datetime(2023, 10, 1, tzinfo=pytz.utc)  # Past date
num_candles = 100  # Small test value

hist_data1 = mt5.copy_rates_from(symbol, timeframe, time_till, num_candles)
hist_data_df1 = pd.DataFrame(hist_data1) 
hist_data_df1.time = pd.to_datetime(hist_data_df1.time, unit="s")
hist_data_df1.set_index("time", inplace=True)
if hist_data_df1 is not None:
    print("Success! Data fetched for:", pd.DataFrame(hist_data_df1).tail())
else:
    print("Failed. MT5 Error:", mt5.last_error())
"""
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL UTILITIES WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING


def get_current_price(symbol):
    return (mt5.symbol_info_tick(symbol).bid + mt5.symbol_info_tick(symbol).ask)/2

def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  


#extract historical data
def get_hist_data(symbol, timeframe,num_candles, time_till=None ):
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
    """
    if isinstance(time_till, (int, float)):
            time_till = str(pd.to_datetime(time_till, unit='s'))
    elif not isinstance(time_till, str):
            raise TypeError(f"Unexpected type for time_till: {type(time_till)}")
    """
    #pytz.all_timezones
    #current_tz = pytz.timezone("Africa/Lagos") #change this based on your location
    #eet_tz = pytz.timezone("Europe/Kyiv")
    #required_tz = pytz.timezone("Etc/UTC")
    
    
    required_tz = pytz.timezone("Etc/UTC")  # UTC timezone

    if time_till is None:
        # Set to previous day at 23:59:59 UTC
        time_till = dt.datetime.now(required_tz) - dt.timedelta(days=1)
        time_till = time_till.replace(hour=23, minute=59, second=59, microsecond=0)
    else:
        if isinstance(time_till, (int, float)):
            # Handle Unix timestamp (seconds since epoch)
            if time_till > 1e12:  # Check for milliseconds timestamp
                time_till = time_till / 1000
            time_till = dt.datetime.fromtimestamp(time_till, tz=required_tz)
        elif isinstance(time_till, str):
            # Parse string directly as UTC time
            time_till = dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")
            time_till = required_tz.localize(time_till)
        else:
            raise ValueError("Invalid time_till format. Use Unix timestamp (int/float) or string in '%Y-%m-%d %H:%M:%S' format.")



    """
    if time_till == None:
        time_till = current_tz.localize(dt.datetime.now()).replace(tzinfo=required_tz)
    else:
    //
        if time_till == None:
            time_till = current_tz.localize(dt.datetime.now()).replace(tzinfo=required_tz)
        else:
            time_till = eet_tz.localize(dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")).replace(tzinfo=required_tz)
    //
        if isinstance(time_till, (int, float)):
            time_till = dt.datetime.fromtimestamp(time_till, tz=required_tz)
        elif isinstance(time_till, str):
            time_till = dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S").replace(tzinfo=required_tz)
        else:
            raise ValueError("Invalid time_till format. Use Unix timestamp (int/float) or string.")
        """
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
#hist_data = get_hist_data("USDCAD", "TIMEFRAME_H1")
#print(hist_data)

"""
def get_hist_data_numeric_index(mt5, symbol, timeframe, start_pos=0, num_candles=200):
    
    Parameters
    ----------
    symbol : TYPE str - e.g "USDCAD"
    timeframe : TYPE str - e.g. "TIMEFRAME_M15"
    start_pos : TYPE int -e.g. 0 means data till current time
    num_candles : TYPE int

    Returns
    -------
    historical data dataframe


    
    
    hist_data = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), start_pos, num_candles)   
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df

hist_data = get_hist_data_numeric_index("USDCAD", "TIMEFRAME_H1")
"""
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

def get_resistance(list_of_highs,current_price,level_range=20,pip=0.0001,min_occurance=2):
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


symbol = "AUDUSD"
# The code `backtest_timeframe` is likely a variable or function name in Python. Without seeing the
# actual implementation of `backtest_timeframe`, it is not possible to determine exactly what it is
# doing. It could be used to specify a timeframe for backtesting financial data or performing some
# other related task.
backtest_timeframe = "TIMEFRAME_M15"
supp_res_timeframe = "TIMEFRAME_H1"
candle_data = get_hist_data(symbol,backtest_timeframe,num_candles=70080,time_till=None)

candle_data[["macd","signal","histogram"]] = MACD(candle_data)

def find_support_res(symbol,timeframe,time_till=None,current_price=None,bar_nums=150):
    pip = get_pip(symbol)
    support_res = []
    
    if current_price == None:
        current_price = get_current_price(symbol)
        
    hist_data_df = get_hist_data(symbol,timeframe,num_candles=bar_nums,time_till=time_till)
    hist_data_df["hill_valley"] = get_hills_valleys(hist_data_df,pip)
    
    try:
        support_res.append(get_support(hist_data_df[hist_data_df["hill_valley"]=="valley"].low.to_list(),current_price,pip))
    except:
        support_res.append(current_price-80*pip) #default support level
    
    try:
        support_res.append(get_resistance(hist_data_df[hist_data_df["hill_valley"]=="hill"].high.to_list(),current_price,pip))
    except:
        support_res.append(current_price+80*pip) #default resistance level
        
    return support_res


signal = None
candle_data["returns"] = 0.0
trade_stats = []
macd_index = candle_data.columns.to_list().index("macd")
op_index = candle_data.columns.to_list().index("open")
cp_index = candle_data.columns.to_list().index("close")
hi_index = candle_data.columns.to_list().index("high")
lo_index = candle_data.columns.to_list().index("low")
returns_index = candle_data.columns.to_list().index("returns")
for i in range(8,len(candle_data)-1):
    if signal == None:
        if candle_data.iloc[i,macd_index]>0 and candle_data.iloc[i-1,macd_index]>0 and (candle_data.iloc[i-8:i-1,macd_index] < 0).all():
            signal = 'long'
            #[supp, res] = find_support_res(symbol,supp_res_timeframe,time_till=candle_data.index[i].strftime('%Y-%m-%d %H:%M:%S'),current_price=candle_data.iloc[i+1,op_index])
            # Ensure time_till is always a string
            if isinstance(candle_data.index[i], int):
                time_till1 = pd.to_datetime(candle_data.index[i], unit='s').strftime('%Y-%m-%d %H:%M:%S')
            else:
                time_till1 = candle_data.index[i].strftime('%Y-%m-%d %H:%M:%S')
            #print(f"time_till1 type: {type(time_till1)}, value: {time_till1}")
            [supp, res] = find_support_res(symbol,supp_res_timeframe,time_till=time_till1,current_price=candle_data.iloc[i+1,op_index])
            trade_stats.append({"time":candle_data.index[i],
                                "dir":"long",
                                "open_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]), #factor slippage
                                "close_price": None,
                                "sl_price":supp,
                                "tp_price":res})
            if trade_stats[-1]["open_price"] <= trade_stats[-1]["sl_price"]:
                trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"] - 80*get_pip(symbol)
            if trade_stats[-1]["open_price"] >= trade_stats[-1]["tp_price"]:
                trade_stats[-1]["tp_price"] = trade_stats[-1]["open_price"] + 80*get_pip(symbol)
            if (trade_stats[-1]["tp_price"] - trade_stats[-1]["open_price"]) < (trade_stats[-1]["open_price"]-trade_stats[-1]["sl_price"]):
                trade_stats[-1]["sl_price"] = (trade_stats[-1]["open_price"] - (trade_stats[-1]["tp_price"] - trade_stats[-1]["open_price"]))
                
        elif candle_data.iloc[i,macd_index]<0 and candle_data.iloc[i-1,macd_index]<0 and (candle_data.iloc[i-8:i-1,macd_index] > 0).all():
            signal = 'short'
            if isinstance(candle_data.index[i], int):
                time_till1 = pd.to_datetime(candle_data.index[i], unit='s').strftime('%Y-%m-%d %H:%M:%S')
            else:
                time_till1 = candle_data.index[i].strftime('%Y-%m-%d %H:%M:%S')
            [supp, res] = find_support_res(symbol,supp_res_timeframe,time_till=time_till1,current_price=candle_data.iloc[i+1,op_index])
            trade_stats.append({"time":candle_data.index[i],
                                "dir":"short",
                                "open_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]),
                                "close_price": None,
                                "sl_price":res,
                                "tp_price":supp})  
            if trade_stats[-1]["open_price"] >= trade_stats[-1]["sl_price"]:
                trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"] + 80*get_pip(symbol)
            if trade_stats[-1]["open_price"] <= trade_stats[-1]["tp_price"]:
                trade_stats[-1]["tp_price"] = trade_stats[-1]["open_price"] - 80*get_pip(symbol)
            if (trade_stats[-1]["open_price"] - trade_stats[-1]["tp_price"]) < (trade_stats[-1]["sl_price"]-trade_stats[-1]["open_price"]):
                trade_stats[-1]["sl_price"] = (trade_stats[-1]["open_price"] + (trade_stats[-1]["open_price"] - trade_stats[-1]["tp_price"] ))
    
    elif signal == "long":
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
        #else:
            #candle_data.iloc[i,returns_index] = (candle_data.iloc[i,cp_index] - candle_data.iloc[i,op_index])/get_pip(symbol)
            
    elif signal == "short":
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
        #else:
            #candle_data.iloc[i,returns_index] = (candle_data.iloc[i,op_index] - candle_data.iloc[i,cp_index])/get_pip(symbol)
            
if trade_stats and trade_stats[-1]["close_price"] == None:
    trade_stats[-1]["close_price"] = candle_data.iloc[-1,cp_index] 
    


"""
#print("Trade Stats:", trade_stats)  # Check if any trades exist
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

#print backtesting results
print()
print("cumulative return in pips = ",candle_data["returns"].cumsum()[-1])
print()
print("win rate of the strategy = {:.2f}%".format(win_rate(trade_stats)))
print()
print("average pip return per winning trade = {:.2f}".format(mean_ret_winner_pip(trade_stats, symbol)))
print()
print("average pip return per losing trade = {:.2f}".format(mean_ret_loser_pip(trade_stats, symbol)))
print()
print("maximum drawdown in pips = {:.2f}".format(max_drawdown(candle_data)))

#plot equity curve in terms of pip
candle_data["returns"].cumsum().plot()
plot.show()

