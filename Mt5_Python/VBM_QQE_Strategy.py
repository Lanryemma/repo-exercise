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

def calculate_vbm_signals(df, factor=4, pd=14):
    """Calculate Buy/Sell signals based on volatility bands."""
    # Calculate ATR and Mid-Price (hl2)
    df['hl2'] = (df['high'] + df['low']) / 2
    df['tr'] = np.maximum(df['high'] - df['low'], 
                        np.maximum(abs(df['high'] - df['close'].shift()), 
                                    abs(df['low'] - df['close'].shift())))
    df['atr'] = df['tr'].rolling(pd).mean()
    
    # Initialize bands
    df['Up'] = df['hl2'] - (factor * df['atr'])
    df['Dn'] = df['hl2'] + (factor * df['atr'])
    
    # Trend Tracking (requires iterative calculation)
    df['TrendUp'] = df['Up'].copy()
    df['TrendDown'] = df['Dn'].copy()
    df['Trend'] = 1  # Default to bullish
    
    # Vectorized trend calculation
    cond_up = df['close'].shift(1) > df['TrendUp'].shift(1)
    df['TrendUp'] = np.where(cond_up, 
                        np.maximum(df['Up'], df['TrendUp'].shift(1)), 
                        df['Up'])
    
    cond_down = df['close'].shift(1) < df['TrendDown'].shift(1)
    df['TrendDown'] = np.where(cond_down, 
                            np.minimum(df['Dn'], df['TrendDown'].shift(1)), 
                            df['Dn'])
    
    # Vectorized trend logic
    df['Trend'] = np.select(
        [
            df['close'] > df['TrendDown'].shift(1),
            df['close'] < df['TrendUp'].shift(1)
        ],
        [1, -1],
        default=df['Trend'].shift(1))
    # Generate Signals
    df['MACD'] = np.where(df['Trend'] == 1, df['TrendUp'], df['TrendDown'])
    df['signal1'] = 0
    
    # Buy Signal: Price crosses above MACD line
    #df.loc[(df['close'] > df['MACD']) | (df['close'].shift() <= df['MACD'].shift()), 'signal1'] = 1
    df.loc[(df['close'] > df['MACD']), 'signal1'] = 1
    
    # Sell Signal: Price crosses below MACD line
    #df.loc[(df['close'] < df['MACD']) | (df['close'].shift() >= df['MACD'].shift()), 'signal1'] = -1
    df.loc[(df['close'] < df['MACD']), 'signal1'] = -1
    
    return df

def calculate_qqe_signals(df, rsi_length=8, smooth=6, bb_length=50, bb_mult=0.5):

    """
    Generates QQE signals: 1 (blue), -1 (red), 0 (gray)
    """
    # Calculate RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(rsi_length).mean()
    avg_loss = loss.rolling(rsi_length).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Smooth RSI with EMA
    df['SmoothedRSI'] = df['RSI'].ewm(span=smooth).mean()
    
    # Adjust RSI to oscillate around 0 (subtract 50)
    df['RSI_Adjusted'] = df['SmoothedRSI'] - 50
    
    # Bollinger Bands on Adjusted RSI
    df['Basis'] = df['RSI_Adjusted'].rolling(bb_length).mean()
    df['Dev'] = bb_mult * df['RSI_Adjusted'].rolling(bb_length).std()
    df['Upper'] = df['Basis'] + df['Dev']
    df['Lower'] = df['Basis'] - df['Dev']
    
    # Generate Signals
    df['Signal2'] = 0
    df.loc[df['RSI_Adjusted'] > df['Upper'], 'Signal2'] = 1     # Blue
    df.loc[df['RSI_Adjusted'] < df['Lower'], 'Signal2'] = -1    # Red
    
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

def parabolic_sar(df, step=0.04, max_step=0.3):#(df, step=0.035, max_step=0.28)
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
    # Load your price data (example with random data)
    symbol = "EURUSD"
    timeframe = "TIMEFRAME_M15"
    num_candles = 35040
    data =  get_hist_data(symbol, timeframe,num_candles, time_till=None )
    data['ema_100'] = data['close'].ewm(span=100, adjust=False).mean()
    data = data.dropna().copy()
    
    # Calculate indicator

    data = calculate_qqe_signals(data, rsi_length=8, smooth=6, bb_length=50, bb_mult=0.5) # 200 bars ≈ 2 days
    #result1 = calculate_bands(data, length=20, distance=2.0, vol_period=100)
    data= calculate_vbm_signals(data, factor=4, pd=14)
    data['volatility'] = calculate_volatility(data, 34, 2.4)
        #print(data['volatility'].tail(20))
    data['sar'] = parabolic_sar(data, step=0.02, max_step=0.2)
    # data['signal1'] = result2['signal1']
    # data['signal2'] = result1['signal2']
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
            if ((data.iloc[i]['signal1']==1)  &  (data.iloc[i]['Signal2']==1) #& (data.iloc[i]['sydney_active'] | data.iloc[i]['newyork_active']) 
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
        
            elif ((data.iloc[i]['signal1']==-1)  &  (data.iloc[i]['Signal2']==-1) #& (data.iloc[i]['sydney_active'] | data.iloc[i]['newyork_active'])
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
