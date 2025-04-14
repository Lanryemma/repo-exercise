import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import datetime as dt
import pytz
import matplotlib.pyplot as plot
from pandas import Series
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
file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5 Python\\key.txt"
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

#give me the mt5 integration, the converted indicator with python and pandas library and the signal generation and make the code easier to understand

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THE CODE WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

# Fetch historical data from MT5
# Configuration
symbol = "EURUSD"
timeframe = "TIMEFRAME_M15"
data = get_hist_data(symbol, timeframe,35040, time_till=None )
# Configuration
print(f"\nData loaded: {len(data)} bars")
print("First 5 rows:")
print(data.head())
print(data.tail(10))


#________________________________________________________________________________________________________________________________

# Calculate Heikin Ashi candles
def calculate_heikin_ashi(df):
    ha = df.copy()
    
    # Heikin-Ashi Close
    ha['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    # Heikin-Ashi Open
    ha['ha_open'] = 0.0
    ha['ha_open'].iloc[0] = (df['open'].iloc[0] + df['close'].iloc[0]) / 2
    ha['ha_open'] = (ha['ha_open'].shift(1) + ha['ha_close'].shift(1)) / 2
    # Heikin-Ashi High/Low
    ha['ha_high'] = ha[['high', 'ha_open', 'ha_close']].max(axis=1)
    ha['ha_low'] = ha[['low', 'ha_open', 'ha_close']].min(axis=1)
    
    ha['color'] = np.where(ha['ha_close'] > ha['ha_open'], 'green', 'red')
    return ha[['ha_open', 'ha_close', 'color']]


ha_data = calculate_heikin_ashi(data)
data[['ha_open', 'ha_close', 'color']]= ha_data[['ha_open', 'ha_close', 'color']]
#print(data[['ha_open', 'ha_close', 'color']].tail(20))

# Calculate ATR-based indicator
def calculate_atr_trailing(DF, atr_period=10, multiplier=2.4):
    df = DF.copy()
    high, low, close = df['high'], df['low'], df['close']
    
    # Calculate True Range
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    df['tr'] = np.max([tr1, tr2, tr3], axis=0)
    
    # Calculate ATR
    df['atr'] = df['tr'].rolling(atr_period).mean()
    df['nLoss'] = multiplier * df['atr']
    
    # Initialize trailing stop array
    trailing_stop = np.zeros(len(df))
    
    for i in range(1, len(df)):
        if close.iloc[i] > trailing_stop[i-1] and close.iloc[i-1] > trailing_stop[i-1]:
            trailing_stop[i] = max(trailing_stop[i-1], close.iloc[i] - df['nLoss'].iloc[i])
        elif close.iloc[i] < trailing_stop[i-1] and close.iloc[i-1] < trailing_stop[i-1]:
            trailing_stop[i] = min(trailing_stop[i-1], close.iloc[i] + df['nLoss'].iloc[i])
        else:
            trailing_stop[i] = close.iloc[i] - df['nLoss'].iloc[i] if close.iloc[i] > trailing_stop[i-1] else close.iloc[i] + df['nLoss'].iloc[i]
    
    return trailing_stop


#_____________________________________________________________________________________________________________________________________________________________________

def calculate_zigzag(df, length=9):
    highs = df['high'].values
    lows = df['low'].values
    zigzag = np.zeros(len(df))
    
    for i in range(length, len(df)):
        if highs[i] == highs[i-length:i+1].max():
            zigzag[i] = 1  # Swing high
        elif lows[i] == lows[i-length:i+1].min():
            zigzag[i] = -1  # Swing low
    return pd.Series(zigzag, index=df.index)

def detect_msb(df, zigzag, fib_factor=0.273):
    swing_highs = []
    swing_lows = []
    msb_lines = []
    
    for i in range(1, len(df)):
        # Use RAW prices, not Heikin Ashi
        curr_high = df['high'].iloc[i]
        curr_low = df['low'].iloc[i]
        curr_close = df['close'].iloc[i]  # Actual close price
        
        if zigzag.iloc[i] == 1:
            swing_highs.append((df.index[i], curr_high))
        elif zigzag.iloc[i] == -1:
            swing_lows.append((df.index[i], curr_low))
        
        if len(swing_highs) > 1 and len(swing_lows) > 1:
            prev_high = swing_highs[-2][1]
            prev_low = swing_lows[-2][1]
            
            # Bullish MSB using actual price
            if curr_close > prev_high + (prev_high - prev_low) * fib_factor:
                msb_lines.append(('bullish', swing_highs[-2][0], prev_high))
                
            # Bearish MSB using actual price    
            if curr_close < prev_low - (prev_high - prev_low) * fib_factor:
                msb_lines.append(('bearish', swing_lows[-2][0], prev_low))
    
    return msb_lines

def generate_signals(DF, msb_lines):
    df = DF.copy()
    df['signal'] = 0.0
    
    # Convert index to timestamp for comparison
    df['timestamp'] = df.index.astype(np.int64) // 10**9
    
    for line in msb_lines:
        line_type, line_time, line_price = line
        line_timestamp = line_time.timestamp()
        
        # Vectorized comparison
        mask = (df['timestamp'] > line_timestamp)
        if line_type == 'bullish':
            df.loc[mask & (df['close'] > line_price), 'signal'] = 1
        else:
            df.loc[mask & (df['close'] < line_price), 'signal'] = -1
    
    return df.drop('timestamp', axis=1)
#________________________________________________________________________________________________________________________________________________
def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["ma_fast"] = EMA(df["close"],a)
    df["ma_slow"] = EMA(df["close"],b)
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signalm"] = EMA(df["macd"],c)
    df["histogram"] = df["macd"] - df["signalm"]
    return df[["macd","signalm","histogram"]]

def EMA(ser, n=9):
    ema = ser.ewm(n, adjust=False).mean()  # Built-in EMA calculation
    return ema

def calculate_stc(DF, fast=23, slow=50, cycle=10):
    """
    Schaff Trend Cycle implementation
    """
    df = DF.copy()
    
    # 1. Calculate MACD
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    
    # 2. Calculate Stochastics of MACD
    lowest_macd = macd.rolling(window=cycle).min()
    highest_macd = macd.rolling(window=cycle).max()
    stoch = 100 * (macd - lowest_macd) / (highest_macd - lowest_macd)
    
    # 3. Double Smooth with EMA
    stc = stoch.ewm(span=cycle, adjust=False).mean().ewm(span=cycle, adjust=False).mean()
    
    return stc

#_____________________________________________________________________________________________________________________________________________________
#STOPLOSS/ TAKE PROFIT AND TRAILING SL/TP
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
        

# Get price data
#______________________________________________________________________________________________________________________________________________________________

    
    # Calculate indicators
data[["macd","signalm","histogram"]] = MACD(data)
data['trailing_stop'] = calculate_atr_trailing(data)
data['ema1'] = data['close'].ewm(span=1).mean()
    
    # Generate signals
data['buy_signal'] = (data['close'] > data['trailing_stop']) & (data['ema1'] > data['trailing_stop'])
data['sell_signal'] = (data['close'] < data['trailing_stop']) & (data['ema1'] < data['trailing_stop'])

    # Calculate indicators
data['zigzag'] = calculate_zigzag(data)
#print(data['zigzag'].tail(20))
msb_lines = detect_msb(data, data['zigzag'])
    
# Generate signals
data = generate_signals(data, msb_lines)
#print( msb_lines)
data['volatility'] = calculate_volatility(data, 34, 2.4)
#print(data['volatility'].tail(20))
data['sar'] = parabolic_sar(data, step=0.02, max_step=0.2)
#print(data['sar'].tail(20))
# In your strategy implementation section, add:
data['stc'] = calculate_stc(data)


print("Sample signals check:")
print(data[['close', 'trailing_stop', 'signal', 'color']].tail(20))


#_________________________________________________________________________________________________________________________________________________________
# Main execution
#____________________________________________________________________________________________________________________________________________________________________
signal = None
data["returns"] = 0
trade_stats = []
hstgrm_index = data.columns.to_list().index("histogram")
signal_index = data.columns.to_list().index("signal")
buy_signal_index = data.columns.to_list().index('buy_signal')
sell_signal_index = data.columns.to_list().index('sell_signal')
ha_color = data.columns.to_list().index("color")
op_index = data.columns.to_list().index("open")
cp_index = data.columns.to_list().index("close")
hi_index = data.columns.to_list().index("high")
lo_index = data.columns.to_list().index("low")
stc_index = data.columns.get_loc('stc')
returns_index = data.columns.to_list().index("returns")

# Strategy Implementation
for i in range(len(data)-1):
    #  params = {
    #     'M1':   {'length': 98,  'mult': 2.8},
    #     'M5':   {'length': 72,  'mult': 2.6},
    #     'M15':  {'length': 54,  'mult': 2.4},
    #     'H1':   {'length': 34,  'mult': 2.2},
    #     'H4':   {'length': 21,  'mult': 2.0},
    #     'D1':   {'length': 13,  'mult': 1.8},
    #     'W1':   {'length': 8,   'mult': 1.6}
    # }
    
    
    
    if signal == None:
        if (data.iloc[i,hstgrm_index] > 0 and data.iloc[i-1,hstgrm_index] > 0  and data.iloc[i,buy_signal_index] == True and\
            data.iloc[i,signal_index] == 1  and data.iloc[i,ha_color] == 'green' and data.iloc[i-1,ha_color] == 'green' and\
                data.iloc[i,stc_index] > 10 and  data.iloc[i,stc_index] > data.iloc[i-1,stc_index]      # STC above 25 = bullish momentum
            ):
                
                atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                sl_pips = 1.5 * atr  # 1.5x ATR
                tp_pips = 3.0 * atr  # 3x ATR (2:1 reward:risk)
                signal = 'long'
                trade_stats.append({"time":data.index[i],
                                    "entry_bar": i,
                                    "dir":"long",
                                    "open_price":data.iloc[i+1,op_index] + 0.3*(data.iloc[i+1,hi_index] - data.iloc[i+1,op_index]), #factor slippage
                                    "close_price": None,
                                    #"sl_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]) - 10*get_pip(symbol),
                                    #"tp_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]) + 20*get_pip(symbol)
                                    "sl_price":data.iloc[i+1,op_index]  - sl_pips * get_pip(symbol),
                                    "tp_price":data.iloc[i+1,op_index]  + tp_pips * get_pip(symbol)})
    
        elif (data.iloc[i,hstgrm_index] < 0 and data.iloc[i-2,hstgrm_index] < 0  and data.iloc[i,sell_signal_index] == True    and\
            data.iloc[i,signal_index] == -1  and data.iloc[i,ha_color] == 'red' and data.iloc[i-1,ha_color] == 'red' and\
                data.iloc[i,stc_index] < 90 and  data.iloc[i,stc_index] < data.iloc[i-1,stc_index]      # STC below 75 = bullish momentum
                ):
                atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                sl_pips = 1.5 * atr  # 1.5x ATR
                tp_pips = 3.0 * atr  # 3x ATR (2:1 reward:risk)
                signal = 'short'
                trade_stats.append({"time":data.index[i],
                                    "entry_bar": i,
                                    "dir":"short",
                                    "open_price":data.iloc[i+1,op_index] - 0.3*(data.iloc[i+1,op_index] - data.iloc[i+1,lo_index]), #factor slippage
                                    "close_price": None,
                                    #"sl_price":data[0].iloc[i+1,op_index] - 0.3*(data[0].iloc[i+1,op_index] - data[0].iloc[i+1,lo_index]) + 10*get_pip(symbol),
                                    #"tp_price":data[0].iloc[i+1,op_index] - 0.3*(data[0].iloc[i+1,op_index] - data[0].iloc[i+1,lo_index]) - 20*get_pip(symbol)
                                    "sl_price":data.iloc[i+1,op_index]  + sl_pips * get_pip(symbol),
                                    "tp_price":data.iloc[i+1,op_index]  - tp_pips * get_pip(symbol)})                 
                        
    elif signal == "long":
        current_sar = data.iloc[i]['sar']
        max_hold_bars = 12 * 6  # 4 hours for M15
    # Update SL to SAR if it's tighter
        #check if the MACD based signal reversed which would imply exiting position even though SL may not have reached
        #candle_data.iloc[i,-1] = (trade_stats[-1]["close_price"] - candle_data.iloc[i,op_index])/get_pip(symbol)
        if data.iloc[i,hi_index] > trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif data.iloc[i,lo_index] < trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif current_sar > trade_stats[-1]["sl_price"]:
            trade_stats[-1]["sl_price"] = current_sar
        elif (i - trade_stats[-1]["entry_bar"]) >= max_hold_bars:
            signal = None
            trade_stats[-1]["close_price"] =  data.iloc[i,cp_index ] 
            data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
            
            
    elif signal == "short":
        current_sar = data.iloc[i]['sar']
        max_hold_bars = 12 * 6  # 4 hours for M15
        #candle_data.iloc[i,-1] = (candle_data.iloc[i,op_index] - trade_stats[-1]["close_price"])/get_pip(symbol) 
        if data.iloc[i,lo_index] < trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        elif data.iloc[i,hi_index] > trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        elif current_sar > trade_stats[-1]["sl_price"]:
            trade_stats[-1]["sl_price"] = current_sar
        elif (i - trade_stats[-1]["entry_bar"]) >= max_hold_bars:
            signal = None
            trade_stats[-1]["close_price"] =  data.iloc[i,cp_index ] 
            data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
    # # if symbol == "USDSEK": 
    #     candle_data.iloc[i,-1] = candle_data.iloc[i,-1]/5 #adjust for pos size of USDSEK            
if trade_stats and trade_stats[-1]["close_price"] == None:
    trade_stats[-1]["close_price"] = data.iloc[-1,cp_index] #update the cp of last trade as the current price


#print backtesting results
print("cumulative return in pips = ",data["returns"].cumsum().iloc[-1])
print("win rate of the strategy = {:.2f}%".format(win_rate(trade_stats)))
print("average pip return per winning trade = {:.2f}".format(mean_ret_winner_pip(trade_stats, symbol)))
print("average pip return per losing trade = {:.2f}".format(mean_ret_loser_pip(trade_stats, symbol)))
print("maximum drawdown in pips = {:.2f}".format(max_drawdown(data)))
#monthly_performance(returns_df)

print("Number of trades taken:", len(trade_stats))

#plot equity curve in terms of pip
data["returns"].cumsum().plot()
plot.show()


#     # Display results
# print("\nLast 5 signals:")
# print(data[['open', 'high', 'low', 'close', 'signal']].tail())
# # Display signals
# print("\nLast 5 signals:")
# print(data[['close', 'trailing_stop', 'ema1', 'buy_signal', 'sell_signal']].tail())

mt5.shutdown()
