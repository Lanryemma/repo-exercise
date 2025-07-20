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

def calculate_heikin_ashi(df):
    ha = df.copy()
    
    # Initialize columns
    ha['ha_close'] = (ha['open'] + ha['high'] + ha['low'] + ha['close']) / 4
    ha['ha_open'] = (ha['open'].shift(1) + ha['close'].shift(1)) / 2
    ha['ha_high'] = ha[['high', 'ha_open', 'ha_close']].max(axis=1)
    ha['ha_low'] = ha[['low', 'ha_open', 'ha_close']].min(axis=1)
    
    ha['color'] = np.where(ha['ha_close'] > ha['ha_open'], 'green', 'red')
    return ha[['ha_open', 'ha_close', 'color','ha_high','ha_low']]


#  ---------------------------------------
# Kalman Filter implementation======================================================================================
def kalman_filter(series, length, R=0.01, Q=0.1):
    estimates = np.zeros(len(series))
    error_est = 1.0
    
    # Use .iloc for position-based access
    estimates[0] = series.iloc[0]  # First element
    
    for i in range(1, len(series)):
        prediction = estimates[i-1]
        
        # Kalman gain calculation
        error_meas = R * length
        kalman_gain = error_est / (error_est + error_meas)
        
        # Use .iloc for position-based access
        current_value = series.iloc[i]
        estimates[i] = prediction + kalman_gain * (current_value - prediction)
        
        # Error estimate update
        error_est = (1 - kalman_gain) * error_est + Q / length
    
    return pd.Series(estimates, index=series.index)

# Calculate signals
def calculate_signals(DF, short_len=50, long_len=150):
    df = DF.copy()
    # Calculate Kalman filters
    df['short_kalman'] = kalman_filter(df['close'], short_len)
    df['long_kalman'] = kalman_filter(df['close'], long_len)
    
    # Generate trend signals
    df['signal1'] = np.where(
        df['short_kalman'] > df['long_kalman'], 
        1,  # Up trend
        -1  # Down trend
    )
    
    return df

# 3. Indicator Calculation
def calculate_xmaster_signals(DF, short_ema=10, long_ema=38):
    df = DF.copy()
    # Calculate EMAs
    df['EMA_Short'] = df['close'].ewm(span=short_ema, adjust=False).mean()
    df['EMA_Long'] = df['close'].ewm(span=long_ema, adjust=False).mean()
    
    # Calculate normalized difference
    df['MA_Diff'] = df['EMA_Short'] - df['EMA_Long']
    df['Min_Diff'] = df['MA_Diff'].expanding().min()
    df['Max_Diff'] = df['MA_Diff'].expanding().max()
    
    # Handle division by zero
    diff_range = df['Max_Diff'] - df['Min_Diff']
    df['Normalized'] = 100 * (df['MA_Diff'] - df['Min_Diff']) / diff_range.replace(0, 1)
    
    # Generate signals
    df['signal2'] = 0
    #df.loc[(df['Normalized'] < 55) & (df['Normalized'] > 50), 'signal2'] = 1   # Green line
    #df.loc[(df['Normalized'] < 50) & (df['Normalized'] > 45), 'signal2'] = -1   # Green line
    df.loc[df['Normalized'] > 50, 'signal2'] = 1   # green line
    df.loc[df['Normalized'] < 50, 'signal2'] = -1   # Red line
    return df

# Calculate technical components
def calculate_components(DF, ema_period=26, atr_period=26, atr_multiplier=1.0):
    df = DF.copy()
    # Calculate True Range
    df['prev_close'] = df['close'].shift(1)
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.abs(df['high'] - df['prev_close']),
        np.abs(df['low'] - df['prev_close'])
    )
    
    # Calculate ATR
    df['atr'] = df['tr'].ewm(span=atr_period, adjust=False).mean() * atr_multiplier
    
    # Calculate price mean (simplified EMA)
    df['price_mean'] = df['close'].ewm(span=ema_period, adjust=False).mean()
    
    return df.dropna()

# Generate MDX signals
def generate_mdx_signals(df):
    # Calculate price deviation from mean
    df['deviation'] = df['close'] - df['price_mean']
    
    # Calculate MDX values
    df['mdx'] = np.where(
        df['deviation'] > 0,
        np.maximum(df['deviation'] - df['atr'], 0),
        np.minimum(df['deviation'] + df['atr'], 0)
    )
    
    # Generate signals (1 for buy, -1 for sell)
    df['signal3'] = np.where(df['mdx'] > 0, 1, np.where(df['mdx'] < 0, -1, 0))
    df['signal3'] = df['signal3'].replace(0, method='ffill')  # Carry forward signals
    
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

def parabolic_sar1(df, step=0.02, max_step=0.2):#(df, step=0.035, max_step=0.28)
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
        

def parabolic_sar(df, step=0.02, max_step=0.2):
    df = df.copy()
    high = df['high'].values
    low = df['low'].values
    sar = np.full(len(df), np.nan)
    trend = 1  # 1 = bullish, -1 = bearish
    
    # Correct initial EP: high[0] for bullish, low[0] for bearish
    ep = high[0] if trend == 1 else low[0]
    af = step
    
    # Initial SAR (first value)
    sar[0] = low[0] if trend == 1 else high[0]
    
    for i in range(1, len(df)):
        # Calculate interim SAR
        sar[i] = sar[i-1] + af * (ep - sar[i-1])
        
        if trend == 1:
            # Update EP FIRST (even if reversal happens)
            if high[i] > ep:
                ep = high[i]
                af = min(af + step, max_step)
            
            # Check reversal
            if low[i] < sar[i]:
                trend = -1
                sar[i] = ep  # Set to prior bullish EP, not current high!
                ep = low[i]  # New bearish EP
                af = step
            else:
                # Non-reversal adjustment
                sar[i] = min(sar[i], low[i-1], low[max(0, i-2)])
        else:
            # Update EP FIRST
            if low[i] < ep:
                ep = low[i]
                af = min(af + step, max_step)
            
            # Check reversal
            if high[i] > sar[i]:
                trend = 1
                sar[i] = ep  # Set to prior bearish EP, not current low!
                ep = high[i]  # New bullish EP
                af = step
            else:
                # Non-reversal adjustment
                sar[i] = max(sar[i], high[i-1], high[max(0, i-2)])
        df['sar'] = sar
    return df['sar'] #pd.Series(sar, index=df.index)

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
    symbol = "BTCUSD"
    timeframe = "TIMEFRAME_M1"
    num_candles = 69560 #3840
    data =  get_hist_data(symbol, timeframe,num_candles, time_till=None )
    
    RISK_PER_TRADE = 5  # $10 risk per trade
    base_risk = 5  # Starting risk amount
    current_risk = base_risk
    consecutive_losses = 0
    max_consecutive_losses = 5
    COMMISSION = 0.1     # $0 if no commission
    

    # ha_data = calculate_heikin_ashi(data)
    # data[['ha_open', 'ha_close', 'color','ha_high','ha_low']]= ha_data[['ha_open', 'ha_close', 'color','ha_high','ha_low']]
    data = data.dropna().copy()
    
    # Calculate indicator
        # Scalping (M1-M15)
    # 'M1':   {'short_len': 180,  'long_len': 540},   # 3hr/9hr
    # 'M5':   {'short_len': 72,   'long_len': 216},   # 6hr/18hr
    # 'M15':  {'short_len': 48,   'long_len': 144},   # 12hr/36hr
    
    # # Day Trading (M30-H4)
    # 'M30':  {'short_len': 24,   'long_len': 72},    # 12hr/36hr
    # 'H1':   {'short_len': 50,   'long_len': 150},   # Original (50hr/150hr)
    # 'H4':   {'short_len': 18,   'long_len': 54},    # 3d/9d
    
    
    #result1 = calculate_components(data, ema_period=26, atr_period=26, atr_multiplier=1.0)  # 80 bars ≈ 20 hours
    result3 = calculate_components(data, ema_period=20, atr_period=14, atr_multiplier=1.5)# for 5 minutes
    #result3 = calculate_components(data, ema_period=18, atr_period=12, atr_multiplier=1.8)# for 15 minutes
    #result3 = calculate_components(data, ema_period=30, atr_period=20, atr_multiplier=1.8)# for 30 minutes
    #result1 = calculate_components(data, ema_period=50, atr_period=26, atr_multiplier=2.0)# for 1 hour
    
    result1 = calculate_signals(data, short_len=48, long_len=144) 
    result2 = calculate_xmaster_signals(data, short_ema=10, long_ema=38) #for M1-M5 (short_ema=10, long_ema=38) | for M15-H1 (short_ema=12, long_ema=48) |
    result4 = generate_mdx_signals(result3)
    data['volatility'] = calculate_volatility(data, 34, 2.4)
        #print(data['volatility'].tail(20))
    data = calculate_adaptive_sl_tp(data, symbol, risk_reward_ratio=2)
    atr_ratio = data['volatility'].iloc[-1] / data['volatility'].mean()
    dynamic_step = max(0.01, min(0.025, 0.018 * atr_ratio))

    data['sar'] = parabolic_sar(data, step=0.02, max_step=0.25)
    data['prev_sar'] = data['sar'].shift(1)  # Use yesterday's PSAR today
    # 1. Convert to proper timezone-aware index
    data = data.tz_convert('Africa/Lagos') 
    # 2. Add session flags directly (no separate function needed)
    data['london_active'] = data.index.map(lambda x: is_session_active(x, "London"))
    data['newyork_active'] = data.index.map(lambda x: is_session_active(x, "New_York"))
    data['sydney_active'] = data.index.map(lambda x: is_session_active(x, "Sydney"))
    data['Tokyo_active'] = data.index.map(lambda x: is_session_active(x, "Tokyo"))
    data['signal1'] = result1['signal1']
    data['signal2'] = result2['signal2']
    data['signal3'] = result4['signal3']
    data["ema1"] = data["close"].ewm(span=3, adjust=False).mean() 
    data["ema2"] = data["close"].ewm(span=15, adjust=False).mean() 
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
        
        if signal is None:
            # Martingale risk adjustment
            if trade_stats and trade_stats[-1]["close_price"] is not None:
                last_trade = trade_stats[-1]
                last_pnl = calculate_trade_pnl(last_trade)
                
                # Reset risk after win
                if last_pnl > 0:
                    consecutive_losses = 0
                    current_risk = base_risk
                # Increase risk after loss
                else:
                    consecutive_losses += 1
                    if consecutive_losses <= max_consecutive_losses:
                        current_risk = base_risk * (1 + consecutive_losses)
                        #print(f"Martingale: Loss #{consecutive_losses}, new risk: ${current_risk}")
                    else:
                        current_risk = base_risk
                        #print("Max consecutive losses reached, resetting to base risk")
        
        #RISK_PER_TRADE
        risk = RISK_PER_TRADE#current_risk
        
        if signal == None:
            
            if ( (data.iloc[i]['signal1']==1) &(data.iloc[i]['signal2']==-1) &(data.iloc[i]['signal3']==1) #&\
                #(data.iloc[i]['newyork_active'] |data.iloc[i]['london_active'])# | data.iloc[i]['Tokyo_active']) #(data.iloc[i]['signal3']==1)&\
                #(data.iloc[i]['newyork_active'] |data.iloc[i]['london_active'] )#| data.iloc[i]['Tokyo_active']) #& (data.iloc[i]['signal3']==1)  #& (data.iloc[i]['newyork_active'] |data.iloc[i]['london_active'])# | data.iloc[i]['Tokyo_active']) 
                #data.iloc[i]['buy_signal3'] and data.iloc[i]['color']=="green" #signals.iloc[i]['buy']      # STC above 25 = bullish momentum  &(data.iloc[i]['close'] > data.iloc[i]['open']) 
                ):
                    
                    atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                    sl_pips = 1.0 * atr  # 1.5x ATR
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
                        pos_size = get_pos_size2(symbol, risk, sl_pips)
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
                    
            
            if ((data.iloc[i]['signal1']==-1) &(data.iloc[i]['signal2']==1) &(data.iloc[i]['signal3']==-1) #&\
                #(data.iloc[i]['newyork_active'] |data.iloc[i]['london_active'])# | data.iloc[i]['Tokyo_active']) #(data.iloc[i]['signal3']==1)&\
                #(data.iloc[i]['newyork_active'] |data.iloc[i]['london_active'] )#| data.iloc[i]['Tokyo_active']) #& (data.iloc[i]['signal3']==1)  #& (data.iloc[i]['newyork_active'] |data.iloc[i]['london_active'])# | data.iloc[i]['Tokyo_active']) 
                #data.iloc[i]['sell_signal3'] and data.iloc[i]['color']=="red"  #signals.iloc[i]['sell']     # STC below 75 = bullish momentum  & (data.iloc[i]['close'] < data.iloc[i]['open']) 
                    ):
                    atr = data.iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
                    sl_pips = 1.0 * atr  # 1.5x ATR
                    tp_pips = 4.0 * atr  # 3x ATR (2:1 reward:risk)
                    # atr = data.iloc[i]['volatility'] / get_pip(symbol)
                    # volatility_ratio = atr / data['volatility'].mean()  # Relative volatility
                    # # Scale ratios inversely with volatility
                    # sl_pips = 1.2 * atr * (1 + (1/volatility_ratio))
                    # tp_pips = 2.4 * atr * (1 + volatility_ratio)
                    #sl_pips = data.iloc[i]['sl_pips']
                    #tp_pips = data.iloc[i]['tp_pips']
                    try:
                        pos_size = get_pos_size2(symbol, risk, sl_pips)
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
            current_sar = data.iloc[i]['prev_sar']
            max_hold_bars = 96*3 #12 * 6  # 4 hours for M15
            
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
            # elif current_sar > trade_stats[-1]["open_price"]:  # Only if above entry
            #     if current_sar > trade_stats[-1]["sl_price"]:  # Only if tighter
            #         trade_stats[-1]["sl_price"] = current_sar
            elif (i - trade_stats[-1]["entry_bar"]) >= max_hold_bars:
                signal = None
                trade_stats[-1]["close_price"] =  data.iloc[i,cp_index ] 
                #data.iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
                data.iloc[i,returns_index] = calculate_trade_pnl(trade_stats[-1]) 
                
        elif signal == "short":
            current_sar = data.iloc[i]['prev_sar']
            max_hold_bars = 96*3#12 * 6  # 4 hours for M15
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
            # elif current_sar < trade_stats[-1]["open_price"]:  # Only if above entry
            #     if current_sar < trade_stats[-1]["sl_price"]:  # Only if tighter
            #         trade_stats[-1]["sl_price"] = current_sar
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
    total_fees = sum(trade['fees_paid'] for trade in trade_stats)
    print(f"Commission & Spread Costs: ${total_fees:.2f}")
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