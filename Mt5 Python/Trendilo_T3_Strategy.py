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
#file_path = r"C:\Users\user\Documents\LANRE\Desktop\FRONTEND\Mt5 Python\key.txt"
key = open(file_path,"r").read().split()
path1 = "C:\\Users\\user\\AppData\\Roaming\\MetaTrader 5\\terminal64.exe"#For the executable path when we run the code

#since we are importing the user id we must convert it to an integer int(key[0])
if not mt5.initialize(path = path1, login= int(key[0]),password=key[1], server=key[2]):
    #print("initialize() failed, error code =",mt5.last_error())
    print("connection not established")
else:
    print("connection established")


# Get price data
#______________________________________________________________________________________________________________________________________________________________
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


#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THE CODE WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

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

def t3ma(series, length, vol_factor):
    """Calculate T3 Moving Average"""
    # Calculate multiple EMAs
    e1 = series.ewm(span=length, adjust=False).mean()
    e2 = e1.ewm(span=length, adjust=False).mean()
    e3 = e2.ewm(span=length, adjust=False).mean()
    e4 = e3.ewm(span=length, adjust=False).mean()
    e5 = e4.ewm(span=length, adjust=False).mean()
    e6 = e5.ewm(span=length, adjust=False).mean()
    
    # Calculate coefficients
    b = vol_factor
    c1 = -b**3
    c2 = 3*b**2 + 3*b**3
    c3 = -6*b**2 - 3*b - 3*b**3
    c4 = 1 + 3*b + b**3 + 3*b**2
    
    return c1*e6 + c2*e5 + c3*e4 + c4*e3

def generate_signals(DF, fast_length=8, slow_length=13, 
                    fast_vol=0.7, slow_vol=0.6, use_heikin_ashi=False):
    """
    Generate trading signals based on T3MA crossover system
    Returns DataFrame with signals and indicator values
    """
    df = DF.copy()
    # 1. Convert to Heikin Ashi if enabled
    if use_heikin_ashi:
        df = calculate_heikin_ashi(df)
    
    # 2. Calculate T3 Moving Averages
    df['fast_t3'] = t3ma(df['close'], fast_length, fast_vol)
    df['slow_t3'] = t3ma(df['close'], slow_length, slow_vol)
    
    # 3. Generate Signals
    df['buy_signal1'] = (df['close'] > df['fast_t3']) & (df['close'] > df['slow_t3'])
    df['sell_signal1'] = (df['close'] < df['fast_t3']) & (df['close'] < df['slow_t3'])
    
    # 4. Clean data
    df.dropna(inplace=True)
    return df
#===============================================================================================================================
def alma(series, window=50, offset=0.85, sigma=6):
    """
    Arnaud Legoux Moving Average (ALMA)
    series: Input data series
    window: Lookback period
    offset: Gaussian window offset (0.85 = near the end)
    sigma: Gaussian window width
    """
    # Calculate Gaussian weights
    m = offset * (window - 1)
    s = window / sigma
    weights = np.arange(window)
    weights = np.exp(-((weights - m)**2)/(2*s**2))
    weights /= weights.sum()
    
    # Apply weights using rolling window
    alma = series.rolling(window=window).apply(
        lambda x: np.sum(x * weights[-len(x):]), raw=True
    )
    return alma

def calculate_trendilo_signals(DF, lookback=50, smooth=1, offset=0.85, sigma=6, 
                            band_mult=1.0, use_custom_band=False, custom_band_len=20):
    """
    Calculate Trendilo indicator and generate signals
    Returns DataFrame with indicator values and signals
    """
    df = DF.copy()
    # 1. Calculate percentage change
    df['pct_change'] = df['close'].pct_change(periods=smooth) * 100
    
    # 2. Calculate ALMA of percentage change
    df['avpch'] = alma(df['pct_change'], window=lookback, offset=offset, sigma=sigma)
    
    # 3. Calculate RMS bands
    band_length = custom_band_len if use_custom_band else lookback
    squared = df['avpch'].rolling(band_length).apply(lambda x: (x**2).mean())
    df['upper_band'] = band_mult * np.sqrt(squared)
    df['lower_band'] = -df['upper_band']
    
    # 4. Generate signals
    df['buy_signal2'] = df['avpch'] > df['upper_band']
    df['sell_signal2'] = df['avpch'] < df['lower_band']
    
    # Clean up
    df.dropna(inplace=True)
    return df
#=================================================================================================================================

def rma(series, period):
    """Wilder's Moving Average (RMA) calculation"""
    return series.ewm(alpha=1/period, adjust=False).mean()

def calculate_ma_adx(DF, adx_length=14, adx_smoothing=14, ma_length=34, adx_threshold=18):
    """
    Calculate MA ADX indicator with signals
    Returns DataFrame with indicators and signals
    """
    df = DF.copy()
    # Calculate True Range
    df['prev_high'] = df['high'].shift(1)
    df['prev_low'] = df['low'].shift(1)
    df['prev_close'] = df['close'].shift(1)
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['prev_close'])
    df['tr3'] = abs(df['low'] - df['prev_close'])
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    
    # Calculate Directional Movements
    df['up'] = df['high'].diff()
    df['down'] = -df['low'].diff()
    
    # Calculate +DM and -DM
    df['plus_dm'] = np.where((df['up'] > df['down']) & (df['up'] > 0), df['up'], 0)
    df['minus_dm'] = np.where((df['down'] > df['up']) & (df['down'] > 0), df['down'], 0)
    
    # Calculate DI values
    df['tr_rma'] = rma(df['tr'], adx_length)
    df['plus_di'] = 100 * rma(df['plus_dm'], adx_length) / df['tr_rma']
    df['minus_di'] = 100 * rma(df['minus_dm'], adx_length) / df['tr_rma']
    
    # Calculate ADX
    df['dx'] = abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di']).replace(0, 1)
    df['adx'] = 100 * rma(df['dx'], adx_smoothing)
    
    # Calculate Weighted Moving Average
    weights = pd.Series(np.arange(1, ma_length+1), index=np.arange(ma_length))
    df['ma'] = df['close'].rolling(ma_length).apply(
        lambda x: (x * weights[:len(x)]).sum() / weights[:len(x)].sum())
    
    # Generate color signals
    df['ma_color'] = np.where(
        (df['adx'] > adx_threshold) & (df['plus_di'] > df['minus_di']), 
        'green', 
        np.where(
            (df['adx'] > adx_threshold) & (df['plus_di'] < df['minus_di']), 
            'red', 
            'neutral'
        )
    )
    
    # Generate buy/sell signals
    df['buy_signal3'] = df['ma_color'].eq('green') & df['ma_color'].shift(1).ne('green')
    df['sell_signal3'] = df['ma_color'].eq('red') & df['ma_color'].shift(1).ne('red')
    
    return df.dropna().copy()

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


#===========================================================================================================================================

if __name__ == "__main__":
    # Get data from MT5
    symbol = "AUDUSD"
    timeframe = "TIMEFRAME_M15"
    data = get_hist_data(symbol, timeframe,num_candles=35040,time_till=None)
    data = data.dropna().copy()
    
    if data is not None:
        # Generate signals
        data1 = generate_signals(data, fast_length=45, slow_length=50, 
                    fast_vol=0.7, slow_vol=0.6, use_heikin_ashi=False)
        data2 = calculate_trendilo_signals(data, lookback=50, smooth=1, offset=0.85, sigma=6, 
                            band_mult=1.0, use_custom_band=False, custom_band_len=20)
        data3 = calculate_ma_adx(data, adx_length=14, adx_smoothing=14, ma_length=34, adx_threshold=18)
        ha_data = calculate_heikin_ashi(data)
        data[['ha_open', 'ha_close', 'color']]= ha_data[['ha_open', 'ha_close', 'color']]
        data['volatility'] = calculate_volatility(data, 34, 2.4)
        #print(data['volatility'].tail(20))
        data['sar'] = parabolic_sar(data, step=0.02, max_step=0.2)
        
        # 1. Create signal copies with unique names
        data['buy_signal1'] = data1['buy_signal1']
        data['sell_signal1'] = data1['sell_signal1']
        data['buy_signal2'] = data2['buy_signal2']
        data['sell_signal2'] = data2['sell_signal2']
        data['buy_signal3'] = data3['buy_signal3']
        data['sell_signal3'] = data3['sell_signal3']
        
        # signal_cols = {
        #     'buy_signal1': data1['buy_signal1'],
        #     'sell_signal1': data1['sell_signal1'],
        #     'buy_signal2': data2['buy_signal2'],
        #     'sell_signal2': data2['sell_signal2'],
        #     'buy_signal3': data3['buy_signal3'],
        #     'sell_signal3': data3['sell_signal3']
        # }
        
        # # 2. Add to main dataframe
        # data = data.assign(**signal_cols)
        
        # # 3. Fill any missing signals (due to indicator calculations)
        # data[signal_cols.keys()] = data[signal_cols.keys()].ffill().fillna(False)

        
        
        print("\nLatest Trading Signals:")
        print(f"Signal1: {data1['buy_signal1']} | {data1['sell_signal1']}")
        print(f"Signal2: {data2['buy_signal2']} | {data2['sell_signal2']}")
        print(f"Signal3: {data3['buy_signal3']} | {data3['sell_signal3']}")
        

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
            if (data.iloc[i]['buy_signal1'] and data.iloc[i]['buy_signal2']
                #data.iloc[i]['buy_signal3'] and data.iloc[i]['color']=="green" #signals.iloc[i]['buy']      # STC above 25 = bullish momentum
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
        
            elif (data.iloc[i]['sell_signal1'] and data.iloc[i]['sell_signal2'] and\
                data.iloc[i]['sell_signal3'] and data.iloc[i]['color']=="red"  #signals.iloc[i]['sell']     # STC below 75 = bullish momentum
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
