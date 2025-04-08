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

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THE CODE WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING
# Parameters
length = 80
mult = 3.0
symbol = "EURUSD"
timeframe1 = "TIMEFRAME_M5"
timeframe2 = "TIMEFRAME_M15"# Default timeframe
timeframe3 = "TIMEFRAME_H1"
timeframe4 = "TIMEFRAME_H4"
timeframe5 = "TIMEFRAME_D1"
lookback = 300  # Number of bars to fetch

# Get historical data
data1 = get_hist_data(symbol, timeframe1,99990, time_till=None )
data2 = get_hist_data(symbol, timeframe2,33400, time_till=None )
data3 = get_hist_data(symbol, timeframe3,17500, time_till=None )
data4 = get_hist_data(symbol, timeframe4,4380, time_till=None )
data5 = get_hist_data(symbol, timeframe5,730, time_till=None )

data = [data1, data2, data3, data4, data5]

for i in range(len(data)):
        # Calculate Zero-Lag EMA
        def zero_lag_ema(series, length):
            lag = (length - 1) // 2
            src = series + (series - series.shift(lag))
            return src.ewm(span=length, adjust=False).mean()

        data[i]['zlema'] = zero_lag_ema(data[i]['close'], length)

        # Calculate Volatility Bands
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

        data[i]['volatility'] = calculate_volatility(data[i], length, mult)

        data[i]['upper_band'] = data[i]['zlema'] + data[i]['volatility']
        data[i]['lower_band'] = data[i]['zlema'] + data[i]['volatility']
        data[i]['volume_ma'] = data[i]['tick_volume'].rolling(20).mean()
        
        def calculate_adx(df, period=14):
            """
            Calculate the Average Directional Index (ADX) for a DataFrame.
            """
            df = df.copy()
            
            # Calculate True Range (TR)
            df['high-low'] = df['high'] - df['low']
            df['high-close_prev'] = abs(df['high'] - df['close'].shift(1))
            df['low-close_prev'] = abs(df['low'] - df['close'].shift(1))
            df['tr'] = df[['high-low', 'high-close_prev', 'low-close_prev']].max(axis=1)
            
            # Calculate Directional Movement (+DM and -DM)
            df['plus_dm'] = df['high'].diff().apply(lambda x: x if x > 0 else 0)
            df['minus_dm'] = (-df['low'].diff()).apply(lambda x: x if x > 0 else 0)
            
            # Smooth the values using Wilder's EMA (Wilder uses 1/period smoothing)
            df['tr_smooth'] = df['tr'].ewm(alpha=1/period, adjust=False).mean()
            df['plus_dm_smooth'] = df['plus_dm'].ewm(alpha=1/period, adjust=False).mean()
            df['minus_dm_smooth'] = df['minus_dm'].ewm(alpha=1/period, adjust=False).mean()
            
            # Calculate Directional Indicators (+DI and -DI)
            df['plus_di'] = (df['plus_dm_smooth'] / df['tr_smooth']) * 100
            df['minus_di'] = (df['minus_dm_smooth'] / df['tr_smooth']) * 100
            
            # Calculate Directional Movement Index (DX)
            df['dx'] = (abs(df['plus_di'] - df['minus_di']) / 
                    (df['plus_di'] + df['minus_di'])) * 100
            
            # Calculate ADX (smoothed DX)
            df['adx'] = df['dx'].ewm(alpha=1/period, adjust=False).mean()
            return df['adx']
        data[i]['adx'] = calculate_adx(data[i], 14)
        
        def parabolic_sar(df, step=0.02, max_step=0.2):
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
        data[i]['sar'] = parabolic_sar(data[i], step=0.02, max_step=0.2)

        # Calculate Trend
        def calculate_trend(DF):
            df = DF.copy()
            # trend = np.zeros(len(df))
            # for i in range(1, len(df)):
            #     # Check for crossovers
            #     if df['close'].iloc[i] > df['upper_band'].iloc[i] and df['close'].iloc[i-1] <= df['upper_band'].iloc[i-1]:
            #         trend[i] = 1
            #     elif df['close'].iloc[i] < df['lower_band'].iloc[i] and df['close'].iloc[i-1] >= df['lower_band'].iloc[i-1]:
            #         trend[i] = -1
            #     else:
            #         trend[i] = trend[i-1]
            # Vectorized crossover detection
            df['upper_cross'] = (df['close'] > df['upper_band']) & (df['close'].shift() <= df['upper_band'])
            df['lower_cross'] = (df['close'] < df['lower_band']) & (df['close'].shift() >= df['lower_band'])
            
            # Calculate trend
            df['trend'] = 0
            df.loc[df['upper_cross'], 'trend'] = 1
            df.loc[df['lower_cross'], 'trend'] = -1
            df['trend'] = df['trend'].replace(0, np.nan).fillna(method='ffill')
            
            return df['trend']
            

        data[i]['trend'] = calculate_trend(data[i])
    

#___________________________________________________________________________________________________________________________________
# MOMENTUM BIAS INDEX CODE

def hma(series: Series, length: int) -> Series:
    """Hull Moving Average implementation"""
    wma_half = series.ewm(span=length//2, adjust=False).mean()
    wma_full = series.ewm(span=length, adjust=False).mean()
    return (2 * wma_half - wma_full).ewm(span=int(np.sqrt(length)), adjust=False).mean()

def calculate_momentum_bias(DF, params):
    df = DF.copy()
    """Calculate Momentum Bias Index components"""
    # Parameters
    ml = params['momentumLength']
    bl = params['biasLength']
    sl = params['smoothLength']
    ibl = params['impulseBoundaryLength']
    sdm = params['stdDevMultiplier']
    smooth = params['smoothIndicator']
    
    # Momentum calculations
    df['momentum'] = df['close'] - df['close'].shift(ml)
    hl_diff = df['high'] - df['low']
    df['stdDev'] = (df['momentum'] / hl_diff.ewm(span=ml, adjust=False).mean()) * 100
    
    # Momentum directions
    df['momentumUp'] = df['stdDev'].apply(lambda x: max(x, 0))
    df['momentumDown'] = df['stdDev'].apply(lambda x: min(x, 0))
    
    # Smoothed biases
    if smooth:
        df['momentumUpBias'] = hma(df['momentumUp'].rolling(bl).sum(), sl).clip(lower=0)
        df['momentumDownBias'] = hma(-df['momentumDown'].rolling(bl).sum(), sl).clip(lower=0)
    else:
        df['momentumUpBias'] = df['momentumUp'].rolling(bl).sum().clip(lower=0)
        df['momentumDownBias'] = (-df['momentumDown'].rolling(bl).sum()).clip(lower=0)
    
    # Boundary calculation
    df['averageBias'] = (df['momentumDownBias'] + df['momentumUpBias']) / 2
    df['boundary'] = (df['averageBias'].ewm(span=ibl, adjust=False).mean() + df['averageBias'].rolling(ibl).std() * sdm)
    
    return df

# Momentum Bias parameters
bias_params = {
    'momentumLength': 34,
    'biasLength': 3,
    'smoothLength': 10,
    'impulseBoundaryLength': 20,
    'stdDevMultiplier': 1.5,
    'smoothIndicator': True
    }

# Calculate Momentum Bias components
data[0] = calculate_momentum_bias(data[0], bias_params)
data[1] = calculate_momentum_bias(data[2], bias_params)

data[0].dropna(subset=['zlema', 'boundary', 'momentumUpBias'], inplace=True)
data[2].dropna(subset=['zlema'], inplace=True)
data[1].dropna(subset=['zlema','boundary', 'momentumUpBias'], inplace=True)
data[3].dropna(subset=['zlema'], inplace=True)
data[4].dropna(subset=['zlema'], inplace=True)

# def generate_combined_signals(df):
#     """Generate trading signals combining both strategies"""
#     # Zero Lag Trend Signals
#     df['trend'] = 0
#     df.loc[df['close'] > df['upper_band'], 'trend'] = 1
#     df.loc[df['close'] < df['lower_band'], 'trend'] = -1
    
#     # Momentum Bias Signals
#     df['bullishBias'] = (df['momentumUpBias'] > df['boundary']) & (df['momentumUpBias'] > df['momentumDownBias'])

#     df['bearishBias'] = (df['momentumDownBias'] > df['boundary']) & (df['momentumDownBias'] > df['momentumUpBias'])
    
#     # Combined Entry Conditions
#     df['bullish_entry'] = False
#     df['bearish_entry'] = False
    
#     # Bullish Entry: Zero Lag trend + Momentum Bias conditions
#     df.loc[(df['trend'] == 1) & 
#         (df['trend'].shift(1) == 1) &
#         (df['close'] > df['zlema']) &
#         (df['close'].shift(1) <= df['zlema']) &
#         (df['bullishBias']), 'bullish_entry'] = True
    
#     # Bearish Entry: Zero Lag trend + Momentum Bias conditions
#     df.loc[(df['trend'] == -1) & 
#         (df['trend'].shift(1) == -1) &
#         (df['close'] < df['zlema']) &
#         (df['close'].shift(1) >= df['zlema']) &
#         (df['bearishBias']), 'bearish_entry'] = True
    
#     return df


# Generate Signals
def generate_signals(DF):
    df1 = DF[0].copy()
    df2 = DF[1].copy()
    df3 = DF[2].copy()
    df4 = DF[3].copy()
    df5 = DF[4].copy()
    df1['bullishBias'] = (df1['momentumUpBias'] > df1['boundary']) 
    df1['bearishBias'] = (df1['momentumDownBias'] > df1['boundary'])
    df2['bullishBias'] = (df2['momentumUpBias'] > df2['boundary']) 
    df2['bearishBias'] = (df2['momentumDownBias'] > df2['boundary'])
    
    # df['bullishBias'] = (df['momentumUpBias'] > df['boundary'] * 0.5) & (df['momentumUpBias'] > df['momentumDownBias'] * 0.3)
    # df['bearishBias'] = (df['momentumDownBias'] > df['boundary']*0.5) & (df['momentumDownBias'] > df['momentumUpBias']*0.3)
    
    df1['bullish_entry'] = False
    df1['bearish_entry'] = False
    df2['bullish_entry'] = False
    df2['bearish_entry'] = False
    df3['bullish_entry'] = False
    df3['bearish_entry'] = False
    df4['bullish_entry'] = False
    df4['bearish_entry'] = False
    df5['bullish_entry'] = False
    df5['bearish_entry'] = False
    
    for i in range(2, len(df1)):
        # Bullish entry condition
        # prev_trend = df['trend'].iloc[i-1]
        # curr_trend = df['trend'].iloc[i]
    
        # if curr_trend == 1 and prev_trend == 1:
        #     crossover = (df['close'].iloc[i] > df['zlema'].iloc[i] and 
        #                 df['close'].iloc[i-1] <= df['zlema'].iloc[i-1])
        #     if crossover and df['bullishBias'].iloc[i]:
        #         df['bullish_entry'].iloc[i] = True
                
        # if curr_trend == -1 and prev_trend == -1:
        #     crossover = (df['close'].iloc[i] < df['zlema'].iloc[i] and 
        #                 df['close'].iloc[i-1] >= df['zlema'].iloc[i-1])
        #     if crossover and df['bullishBias'].iloc[i]:
        #         df['bearish_entry'].iloc[i] = True
        # Bullish condition
        if (df1.iat[i, df1.columns.get_loc('adx')] > 25 and 
            #df1.iat[i, df1.columns.get_loc('minus_di')] < df1.iat[i, df1.columns.get_loc('plus_di')] and
            df1.iat[i, df1.columns.get_loc('tick_volume')] > df1.iat[i, df1.columns.get_loc('volume_ma')] and
            df1.iat[i, df1.columns.get_loc('trend')] == 1 and 
            df1.iat[i-1, df1.columns.get_loc('trend')] == 1 and 
            #df1.iat[i-2, df1.columns.get_loc('trend')] == 1 and
            df1.iat[i, df1.columns.get_loc('close')] > df1.iat[i, df1.columns.get_loc('zlema')] and 
            df1.iat[i-1, df1.columns.get_loc('close')] > df1.iat[i-1, df1.columns.get_loc('zlema')] and 
            df1.iat[i, df1.columns.get_loc('bullishBias')]):
            df1.iat[i, df1.columns.get_loc('bullish_entry')] = True
        
        # Bearish condition (FIXED TYPO: changed bullishBias to bearishBias)
        if (df1.iat[i, df1.columns.get_loc('adx')] > 25 and
            #df1.iat[i, df1.columns.get_loc('minus_di')] > df1.iat[i, df1.columns.get_loc('plus_di')] and
            df1.iat[i, df1.columns.get_loc('tick_volume')] < df1.iat[i, df1.columns.get_loc('volume_ma')] and
            df1.iat[i, df1.columns.get_loc('trend')] == -1 and 
            df1.iat[i-1, df1.columns.get_loc('trend')] == -1 and 
            #df1.iat[i-2, df1.columns.get_loc('trend')] == -1 and
            df1.iat[i, df1.columns.get_loc('close')] < df1.iat[i, df1.columns.get_loc('zlema')] and 
            df1.iat[i-1, df1.columns.get_loc('close')] >= df1.iat[i-1, df1.columns.get_loc('zlema')] and 
            df1.iat[i, df1.columns.get_loc('bearishBias')]):  # CORRECTED THIS LINE
            df1.iat[i, df1.columns.get_loc('bearish_entry')] = True
    
    for i in range(2, len(df2)):
        if (df2.iat[i, df2.columns.get_loc('adx')] > 25 and 
            df2.iat[i, df2.columns.get_loc('trend')] == 1 and 
            df2.iat[i-1, df2.columns.get_loc('trend')] == 1  and
            #df2.iat[i-2, df2.columns.get_loc('trend')] == 1 and
            df2.iat[i, df2.columns.get_loc('bullishBias')]):
            df2.iat[i, df2.columns.get_loc('bullish_entry')] = True
        
        # Bearish condition (FIXED TYPO: changed bullishBias to bearishBias)
        if (df2.iat[i, df2.columns.get_loc('adx')] > 25 and 
            df2.iat[i, df2.columns.get_loc('trend')] == -1 and 
            df2.iat[i-1, df2.columns.get_loc('trend')] == -1  and
            #df2.iat[i-2, df2.columns.get_loc('trend')] == -1 and
            df2.iat[i, df2.columns.get_loc('bearishBias')]):  # CORRECTED THIS LINE
            df2.iat[i, df2.columns.get_loc('bearish_entry')] = True
    
    for i in range(2, len(df3)):
        if (df3.iat[i, df3.columns.get_loc('adx')] > 25 and 
            #df3.iat[i, df1.columns.get_loc('minus_di')] < df3.iat[i, df3.columns.get_loc('plus_di')] and
            df3.iat[i, df3.columns.get_loc('trend')] == 1 and 
            df3.iat[i-1, df3.columns.get_loc('trend')] == 1
            ):
            df3.iat[i, df3.columns.get_loc('bullish_entry')] = True
        
        # Bearish condition (FIXED TYPO: changed bullishBias to bearishBias)
        if (df3.iat[i, df3.columns.get_loc('adx')] > 25 and 
            #df3.iat[i, df1.columns.get_loc('minus_di')] > df3.iat[i, df3.columns.get_loc('plus_di')] and
            df3.iat[i, df3.columns.get_loc('trend')] == -1 and 
            df3.iat[i-1, df3.columns.get_loc('trend')] == -1 
            ):  # CORRECTED THIS LINE
            df3.iat[i, df3.columns.get_loc('bearish_entry')] = True
    
    for i in range(2, len(df4)):
        if (df4.iat[i, df4.columns.get_loc('adx')] > 25 and 
            df4.iat[i, df4.columns.get_loc('trend')] == 1 and 
            df4.iat[i-1, df4.columns.get_loc('trend')] == 1 ):
            df4.iat[i, df4.columns.get_loc('bullish_entry')] = True
        
        # Bearish condition (FIXED TYPO: changed bullishBias to bearishBias)
        if (df4.iat[i, df4.columns.get_loc('adx')] > 25 and 
            df4.iat[i, df4.columns.get_loc('trend')] == -1 and 
            df4.iat[i-1, df4.columns.get_loc('trend')] == -1 ):  # CORRECTED THIS LINE
            df4.iat[i, df4.columns.get_loc('bearish_entry')] = True
    
    for i in range(2, len(df5)):
        if (df5.iat[i, df5.columns.get_loc('adx')] > 25 and 
            df5.iat[i, df5.columns.get_loc('trend')] == 1 and 
            df5.iat[i-1, df5.columns.get_loc('trend')] == 1 ):
            df5.iat[i, df5.columns.get_loc('bullish_entry')] = True
        
        # Bearish condition (FIXED TYPO: changed bullishBias to bearishBias)
        if (df5.iat[i, df5.columns.get_loc('adx')] > 25 and 
            df5.iat[i, df5.columns.get_loc('trend')] == -1 and 
            df5.iat[i-1, df5.columns.get_loc('trend')] == -1 ):  # CORRECTED THIS LINE
            df5.iat[i, df5.columns.get_loc('bearish_entry')] = True
    
    
    return [df1, df2, df3, df4,df5]

signals = generate_signals(data)  # Ensure the function returns a DataFrame

# Assign each column separately
data[0]['bullish_entry'] = signals[0]['bullish_entry']
data[0]['bearish_entry'] = signals[0]['bearish_entry']
data[1]['bullish_entry'] = signals[1]['bullish_entry']
data[1]['bearish_entry'] = signals[1]['bearish_entry']
data[2]['bullish_entry'] = signals[2]['bullish_entry']
data[2]['bearish_entry'] = signals[2]['bearish_entry']
data[3]['bullish_entry'] = signals[3]['bullish_entry']
data[3]['bearish_entry'] = signals[3]['bearish_entry']
data[4]['bullish_entry'] = signals[4]['bullish_entry']
data[4]['bearish_entry'] = signals[4]['bearish_entry']

# print("Trend Distribution:\n", data['trend'].value_counts())
# print("\n--- Strategy Summary ---")
# print("Bullish Signals:", data['bullish_entry'].sum())
# print("Bearish Signals:", data['bearish_entry'].sum())
# test_data = data.iloc[-500:]
# print(test_data[['close','trend','bullish_entry']].tail(20))

# print("Sample signals:")
# print(data[data['bullish_entry'] | data['bearish_entry']][['close', 'trend', 'zlema']].head(10))

signal = None
data[0]["returns"] = 0
trade_stats = []
op_index = data[0].columns.to_list().index("open")
cp_index = data[0].columns.to_list().index("close")
hi_index = data[0].columns.to_list().index("high")
lo_index = data[0].columns.to_list().index("low")
returns_index = data[0].columns.to_list().index("returns")

# Strategy Implementation
for i in range(len(data[0])-1):
    # D = int(round((i/96), 1))
    # H4 = int(round((i/16), 1))
    # H1 = int(round((i/4), 1))
    # HD =int(round((i/24), 1))
    M15 = int(round((i/3), 1))
    MH4 = int(round((i/288), 1))
    if M15 >= len(data[1]) or MH4 >= len(data[4]):
        continue 
    
    atr = data[0].iloc[i]['volatility'] / get_pip(symbol)  # ATR in pips
    sl_pips = 1.5 * atr  # 1.5x ATR
    tp_pips = 3.0 * atr  # 3x ATR (2:1 reward:risk)
    
    if signal == None:
        if (data[0].iat[i, data[0].columns.get_loc('bullish_entry')] == True and\
            #data[1].iat[M15, data[1].columns.get_loc('bullish_entry')] == True 
            #data[2].iat[MH1, data[2].columns.get_loc('bullish_entry')] == True
            #data[3].iat[MH4, data[3].columns.get_loc('bullish_entry')] == True
            data[4].iat[MH4, data[4].columns.get_loc('bullish_entry')] == True
            ):
                signal = 'long'
                trade_stats.append({"time":data[0].index[i],
                                    "entry_bar": i,
                                    "dir":"long",
                                    "open_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]), #factor slippage
                                    "close_price": None,
                                    #"sl_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]) - 10*get_pip(symbol),
                                    #"tp_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]) + 20*get_pip(symbol)
                                    "sl_price":data[0].iloc[i+1,op_index]  - sl_pips * get_pip(symbol),
                                    "tp_price":data[0].iloc[i+1,op_index]  + tp_pips * get_pip(symbol)})
    
        elif (data[0].iat[i, data[0].columns.get_loc('bearish_entry')] == True and\
             #data[1].iat[M15, data[1].columns.get_loc('bearish_entry')] == True 
             #data[2].iat[MH1, data[2].columns.get_loc('bearish_entry')] == True
                #data[3].iat[MH4, data[3].columns.get_loc('bearish_entry')] == True
                data[4].iat[MH4, data[4].columns.get_loc('bullish_entry')] == True
                ):
                signal = 'short'
                trade_stats.append({"time":data[0].index[i],
                                    "entry_bar": i,
                                    "dir":"short",
                                    "open_price":data[0].iloc[i+1,op_index] + 0.3*(data[0].iloc[i+1,hi_index] - data[0].iloc[i+1,op_index]), #factor slippage
                                    "close_price": None,
                                    #"sl_price":data[0].iloc[i+1,op_index] - 0.3*(data[0].iloc[i+1,op_index] - data[0].iloc[i+1,lo_index]) + 10*get_pip(symbol),
                                    #"tp_price":data[0].iloc[i+1,op_index] - 0.3*(data[0].iloc[i+1,op_index] - data[0].iloc[i+1,lo_index]) - 20*get_pip(symbol)
                                    "sl_price":data[0].iloc[i+1,op_index]  + sl_pips * get_pip(symbol),
                                    "tp_price":data[0].iloc[i+1,op_index]  - tp_pips * get_pip(symbol)})                 
                        
    elif signal == "long":
        current_sar = data[0].iloc[i]['sar']
    # Update SL to SAR if it's tighter
        #check if the MACD based signal reversed which would imply exiting position even though SL may not have reached
        #candle_data.iloc[i,-1] = (trade_stats[-1]["close_price"] - candle_data.iloc[i,op_index])/get_pip(symbol)
        if data[0].iloc[i,hi_index] > trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            data[0].iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif data[0].iloc[i,lo_index] < trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            data[0].iloc[i,returns_index] = (trade_stats[-1]["close_price"]- trade_stats[-1]["open_price"])/get_pip(symbol)
        elif current_sar > trade_stats[-1]["sl_price"]:
            trade_stats[-1]["sl_price"] = current_sar
            
            
    elif signal == "short":
        current_sar = data[0].iloc[i]['sar']
        #candle_data.iloc[i,-1] = (candle_data.iloc[i,op_index] - trade_stats[-1]["close_price"])/get_pip(symbol) 
        if data[0].iloc[i,lo_index] < trade_stats[-1]["tp_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["tp_price"] 
            data[0].iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        elif data[0].iloc[i,hi_index] > trade_stats[-1]["sl_price"]: 
            signal = None
            trade_stats[-1]["close_price"] =   trade_stats[-1]["sl_price"] 
            data[0].iloc[i,returns_index] = (trade_stats[-1]["open_price"]- trade_stats[-1]["close_price"])/get_pip(symbol)
        elif current_sar > trade_stats[-1]["sl_price"]:
            trade_stats[-1]["sl_price"] = current_sar
    # if symbol == "USDSEK": 
    #     candle_data.iloc[i,-1] = candle_data.iloc[i,-1]/5 #adjust for pos size of USDSEK            
if trade_stats and trade_stats[-1]["close_price"] == None:
    trade_stats[-1]["close_price"] = data[0].iloc[-1,cp_index] #update the cp of last trade as the current price


#print backtesting results
print("cumulative return in pips = ",data[0]["returns"].cumsum()[-1])
print("win rate of the strategy = {:2f}%".format(win_rate(trade_stats)))
print("average pip return per winning trade = {:2f}".format(mean_ret_winner_pip(trade_stats, symbol)))
print("average pip return per losing trade = {:2f}".format(mean_ret_loser_pip(trade_stats, symbol)))
print("maximum drawdown in pips = {:2f}".format(max_drawdown(data[0])))
#monthly_performance(returns_df)

print("Number of trades taken:", len(trade_stats))

#plot equity curve in terms of pip
data[0]["returns"].cumsum().plot()
plot.show()
# Display signals
print(data[0][['close', 'zlema', 'upper_band', 'lower_band', 'trend', 'bullish_entry', 'bearish_entry']].tail(20))

mt5.shutdown()

# # Buy when bullish trend and bullish entry signal
# if bullish_trend and bullish_entry:
#     enter_long()

# # Sell when bearish trend and bearish entry signal
# if bearish_trend and bearish_entry:
#     enter_short()
# Risk Management (add these to your strategy):


# # Add these parameters
# stop_loss_pct = 1.0  # 1% stop loss
# take_profit_pct = 2.0  # 2% take profit

# def calculate_lot_size(balance, risk_percent):
#     return (balance * risk_percent/100) / stop_loss_pct

# def calculate_stop_loss(entry_price, direction):
#     if direction == 'long':
#         return entry_price * (1 - stop_loss_pct/100)
#     else:
#         return entry_price * (1 + stop_loss_pct/100)

# def calculate_take_profit(entry_price, direction):
#     if direction == 'long':
#         return entry_price * (1 + take_profit_pct/100)
#     else:
#         return entry_price * (1 - take_profit_pct/100)
# #MT5 Order Execution (example for buy orders):


# def mt5_buy(symbol, lot_size, stop_loss, take_profit):
#     price = mt5.symbol_info_tick(symbol).ask
#     deviation = 20
    
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot_size,
#         "type": mt5.ORDER_TYPE_BUY,
#         "price": price,
#         "sl": stop_loss,
#         "tp": take_profit,
#         "deviation": deviation,
#         "magic": 123456,
#         "comment": "Bullish Entry",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_FOK,
#     }
    
#     result = mt5.order_send(request)
#     return result