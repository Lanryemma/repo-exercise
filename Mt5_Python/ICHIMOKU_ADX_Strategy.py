import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import datetime as dt
import pytz
import matplotlib.pyplot as plot
from pandas import Series
#from Stratergy_evaluation import win_rate,mean_ret_winner_pip,mean_ret_loser_pip,max_drawdown


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
#file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5_Python\\key.txt"
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

def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  

def calculate_donchian(data, period):
    """Calculate Donchian Channel midpoint"""
    return (
        data['high'].rolling(period).max() + 
        data['low'].rolling(period).min()
    ) / 2

def ichimoku_signals(DF, conversion_period=20, base_period=60):
    """Calculate Ichimoku components and generate trading signals"""
    df = DF.copy()
    
    # Calculate components
    df['Conversion'] = calculate_donchian(df, conversion_period)
    df['Base'] = calculate_donchian(df, base_period)
    
    # Generate signals (1 = buy, -1 = sell)
    df['signal1'] = np.where(
        df['Conversion'] > df['Base'], 1, -1
    )
    
    return df

# ======================
# INDICATOR CALCULATION
# ======================
def calculate_adx_histogram(df, period=14):
    """
    Calculate ADX with colored histogram signals
    Returns DataFrame with '+DI', '-DI', 'ADX', and 'Signal' columns
    """
    data = df.copy()
    
    # Calculate True Range
    prev_close = data['close'].shift(1)
    data['TR'] = np.maximum.reduce([
        data['high'] - data['low'],
        abs(data['high'] - prev_close),
        abs(data['low'] - prev_close)
    ])
    
    # Calculate Directional Movements
    up_move = data['high'] - data['high'].shift(1)
    down_move = data['low'].shift(1) - data['low']
    data['+DM'] = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    data['-DM'] = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # Smooth values using Wilder's method
    data['TR_smooth'] = data['TR'].rolling(period).sum()
    data['+DM_smooth'] = data['+DM'].rolling(period).sum()
    data['-DM_smooth'] = data['-DM'].rolling(period).sum()
    
    # Calculate DI values
    data['+DI'] = (data['+DM_smooth'] / data['TR_smooth']) * 100
    data['-DI'] = (data['-DM_smooth'] / data['TR_smooth']) * 100
    
    # Calculate ADX
    dx = (abs(data['+DI'] - data['-DI']) / (data['+DI'] + data['-DI'])) * 100
    data['ADX'] = dx.rolling(period).mean()
    
    # Generate signals (1 = buy, -1 = sell)
    data['signal2'] = 0
    buy_condition = (data['ADX'] > data['-DI']) & (data['+DI'] > data['-DI']) & (data['ADX'] > data['ADX'].shift(1))
    sell_condition = (data['ADX'] > data['+DI']) & (data['-DI'] > data['+DI']) & (data['ADX'] > data['ADX'].shift(1))
    
    data.loc[buy_condition, 'signal2'] = 1
    data.loc[sell_condition, 'signal2'] = -1
    
    return data[['+DI', '-DI', 'ADX', 'signal2']]

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
        

def calculate_adaptive_sl_tp(df, symbol, risk_reward_ratio=2):
    """Improved volatility-adjusted SL/TP with dynamic risk management"""
    df['atr_pips'] = df['volatility'] / get_pip(symbol)
    
    # Dynamic multiplier based on recent volatility
    vol_ratio = df['atr_pips'].rolling(50).mean() / df['atr_pips']
    sl_mult = np.clip(1.5 * vol_ratio, 1.0, 2.5)
    tp_mult = sl_mult * risk_reward_ratio
    
    df['sl_pips'] = df['atr_pips'] * sl_mult
    df['tp_pips'] = df['atr_pips'] * tp_mult
    return df

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
        

# Add these near your other utility functions
def get_pip_value1(symbol, lot_size=100000):
    """Calculate the value of 1 pip in USD for a given symbol"""
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise ValueError(f"Symbol {symbol} not found")
    contract_size = symbol_info.trade_contract_size  # Critical for non-forex
    point = symbol_info.point
    pip_size = symbol_info.pip_size if hasattr(symbol_info, 'pip_size') else 10 * point#10 * point
    quote_currency = symbol[3:]
    
    pip_value_quote = pip_size * contract_size #lot_size
    
    if quote_currency == "USD":
        return pip_value_quote
    
    conversion_symbol = f"{quote_currency}USD"
    conversion_symbol_info = mt5.symbol_info(conversion_symbol)
    
    if not conversion_symbol_info:
        conversion_symbol = f"USD{quote_currency}"
        conversion_symbol_info = mt5.symbol_info(conversion_symbol)
        if not conversion_symbol_info:
            raise ValueError(f"Cannot find conversion pair for {quote_currency}")
        
        conversion_rate = mt5.symbol_info_tick(conversion_symbol).ask
        return pip_value_quote / conversion_rate
    
    conversion_rate = mt5.symbol_info_tick(conversion_symbol).ask
    return pip_value_quote * conversion_rate

def get_pos_size2(symbol, risk_amount, stop_loss_pips):
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise ValueError(f"Symbol {symbol} not found")
    
    pip_value_per_lot = get_pip_value1(symbol)
    risk_per_lot = stop_loss_pips * pip_value_per_lot
    
    if risk_per_lot <= 0:
        raise ValueError("Invalid risk calculation")
    
    raw_position_size = risk_amount / risk_per_lot
    volume_step = symbol_info.volume_step
    position_size = round(raw_position_size / volume_step) * volume_step
    
    position_size = max(position_size, symbol_info.volume_min)
    position_size = min(position_size, symbol_info.volume_max)
    
    return position_size

MARTINGALE_MULTIPLIER = 1.01  # <-- Change this value as needed
MARTINGALE_TRADES = 20         # Number of trades in martingale sequence

# Add this function in your utility section
def ev_martingale(trades, rr, p, m):
    """Calculate expected value of martingale strategy"""
    import math  # Make sure this is imported at the top of your file
    q = 1.0 - p
    ev = 0.0
    for n in range(trades + 1):
        bet = math.pow(m, n)
        loss_sum = (math.pow(m, n) - 1.0) / (m - 1.0)
        
        if n < trades:
            reward = bet * rr
            profit = reward - loss_sum
            prob = p * math.pow(q, n)
        else:
            profit = -loss_sum
            prob = math.pow(q, trades)
        
        ev += prob * profit
    return ev

def calculate_cumulative_ev(trade_list, step_size, m, max_trades):
    """Calculate EV for cumulative trade groups (5, 10, 15 trades)"""
    ev_results = []
    trade_counts = []
    
    # Create checkpoints: 5, 10, 15,... up to max_trades
    current = step_size
    while current <= len(trade_list):
        trade_counts.append(current)
        current += step_size
    
    # Always include final count if not exact multiple
    if len(trade_list) not in trade_counts:
        trade_counts.append(len(trade_list))
    
    for n in trade_counts:
        # Get first n trades
        trades_subset = trade_list[:n]
        
        # Calculate metrics
        wins = sum(1 for t in trades_subset if calculate_trade_pnl(t) > 0)
        losses = n - wins
        
        try:
            p = wins / n
            avg_win = np.mean([calculate_trade_pnl(t) for t in trades_subset if calculate_trade_pnl(t) > 0])
            avg_loss = np.mean([abs(calculate_trade_pnl(t)) for t in trades_subset if calculate_trade_pnl(t) <= 0])
            rr = avg_win / avg_loss if avg_loss != 0 else 0
        except ZeroDivisionError:
            p = 0
            rr = 0
        
        # Calculate EV
        try:
            ev = ev_martingale(trades=step_size, rr=rr, p=p, m=m)
        except:
            ev = 0  # Fallback for calculation errors
            
        ev_results.append(ev)
    return trade_counts, ev_results

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


def is_pre_weekly_close(timestamp):
    """Check if within 5 minutes of weekly market close (Friday 20:55-21:00 Kyiv time)"""
    kyiv_tz = pytz.timezone('Europe/Kyiv')
    kyiv_time = timestamp.astimezone(kyiv_tz)
    return (
        kyiv_time.weekday() == 4 and  # Friday
        kyiv_time.hour == 20 and 
        kyiv_time.minute >= 45
    )

# Example usage
if __name__ == "__main__":
    # Load your price data (example with random data)
    #THE STRATEGY IS NOT GOOD FOR USDCAD you can only use (signal1 + signal3) to get good win-rate for USDCAD
    #THE STRATEGY IS NOT GOOD FOR EURGBP you can only use (signal1 + signal3) to get good win-rate for EURGBP
    #THE STRATEGY IS NOT GOOD FOR GBPMXN you can only use (signal1 + signal3) to get good win-rate for GBPMXN
    symbol = "GBPJPY"
    timeframe = "TIMEFRAME_M15"
    num_candles = 3840 #3840
    data =  get_hist_data(symbol, timeframe,num_candles, time_till=None )
    
    RISK_PER_TRADE = 10  # $10 risk per trade
    
    COMMISSION = 0.1     # $0 if no commission

    # ha_data = calculate_heikin_ashi(data)
    # data[['ha_open', 'ha_close', 'color','ha_high','ha_low']]= ha_data[['ha_open', 'ha_close', 'color','ha_high','ha_low']]
    data = data.dropna().copy()
    result1 = ichimoku_signals(data, conversion_period=20, base_period=60)
    #15min conversion_period=20, base_period=60
    #30min conversion_period=25, base_period=75
    #1hr conversion_period=33, base_period=99
    
    result2 = calculate_adx_histogram(data, period=24)
    #15min period=20
    #30min period=15
    #1hr period=14
    
    data['volatility'] = calculate_volatility(data, 38, 2.4)
    #print(data['volatility'].tail(20))
    data['sar'] = parabolic_sar(data, step=0.02, max_step=0.2)
    data.dropna(inplace=True)
    
    data[['+DI', '-DI', 'ADX', 'signal2']] = result2[['+DI', '-DI', 'ADX', 'signal2']]
    data['signal1'] = result1['signal1']

    data = data.tz_convert('Africa/Lagos') 
    # 2. Add session flags directly (no separate function needed)
    data['london_active'] = data.index.map(lambda x: is_session_active(x, "London"))
    data['newyork_active'] = data.index.map(lambda x: is_session_active(x, "New_York"))
    data['sydney_active'] = data.index.map(lambda x: is_session_active(x, "Sydney"))
    data['Tokyo_active'] = data.index.map(lambda x: is_session_active(x, "Tokyo"))
    def calculate_trade_pnl(trade):
        if trade['dir'] == 'long':
            pips = (trade['close_price'] - trade['open_price'])/get_pip(symbol)
        elif trade['dir'] == 'short':
            pips = (trade['open_price'] - trade['close_price'])/get_pip(symbol)
                
        dollar_pnl = (pips * trade['pip_value']) - trade['fees_paid']
        return dollar_pnl
    
    signal = None
    data["returns"] = 0.0
    trade_stats = []
    op_index = data.columns.to_list().index("open")
    cp_index = data.columns.to_list().index("close")
    hi_index = data.columns.to_list().index("high")
    lo_index = data.columns.to_list().index("low")
    returns_index = data.columns.to_list().index("returns")
    
    for i in range(len(data)-1):
        
        current_time = data.index[i]  # <-- This is where the timestamp comes from
            # ======== NEW CODE START ======== (COMMENT: Weekly close check)
        if is_pre_weekly_close(current_time) and signal is not None:
            if signal == 'long':
                close_price = data.iloc[i-1,cp_index]  # Exit at next bar's open
                trade_stats[-1]["close_price"] = close_price
                #data.iloc[i,returns_index] = (close_price - trade_stats[-1]["open_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
                signal = None
            elif signal == 'short':
                close_price = data.iloc[i-1,cp_index]  # Exit at next bar's open
                trade_stats[-1]["close_price"] = close_price
                #data.iloc[i,returns_index] = (trade_stats[-1]["open_price"] - close_price)/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
                signal = None
        
        if signal == None:
            
            if ((data.iloc[i]['signal1']==1)  &  (data.iloc[i]['signal2']==1)  #| data.iloc[i]['Tokyo_active']) 
                #data.iloc[i]['buy_signal3'] and data.iloc[i]['color']=="green" #signals.iloc[i]['buy']      # STC above 25 = bullish momentum  &(data.iloc[i]['close'] > data.iloc[i]['open']) 
                ):
                    
                    atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                    sl_pips = 1.5 * atr  # 1.5x ATR
                    tp_pips = 4.0 * atr  # 3x ATR (2:1 reward:risk)
                    # atr = data.iloc[i]['volatility'] / get_pip(symbol)
                    # volatility_ratio = atr / data['volatility'].mean()  # Relative volatility
                    # # Scale ratios inversely with volatility
                    # sl_pips = 1.2 * atr * (1 + (1/volatility_ratio))
                    # tp_pips = 2.4 * atr * (1 + volatility_ratio)
                    #sl_pips = data.iloc[i]['sl_pips']
                    #tp_pips = data.iloc[i]['tp_pips']
                    # Calculate position size based on risk
                    try:
                        pos_size = get_pos_size2(symbol, RISK_PER_TRADE, sl_pips)
                    except Exception as e:
                        print(f"Position sizing error: {e}")
                        continue
                    SPREAD_COST1 = pos_size*5    # $2 per round trip (adjust based on your broker)
                    # Store risk management parameters
                    pip_value = get_pip_value1(symbol) * pos_size
                    signal = 'long'
                    trade_stats.append({"time":data.index[i],
                                        "entry_bar": i,
                                        "dir":"long",
                                        "open_price":data.iloc[i+1,op_index] + 0.3*(data.iloc[i+1,hi_index] - data.iloc[i+1,op_index]), #factor slippage
                                        "close_price": None,
                                        #"sl_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]) - 10*get_pip(symbol),
                                        #"tp_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]) + 20*get_pip(symbol)
                                        "sl_price":data.iloc[i+1,op_index]  - sl_pips * get_pip(symbol),
                                        "tp_price":data.iloc[i+1,op_index]  + tp_pips * get_pip(symbol),
                                        "risk_amount": RISK_PER_TRADE,
                                        "position_size": pos_size,
                                        "pip_value": pip_value,
                                        "fees_paid": SPREAD_COST1 + (COMMISSION * 2)})
                    
            
            if ((data.iloc[i]['signal1']==-1)  &  (data.iloc[i]['signal2']==-1)# | data.iloc[i]['Tokyo_active'])
                #data.iloc[i]['sell_signal3'] and data.iloc[i]['color']=="red"  #signals.iloc[i]['sell']     # STC below 75 = bullish momentum  & (data.iloc[i]['close'] < data.iloc[i]['open']) 
                    ):
                    atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                    sl_pips = 1.5 * atr  # 1.5x ATR
                    tp_pips = 4.0 * atr  # 3x ATR (2:1 reward:risk)
                    # atr = data.iloc[i]['volatility'] / get_pip(symbol)
                    # volatility_ratio = atr / data['volatility'].mean()  # Relative volatility
                    # # Scale ratios inversely with volatility
                    # sl_pips = 1.2 * atr * (1 + (1/volatility_ratio))
                    # tp_pips = 2.4 * atr * (1 + volatility_ratio)
                    #sl_pips = data.iloc[i]['sl_pips']
                    #tp_pips = data.iloc[i]['tp_pips']
                    try:
                        pos_size = get_pos_size2(symbol, RISK_PER_TRADE, sl_pips)
                    except Exception as e:
                        print(f"Position sizing error: {e}")
                        continue
                    SPREAD_COST2 = pos_size*5    # $2 per round trip (adjust based on your broker)
                    # Store risk management parameters
                    pip_value = get_pip_value1(symbol) * pos_size
                    signal = 'short'
                    trade_stats.append({"time":data.index[i],
                                        "entry_bar": i,
                                        "dir":"short",
                                        "open_price":data.iloc[i+1,op_index] - 0.3*(data.iloc[i+1,op_index] - data.iloc[i+1,lo_index]), #factor slippage
                                        "close_price": None,
                                        #"sl_price":data[0].iloc[i+1,op_index] - 0.3*(data[0].iloc[i+1,op_index] - data[0].iloc[i+1,lo_index]) + 10*get_pip(symbol),
                                        #"tp_price":data[0].iloc[i+1,op_index] - 0.3*(data[0].iloc[i+1,op_index] - data[0].iloc[i+1,lo_index]) - 20*get_pip(symbol)
                                        "sl_price":data.iloc[i+1,op_index]  + sl_pips * get_pip(symbol),
                                        "tp_price":data.iloc[i+1,op_index]  - tp_pips * get_pip(symbol),
                                        "risk_amount": RISK_PER_TRADE,
                                        "position_size": pos_size,
                                        "pip_value": pip_value,
                                        "fees_paid": SPREAD_COST2 + (COMMISSION * 2)})                 
                            
        
        elif signal == "long":
            current_sar = data.iloc[i]['sar']
            max_hold_bars = 96 #12 * 6  # 4 hours for M15
            
        # Update SL to SAR if it's tighter
            #check if the MACD based signal reversed which would imply exiting position even though SL may not have reached
            #candle_data.iloc[i,-1] = (trade_stats[-1]["close_price"] - candle_data.iloc[i,op_index])/get_pip(symbol)
            if data.iloc[i,hi_index] > trade_stats[-1]["tp_price"]: 
                signal = None
                trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
                #data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
            elif data.iloc[i,lo_index] < trade_stats[-1]["sl_price"]: 
                signal = None
                trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
                #data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
            elif current_sar > trade_stats[-1]["sl_price"]:
                trade_stats[-1]["sl_price"] = current_sar
            elif (i - trade_stats[-1]["entry_bar"]) >= max_hold_bars:
                signal = None
                trade_stats[-1]["close_price"] =  data.iloc[i,cp_index ] 
                #data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
                
        elif signal == "short":
            current_sar = data.iloc[i]['sar']
            max_hold_bars = 96#12 * 6  # 4 hours for M15
            #candle_data.iloc[i,-1] = (candle_data.iloc[i,op_index] - trade_stats[-1]["close_price"])/get_pip(symbol) 
            if data.iloc[i,lo_index] < trade_stats[-1]["tp_price"]: 
                signal = None
                trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
                #data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
            elif data.iloc[i,hi_index] > trade_stats[-1]["sl_price"]: 
                signal = None
                trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
                #data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
            elif current_sar < trade_stats[-1]["sl_price"]:
                trade_stats[-1]["sl_price"] = current_sar
            elif (i - trade_stats[-1]["entry_bar"]) >= max_hold_bars:
                signal = None
                trade_stats[-1]["close_price"] =  data.iloc[i,cp_index ] 
                #data.iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
        # # if symbol == "USDSEK": 
        #     candle_data.iloc[i,-1] = candle_data.iloc[i,-1]/5 #adjust for pos size of USDSEK            
    if trade_stats and trade_stats[-1]["close_price"] == None:
        trade_stats[-1]["close_price"] = data.iloc[-1,cp_index] #update the cp of last trade as the current price
    
    
    # After processing all trades, add this analysis:
    total_wins = 0
    total_losses = 0
    gross_profit = 0
    gross_loss = 0
    net_profit = 0

    for trade in trade_stats:
        if trade['close_price'] is not None:
            pnl = calculate_trade_pnl(trade)
            net_profit += pnl
            if pnl > 0:
                total_wins += 1
                gross_profit += pnl
            else:
                total_losses += 1
                gross_loss += abs(pnl)

    print("\n=== Risk-Adjusted Performance ===")
    """
    if len(trade_stats) > 0:
        print("\n=== Cumulative EV Analysis ===")
        print(f"Step Size: {MARTINGALE_TRADES} trades")
        print(f"Multiplier: {MARTINGALE_MULTIPLIER}")
        
        # Get cumulative EV values
        x_vals, y_vals = calculate_cumulative_ev(
            trade_stats,
            step_size=MARTINGALE_TRADES,
            m=MARTINGALE_MULTIPLIER,
            max_trades=len(trade_stats)
        )
        
        # Print results
        for n, ev in zip(x_vals, y_vals):
            print(f"EV after {n} trades: ${ev:.2f}")
        
        # Plot results
        plot.figure(figsize=(10, 4))
        plot.plot(x_vals, y_vals, marker='o', linestyle='-')
        plot.title("Cumulative Martingale EV Progression")
        plot.xlabel("Number of Trades Analyzed")
        plot.ylabel("Expected Value ($)")
        plot.axhline(0, color='red', linestyle='--')
        plot.grid(True)
        plot.show()
    else:
        print("\nNo trades executed - EV analysis skipped")
    """
    print(f"Fixed Risk per Trade: ${RISK_PER_TRADE}")
    print(f"Total Trades: {len(trade_stats)}")
    print(f"Gross Profit: ${gross_profit:.2f}")
    print(f"Gross Loss: ${gross_loss:.2f}")
    print(f"Net Profit: ${net_profit:.2f}")
    print(f"Profit Factor: {gross_profit/max(gross_loss, 1):.2f}")
    print(f"Commission & Spread Costs: ${len(trade_stats) * (((SPREAD_COST2 + SPREAD_COST1)/2) + COMMISSION*2):.2f}")
    print("Number of trades taken:", len(trade_stats))
    retun = data['returns'][(data['returns'] > 0) | (data['returns'] < 0)].to_list()
    print(retun)
    # Modify your equity curve plotting:
    cumulative_pnl = [calculate_trade_pnl(trade) for trade in trade_stats if trade['close_price'] is not None]
    cumulative_series = pd.Series(cumulative_pnl).cumsum()
    cumulative_series.plot(title=f"Equity Curve (Risk per Trade: ${RISK_PER_TRADE})")
    plot.ylabel("Dollar P&L")
    plot.show()
    """
    #print backtesting results
    retun = data['returns'][(data['returns'] > 0) | (data['returns'] < 0)].to_list()
    print(retun)
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
    """