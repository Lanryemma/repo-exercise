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
file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5_Python\\key.txt"
#file_path = r"C:\Users\user\Documents\LANRE\Desktop\FRONTEND\Mt5 Python\key.txt"
key = open(file_path,"r").read().split()
path1 = "C:\\Users\\user\\AppData\\Roaming\\MetaTrader 5\\terminal64.exe"#For the executable path when we run the code

#since we are importing the user id we must convert it to an integer int(key[0])
if not mt5.initialize(path = path1, login= int(key[0]),password=key[1], server=key[2]):
    #print("initialize() failed, error code =",mt5.last_error())
    print("connection not established")
else:
    print("connection established")



# Configuration
RSI_PERIOD = 21
MA_PERIOD = 21
MA_TYPE = 'EMA'
OB_LEVEL = 70
OS_LEVEL = 30
MOMENTUM_THRESHOLD = 50

def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  

def calculate_rsi(data, period):
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Wilder's RMA calculation
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi



def calculate_ma(data, period, ma_type):
    """Calculate moving average"""
    if ma_type == 'SMA':
        return data.rolling(period).mean()
    elif ma_type == 'EMA':
        return data.ewm(span=period, adjust=False).mean()
    elif ma_type == 'RMA':
        return data.ewm(alpha=1/period, adjust=False).mean()
    return data  # Fallback to original data
"""
def detect_divergence(high, low, rsi, lookback=14):
    #Detect regular and hidden divergences
    signals = pd.DataFrame(index=rsi.index)
    
    # Find pivot points
    highs = high.rolling(lookback, center=True).max()
    lows = low.rolling(lookback, center=True).min()
    
    # Regular Bullish Divergence
    regular_bullish = (low.shift(2) < lows) & (rsi.shift(2) > rsi)
    # Regular Bearish Divergence
    regular_bearish = (high.shift(2) > highs) & (rsi.shift(2) < rsi)
    
    # Hidden Bullish Divergence
    hidden_bullish = (low.shift(2) > lows) & (rsi.shift(2) < rsi)
    # Hidden Bearish Divergence
    hidden_bearish = (high.shift(2) < highs) & (rsi.shift(2) > rsi)
    
    signals['regular_bullish'] = regular_bullish
    signals['regular_bearish'] = regular_bearish
    signals['hidden_bullish'] = hidden_bullish
    signals['hidden_bearish'] = hidden_bearish
    
    return signals
"""
def detect_divergence(high, low, rsi, lookback_left=14, lookback_right=1):
    signals = pd.DataFrame(index=rsi.index)
    
    # 1. Pivot Detection with Proper Lookback
    def find_pivots(series, is_high=True):
        pivots = pd.Series(False, index=series.index)
        for i in range(lookback_left, len(series)-lookback_right):
            window = series.iloc[i-lookback_left:i+lookback_right+1]
            if is_high:
                pivots.iloc[i] = window.idxmax() == series.index[i]
            else:
                pivots.iloc[i] = window.idxmin() == series.index[i]
        return pivots

    # Find pivot points
    high_pivots = find_pivots(high, is_high=True)
    low_pivots = find_pivots(low, is_high=False)

    # 2. Regular Divergence
    regular_bullish = (
        low_pivots & 
        (low.shift(lookback_left) > low) &  # Lower low
        (rsi.shift(lookback_left) < rsi) )   # Higher RSI

    regular_bearish = (
        high_pivots & 
        (high.shift(lookback_left) < high) &  # Higher high
        (rsi.shift(lookback_left) > rsi)   )   # Lower RSI

    # 3. Hidden Divergence
    hidden_bullish = (
        low_pivots & 
        (low.shift(lookback_left) < low) &  # Higher low
        (rsi.shift(lookback_left) > rsi))    # Lower RSI

    hidden_bearish = (
        high_pivots & 
        (high.shift(lookback_left) > high) &  # Lower high
        (rsi.shift(lookback_left) < rsi) )     # Higher RSI

    # 4. Assign Signals
    signals['regular_bullish'] = regular_bullish
    signals['regular_bearish'] = regular_bearish
    signals['hidden_bullish'] = hidden_bullish
    signals['hidden_bearish'] = hidden_bearish

    return signals
"""
def detect_sweep(rsi, price, momentum_threshold):
    #Detect RSI sweep signals
    signals = pd.DataFrame(index=rsi.index)
    
    # Bullish sweep conditions
    bullish_crossover = (rsi.shift(1) < momentum_threshold) & (rsi > momentum_threshold)
    bearish_crossunder = (rsi.shift(1) > momentum_threshold) & (rsi < momentum_threshold)
    
    signals['bullish_sweep'] = bullish_crossover
    signals['bearish_sweep'] = bearish_crossunder
    
    return signals
"""
def detect_sweep(rsi, price, momentum_threshold):
    """Detect RSI sweep with liquidity checks"""
    signals = pd.DataFrame(index=rsi.index)
    
    # 1. Identify liquidity pools
    liquidity_zones = price.rolling(20).agg(['min', 'max'])
    
    # 2. RSI sweep conditions
    bullish = (
        (rsi.shift(1) < momentum_threshold) &
        (rsi > momentum_threshold) &
        (price <= liquidity_zones['min'].shift(1))  # Swept previous low
    )
    
    bearish = (
        (rsi.shift(1) > momentum_threshold) &
        (rsi < momentum_threshold) &
        (price >= liquidity_zones['max'].shift(1))  # Swept previous high
    )
    
    signals['bullish_sweep'] = bullish
    signals['bearish_sweep'] = bearish
    
    return signals

def generate_signals(data):
    """Generate trading signals"""
    # Calculate indicators
    data['rsi'] = calculate_rsi(data, RSI_PERIOD)
    data['ma'] = calculate_ma(data['rsi'], MA_PERIOD, MA_TYPE)
    
    # Detect patterns
    divergence_signals = detect_divergence(data['high'], data['low'], data['rsi'])
    sweep_signals = detect_sweep(data['rsi'], data['close'], MOMENTUM_THRESHOLD)
    
    # Combine signals
    signals = pd.concat([divergence_signals, sweep_signals], axis=1)
    
    # Generate final signals
    signals['buy'] = signals['regular_bullish'] | signals['hidden_bullish'] | signals['bullish_sweep']
    signals['sell'] = signals['regular_bearish'] | signals['hidden_bearish'] | signals['bearish_sweep']
    
    signals['strong_buy'] = (
    signals['regular_bullish'] &
    (data['rsi'] - data['rsi'].shift(5) > 3) &  # Per-bar comparison
    (data['low'] == data['low'].rolling(5).min()))  # Per-bar min check
    # # RSI increased by 5 points
    # # Price decreased

    signals['strong_sell'] = (
    signals['regular_bearish'] &
    (data['rsi'].shift(5) - data['rsi'] > 3) &  # 3+ points decrease over 5 bars
    (data['high'] == data['high'].rolling(5, min_periods=1).max()))  # Current high is 5-bar maximum
    return signals

# MT5 Integration
"""
def get_hist_data_numeric_index(symbol, timeframe, start_pos=0, num_candles=35040):
    
    # Parameters
    # ----------
    # symbol : TYPE str - e.g "USDCAD"
    # timeframe : TYPE str - e.g. "TIMEFRAME_M15"
    # start_pos : TYPE int -e.g. 0 means data till current time
    # num_candles : TYPE int
    # Returns
    # -------
    # historical data dataframe
    
    hist_data = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), start_pos, num_candles)   
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df
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


# Example usage
if __name__ == "__main__":
    # Get data from MT5
    symbol = "AUDUSD"
    timeframe = "TIMEFRAME_M15"
    data = get_hist_data(symbol, timeframe,num_candles=35040,time_till=None)
    data = data.dropna().copy()
    
    if data is not None:
        # Generate signals
        signals = generate_signals(data)
        data['volatility'] = calculate_volatility(data, 34, 2.4)
        #print(data['volatility'].tail(20))
        data['sar'] = parabolic_sar(data, step=0.02, max_step=0.2)
        
        # Get latest signal
        latest_signal = signals.iloc[-1]
        
        print("\nLatest Trading Signals:")
        print(f"Buy Signal: {latest_signal['buy']}")
        print(f"Sell Signal: {latest_signal['sell']}")
        print(f"RSI Value: {data['rsi'].iloc[-1]:.2f}")
        
        # Trading logic example
        if latest_signal['buy']:
            print("\nBullish Signal Detected!")
            # Add MT5 order execution logic here
            
        elif latest_signal['sell']:
            print("\nBearish Signal Detected!")
            # Add MT5 order execution logic here


    signal = None
    data["returns"] = 0.0
    trade_stats = []
    op_index = data.columns.to_list().index("open")
    cp_index = data.columns.to_list().index("close")
    hi_index = data.columns.to_list().index("high")
    lo_index = data.columns.to_list().index("low")
    returns_index = data.columns.to_list().index("returns")
    
    for i in range(len(data)-1):
        
        if signal == None:
            if (signals.iloc[i]['buy'] #signals.iloc[i]['buy']      # STC above 25 = bullish momentum
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
        
            elif (signals.iloc[i]['sell'] #signals.iloc[i]['sell']     # STC below 75 = bullish momentum
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
