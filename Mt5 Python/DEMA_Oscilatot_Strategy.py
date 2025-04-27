import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import datetime as dt
import pytz
from talib import DEMA, STDDEV, SMA, ATR
import matplotlib.pyplot as plt
from Stratergy_evaluation import win_rate,mean_ret_winner_pip,mean_ret_loser_pip,max_drawdown

# ======================
# MT5 CONNECTION SETUP
# ======================
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


# ======================
# DATA FETCHING
# ======================
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


def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  

# =================================================================================
#       INDICATOR CALCULATION
# =================================================================================
def calculate_indicators(df, dema_period, base_period, atr_period):
    """Calculate all technical indicators"""
    # Price smoothing
    df['DEMA'] = DEMA(df['close'], timeperiod=dema_period)
    
    # Base calculations
    df['BASE'] = SMA(df['DEMA'], timeperiod=base_period)
    df['SD'] = STDDEV(df['DEMA'], timeperiod=base_period) * 2
    df['UpperBand'] = df['BASE'] + df['SD']
    df['LowerBand'] = df['BASE'] - df['SD']
    
    # Normalized oscillator
    df['NormBase'] = 100 * (df['DEMA'] - df['LowerBand']) / (df['UpperBand'] - df['LowerBand'])
    
    # Volatility measure
    df['ATR'] = ATR(df['high'], df['low'], df['close'], timeperiod=atr_period)
    
    return df.dropna()

# =====================================================================================
#       SIGNAL GENERATION
# =====================================================================================
def generate_signals(df, long_thresh=55, short_thresh=45):
    """Generate trading signals based on strategy rules"""
    signals = pd.DataFrame(index=df.index)
    
    # Core signal logic
    signals['Long'] = (df['NormBase'] > long_thresh) & (df['close'] > df['LowerBand'])#df['LowerBand'])
    signals['Short'] = (df['NormBase'] < short_thresh) & (df['close'] < df['UpperBand'])
    
    # State tracking
    signals['Position'] = 0
    signals.loc[signals['Long'], 'Position'] = 1
    signals.loc[signals['Short'], 'Position'] = -1
    
    return signals

# ======================
# VISUALIZATION
# ======================
def plot_results(data, signals):
    """Visualize strategy components and signals"""
    plt.figure(figsize=(15,10))
    
    # Price and bands
    plt.subplot(2,1,1)
    plt.plot(data['close'], label='Price', color='royalblue')
    plt.plot(data['DEMA'], label='DEMA', color='orange', linestyle='--')
    plt.plot(data['UpperBand'], label='Upper Band', color='gray', alpha=0.7)
    plt.plot(data['LowerBand'], label='Lower Band', color='gray', alpha=0.7)
    plt.fill_between(data.index, data['UpperBand'], data['LowerBand'], color='gray', alpha=0.1)
    plt.title('Price with DEMA and Volatility Bands')
    plt.legend()
    
    # Oscillator and signals
    plt.subplot(2,1,2)
    plt.plot(data['NormBase'], label='Normalized Oscillator', color='purple')
    plt.axhline(55, color='green', linestyle='--', alpha=0.7)
    plt.axhline(45, color='red', linestyle='--', alpha=0.7)
    plt.scatter(signals[signals['Position'] == 1].index, 
                data['NormBase'][signals['Position'] == 1], 
                marker='^', color='green', s=100, label='Long Signal')
    plt.scatter(signals[signals['Position'] == -1].index, 
                data['NormBase'][signals['Position'] == -1], 
                marker='v', color='red', s=100, label='Short Signal')
    plt.title('Normalized Oscillator with Signals')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

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


# ======================
# MAIN PROCESSING
# ======================
if __name__ == "__main__":
    
    # ======================
    # STRATEGY CONFIGURATION
    # ======================
    symbol = "AUDCHF"
    TIMEFRAME = "TIMEFRAME_M15"
    BARS_TO_FETCH = 36000
    
    # Indicator parameters
    DEMA_PERIOD = 40     # Double EMA period (original: 30)
    BASE_PERIOD = 20     # Base SMA period (original: 20)
    LONG_THRESH = 55     # Long entry threshold (original: 55)
    SHORT_THRESH = 45    # Short entry threshold (original: 45)
    ATR_PERIOD = 14      # Volatility measurement period
    
    try:
        # Fetch and process data
        data =  get_hist_data(symbol, TIMEFRAME, BARS_TO_FETCH)
        data = calculate_indicators(data,
                                dema_period=DEMA_PERIOD,
                                base_period=BASE_PERIOD,
                                atr_period=ATR_PERIOD)
        
        # Generate signals
        signals = generate_signals(data,
                                long_thresh=LONG_THRESH,
                                short_thresh=SHORT_THRESH)
        data['volatility'] = calculate_volatility(data, 34, 2.4)
        #print(data['volatility'].tail(20))
        data['sar'] = parabolic_sar(data, step=0.04, max_step=0.3)
        
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
                if (signals['Position'].iloc[i] == 1 #signals.iloc[i]['buy']      # STC above 25 = bullish momentum
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
            
                elif (signals['Position'].iloc[i] == -1 #signals.iloc[i]['sell']     # STC below 75 = bullish momentum
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
        plt.show()
        
        # Display results
        print("\nSignal Summary:")
        print(f"Total Long Signals: {sum(signals['Position'] == 1)}")
        print(f"Total Short Signals: {sum(signals['Position'] == -1)}")
        
        # Visualize
        #plot_results(data, signals)

    finally:
        mt5.shutdown()

