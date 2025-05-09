import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import datetime as dt
import pytz
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
#file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5 Python\\keyfusionmarket.txt"
file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5_Python\\key.txt"
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

def RMA(series, period):
    #  Calculate the Relative Moving Average (RMA) using Pandas.
    return series.ewm(alpha=1/period, adjust=False).mean()

def RSI(DF, n=5):
    "function to calculate RSI"
    df = DF.copy()
    df["change"] = df["close"] - df["close"].shift(1)
    df["gain"] = np.where(df["change"]>=0, df["change"], 0)
    df["loss"] = np.where(df["change"]<0, -1*df["change"], 0)
    df["avgGain"] = RMA(df["gain"],n)
    df["avgLoss"] = RMA(df["loss"],n)
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["rsi"] = 100 - (100/ (1 + df["rs"]))
    return df["rsi"]

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


def calculate_volatility(DF, length, mult):
            df = DF.copy()
            # Calculate True Range
            df['tr1'] = df['high'] - df['low']
            df['tr2'] = abs(df['high'] - df['close'].shift())
            df['tr3'] = abs(df['low'] - df['close'].shift())
            df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
            
            # Calculate ATR
            df['atr'] = df['tr'].ewm(span=length, adjust=False).mean()
            
            # Calculate volatility bands
            return df['atr'] * mult

def parabolic_sar(df, step=0.02, max_step=0.2):#(df, step=0.035, max_step=0.28)
        df = df.copy()
        high = df['high'].values
        low = df['low'].values
        sar = np.full(len(df), np.nan)
        trend = 1  # 1 = bullish, -1 = bearish
        ep = low[0] if trend == 1 else high[0]  # Extreme Point
        af = step  # Acceleration Factor
            
        # Initial SAR (first value)
        sar[0] = low[0] if trend == 1 else high[0]
            
        for i in range(1, len(df)):
            # Calculate SAR for current period
            sar[i] = sar[i-1] + af * (ep - sar[i-1])
                
            # Check for trend reversal
            if trend == 1:
                if low[i] < sar[i]:  # Bearish reversal
                    trend = -1
                    sar[i] = high[i]
                    ep = high[i]
                    af = step
                else:  # Continue bullish
                    if high[i] > ep:
                        ep = high[i]
                        af = min(af + step, max_step)
                    # SAR cannot be above prior 2 lows
                    sar[i] = min(sar[i], low[i-1], low[max(0, i-2)])
            else:
                if high[i] > sar[i]:  # Bullish reversal
                    trend = 1
                    sar[i] = low[i]
                    ep = low[i]
                    af = step
                else:  # Continue bearish
                    if low[i] < ep:
                        ep = low[i]
                        af = min(af + step, max_step)
                    # SAR cannot be below prior 2 highs
                    sar[i] = max(sar[i], high[i-1], high[max(0, i-2)])
    
            df['sar'] = sar
        return df['sar']
        

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THE CODE WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

symbol = "GBPUSD"
backtest_timeframe = "TIMEFRAME_M5"
candle_data = get_hist_data(symbol,backtest_timeframe,num_candles=99040,time_till=None)

#add technical indicators
candle_data["sma"] = SMA(candle_data)       
candle_data["rsi"] = RSI(candle_data)
candle_data['volatility'] = calculate_volatility(candle_data, 38, 2.4)
#print(data['volatility'].tail(20))
candle_data['sar'] = parabolic_sar(candle_data, step=0.01, max_step=0.2)
candle_data.dropna(inplace=True)

signal = None
candle_data["returns"] = 0
trade_stats = []
sma_index = candle_data.columns.to_list().index("sma")
rsi_index = candle_data.columns.to_list().index("rsi")
op_index = candle_data.columns.to_list().index("open")
cp_index = candle_data.columns.to_list().index("close")
hi_index = candle_data.columns.to_list().index("high")
lo_index = candle_data.columns.to_list().index("low")
returns_index = candle_data.columns.to_list().index("returns")

for i in range(3,len(candle_data)-1):
    if signal == None:
        if (#candle_data.iloc[i,cp_index] > candle_data.iloc[i,sma_index] and \
        candle_data.iloc[i,rsi_index] > 10 and \
        candle_data.iloc[i-1,rsi_index] > 10 and \
        candle_data.iloc[i-2,rsi_index] < 10): #and \
        #candle_data.iloc[i-3,rsi_index] < 10):
        #    candle_data.iloc[i,rsi_index] >  candle_data.iloc[i-1,rsi_index] and \
        #    candle_data.iloc[i-1,rsi_index] < candle_data.iloc[i-2,rsi_index] and \
        #    candle_data.iloc[i-2,rsi_index] < candle_data.iloc[i-3,rsi_index] and \
        
                atr = candle_data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                sl_pips = 1.1 * atr  # 1.5x ATR
                tp_pips = 2.2 * atr  # 3x ATR (2:1 reward:risk)
                signal = 'long'
                trade_stats.append({"time":candle_data.index[i],
                                    "entry_bar": i,
                                    "dir":"long",
                                    "open_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]), #factor slippage
                                    "close_price": None,
                                    "sl_price":candle_data.iloc[i+1,op_index]  - sl_pips * get_pip(symbol),
                                    "tp_price":candle_data.iloc[i+1,op_index]  + tp_pips * get_pip(symbol)
                                    # "sl_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]) - 31*get_pip(symbol),
                                    # "tp_price":candle_data.iloc[i+1,op_index] + 0.3*(candle_data.iloc[i+1,hi_index] - candle_data.iloc[i+1,op_index]) + 60*get_pip(symbol)
                                    })
    
        elif (#candle_data.iloc[i,cp_index] < candle_data.iloc[i,sma_index] and \
                candle_data.iloc[i,rsi_index] < 90 and \
                candle_data.iloc[i-1,rsi_index] < 90 and \
                candle_data.iloc[i-2,rsi_index] > 90): #and \
                #candle_data.iloc[i-3,rsi_index] > 90):
            # candle_data.iloc[i,rsi_index] > candle_data.iloc[i-1,rsi_index] and \
            # candle_data.iloc[i-1,rsi_index] > candle_data.iloc[i-2,rsi_index] and \
            # candle_data.iloc[i-2,rsi_index] > candle_data.iloc[i-3,rsi_index] and \
            # candle_data.iloc[i-3,rsi_index] > 40:
                atr = candle_data.iloc[i]['volatility'] / get_pip(symbol)
                sl_pips = 1.1 * atr  # 1.5x ATR
                tp_pips = 2.2 * atr  # 3x ATR (2:1 reward:risk)
                signal = 'short'
                trade_stats.append({"time":candle_data.index[i],
                                    "entry_bar": i,
                                    "dir":"short",
                                    "open_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]), #factor slippage
                                    "close_price": None,
                                    # "sl_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]) + 31*get_pip(symbol),
                                    # "tp_price":candle_data.iloc[i+1,op_index] - 0.3*(candle_data.iloc[i+1,op_index] - candle_data.iloc[i+1,lo_index]) - 60*get_pip(symbol)
                                    "sl_price":candle_data.iloc[i+1,op_index]  + sl_pips * get_pip(symbol),
                                    "tp_price":candle_data.iloc[i+1,op_index]  - tp_pips * get_pip(symbol)})                 
                        
    elif signal == "long":
        current_sar = candle_data.iloc[i]['sar']
        max_hold_bars = 96*3#12 * 6  # 4 hours for M15
        #check if the MACD based signal reversed which would imply exiting position even though SL may not have reached
        if candle_data.iloc[i,hi_index] > trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif candle_data.iloc[i,lo_index] < trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif candle_data.iloc[i,rsi_index] > 90: 
            signal = None
            trade_stats[-1]["close_price"] =   candle_data.iloc[i+1,op_index]
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif current_sar > trade_stats[-1]["sl_price"]:
            trade_stats[-1]["sl_price"] = current_sar
        # elif candle_data.iloc[i,hi_index] > (trade_stats[-1]["open_price"] + 45*get_pip(symbol)):
        #     trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"]
        elif (i - trade_stats[-1]["entry_bar"]) >= max_hold_bars:
                signal = None
                trade_stats[-1]["close_price"] =  candle_data.iloc[i,cp_index ] 
                candle_data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
            
            
    elif signal == "short":
        current_sar = candle_data.iloc[i]['sar']
        max_hold_bars = 96*3#12 * 6  # 4 hours for M15
            
        if candle_data.iloc[i,lo_index] < trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        elif candle_data.iloc[i,hi_index] > trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        # elif candle_data.iloc[i,lo_index] < (trade_stats[-1]["open_price"] - 45*get_pip(symbol)):
        #     trade_stats[-1]["sl_price"] = trade_stats[-1]["open_price"]
        elif candle_data.iloc[i,rsi_index] < 10: 
            signal = None
            trade_stats[-1]["close_price"] =   candle_data.iloc[i+1,op_index]
            candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        elif current_sar > trade_stats[-1]["sl_price"]:
            trade_stats[-1]["sl_price"] = current_sar
        elif (i - trade_stats[-1]["entry_bar"]) >= max_hold_bars:
                signal = None
                trade_stats[-1]["close_price"] =  candle_data.iloc[i,cp_index ] 
                candle_data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
    # if symbol == "USDSEK": 
    #     candle_data.iloc[i,-1] = candle_data.iloc[i,-1]/5 #adjust for pos size of USDSEK            
if trade_stats and trade_stats[-1]["close_price"] == None:
    trade_stats[-1]["close_price"] = candle_data.iloc[-1,cp_index] #update the cp of last trade as the current price


#print backtesting results
print("cumulative return in pips = ",candle_data["returns"].cumsum()[-1])
print("win rate of the strategy = {:.2f}%".format(win_rate(trade_stats)))
print("average pip return per winning trade = {:.2f}".format(mean_ret_winner_pip(trade_stats, symbol)))
print("average pip return per losing trade = {:.2f}".format(mean_ret_loser_pip(trade_stats, symbol)))
print("maximum drawdown in pips = {:.2f}".format(max_drawdown(candle_data)))
#monthly_performance(returns_df)

print("Number of trades taken:", len(trade_stats))

#plot equity curve in terms of pip
candle_data["returns"].cumsum().plot()
plot.show()