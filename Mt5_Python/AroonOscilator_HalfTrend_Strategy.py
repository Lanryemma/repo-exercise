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
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s").dt.tz_localize('UTC')
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THE CODE WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

# Calculate technical components
def calculate_heikin_ashi(df):
    ha = df.copy()
    
    # Initialize columns
    ha['ha_close'] = (ha['open'] + ha['high'] + ha['low'] + ha['close']) / 4
    ha['ha_open'] = (ha['open'].shift(1) + ha['close'].shift(1)) / 2
    ha['ha_high'] = ha[['high', 'ha_open', 'ha_close']].max(axis=1)
    ha['ha_low'] = ha[['low', 'ha_open', 'ha_close']].min(axis=1)
    
    ha['color'] = np.where(ha['ha_close'] > ha['ha_open'], 'green', 'red')
    return ha[['ha_open', 'ha_close', 'color','ha_high','ha_low']]

# 4. HALF TREND CALCULATION ==========================================================================
def calculate_half_trend(df, period=5):
    """Vectorized Half Trend calculation"""
    ht_df = df.copy()
    close = ht_df['ha_close'].values
    high = ht_df['ha_high'].values
    low = ht_df['ha_low'].values
    
    # Precompute rolling values
    rolling_max = pd.Series(high).rolling(period, min_periods=1).max().values
    rolling_min = pd.Series(low).rolling(period, min_periods=1).min().values
    close_ma = pd.Series(close).rolling(period, min_periods=1).mean().values
    
    # Initialize arrays
    hl_t = np.zeros_like(close)
    signal = np.zeros_like(close)
    
    # Vectorized conditional logic
    cond1 = (close_ma < np.roll(hl_t, 1)) & (rolling_max < np.roll(hl_t, 1))
    cond2 = (close_ma > np.roll(hl_t, 1)) & (rolling_min > np.roll(hl_t, 1))
    
    hl_t = np.select(
        [cond1, cond2],
        [rolling_max, rolling_min],
        default=np.roll(hl_t, 1)
    )
    # Generate signals
    signal = np.where(hl_t > np.roll(hl_t, 1), 1, 
            np.where(hl_t < np.roll(hl_t, 1), -1, 0))
    
    # Handle initial period
    hl_t[:period] = close[:period]
    signal[:period] = 0
    
    # Assign to DataFrame
    ht_df['half_trend'] = hl_t
    ht_df['signal1'] = signal
    return ht_df

# 3. AROON CALCULATIONS ================================================================================================
def calculate_aroon(DF, length=14):
    df = DF.copy()
    
    # Calculate periods since highest high/lowest low
    df['high_idx'] = df['high'].rolling(length).apply(np.argmax, raw=True)
    df['low_idx'] = df['low'].rolling(length).apply(np.argmin, raw=True)
    
    # Calculate Aroon values
    df['aroon_up'] = ((length - (length - 1 - df['high_idx'])) / length) * 100
    df['aroon_down'] = ((length - (length - 1 - df['low_idx'])) / length) * 100
    
    # Calculate oscillator
    df['aroon_osc'] = df['aroon_up'] - df['aroon_down']
    
    return df.drop(['high_idx', 'low_idx'], axis=1)

# 4. SIGNAL GENERATION =================================================================================================
def generate_signals(df):
    df['signal2'] = 0
    df['signal2'] = np.where(df['aroon_osc'] > 0, 1, -1)
    return df

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
        

# MODIFY SESSION DETECTION:
def is_session_active(timestamp, session):
    """Check session status in Lagos time context"""
    lagos_hour = timestamp.hour  # Already in Lagos time
    
    # Session hours in LAGOS TIME (GMT+1)
    session_hours = {
        "London": (8, 17),    # 7AM-4PM UTC → 8AM-5PM Lagos
        "New_York": (13, 22), # 12PM-9PM UTC → 1PM-10PM Lagos
        "Sydney": (23, 8),    # 10PM-7AM UTC → 11PM-8AM Lagos
        "Tokyo": (1, 10)      # 12AM-9AM UTC → 1AM-10AM Lagos
    }[session]

    start, end = session_hours
    if start <= end:
        return start <= lagos_hour < end
    else:
        return lagos_hour >= start or lagos_hour < end

# Example usage
if __name__ == "__main__":
    # Load your price data (example with random data)
    symbol = "AUDUSD"
    timeframe = "TIMEFRAME_M15"
    num_candles = 35040
    data =  get_hist_data(symbol, timeframe,num_candles, time_till=None )
    result1 = calculate_heikin_ashi(data)# for 1
    data = data.dropna().copy()
    
    # Calculate indicator
    result2 = calculate_half_trend(result1, period=25)
    result3 = calculate_aroon(data, length=35)
    result4 = generate_signals(result3)
    data['volatility'] = calculate_volatility(data, 34, 2.4)
        #print(data['volatility'].tail(20))
    data['sar'] = parabolic_sar(data, step=0.04, max_step=0.3)
    # 1. Convert to proper timezone-aware index
    data = data.tz_convert('Africa/Lagos') 
    # 2. Add session flags directly (no separate function needed)
    data['london_active'] = data.index.map(lambda x: is_session_active(x, "London"))
    data['newyork_active'] = data.index.map(lambda x: is_session_active(x, "New_York"))
    data['sydney_active'] = data.index.map(lambda x: is_session_active(x, "Sydney"))
    data['Tokyo_active'] = data.index.map(lambda x: is_session_active(x, "Tokyo"))
    data['signal1'] = result2['signal1']
    data['signal2'] = result4['signal2']
    # data['bear_signal'] = result2['bear_signal']
    # data['bear_signal+'] = result2['bear_signal+']
    # data['sell_signal2'] = data2['sell_signal2']
    # data['buy_signal3'] = data3['buy_signal3']
    
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
            if ((data.iloc[i]['signal1']==1)  &  ((data.iloc[i]['signal2']==1) | (data.iloc[i]['signal2']==0) ) #& (data.iloc[i]['sydney_active'] | data.iloc[i]['newyork_active']) 
                #data.iloc[i]['buy_signal3'] and data.iloc[i]['color']=="green" #signals.iloc[i]['buy']      # STC above 25 = bullish momentum
                ):
                    
                    atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                    sl_pips = 1.5 * atr  # 1.5x ATR
                    tp_pips = 3.0 * atr  # 3x ATR (2:1 reward:risk)
                    # atr = data.iloc[i]['volatility'] / get_pip(symbol)
                    # volatility_ratio = atr / data['volatility'].mean()  # Relative volatility
                    # # Scale ratios inversely with volatility
                    # sl_pips = 1.2 * atr * (1 + (1/volatility_ratio))
                    # tp_pips = 2.4 * atr * (1 + volatility_ratio)
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
        
            elif ((data.iloc[i]['signal1']==-1)  &  ((data.iloc[i]['signal2']==-1) | (data.iloc[i]['signal2']==0) )#(data.iloc[i]['signal2']==-1) #& (data.iloc[i]['sydney_active'] | data.iloc[i]['newyork_active'])
                #data.iloc[i]['sell_signal3'] and data.iloc[i]['color']=="red"  #signals.iloc[i]['sell']     # STC below 75 = bullish momentum
                    ):
                    atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                    sl_pips = 1.5 * atr  # 1.5x ATR
                    tp_pips = 3.0 * atr  # 3x ATR (2:1 reward:risk)
                    # atr = data.iloc[i]['volatility'] / get_pip(symbol)
                    # volatility_ratio = atr / data['volatility'].mean()  # Relative volatility
                    # # Scale ratios inversely with volatility
                    # sl_pips = 1.2 * atr * (1 + (1/volatility_ratio))
                    # tp_pips = 2.4 * atr * (1 + volatility_ratio)
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
            max_hold_bars = 96 #12 * 6  # 4 hours for M15
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
            max_hold_bars = 96#12 * 6  # 4 hours for M15
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
