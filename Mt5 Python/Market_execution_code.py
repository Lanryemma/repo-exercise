import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import datetime as dt
import pytz
import matplotlib.pyplot as plot
from pandas import Series
import time
from Stratergy_evaluation import win_rate,mean_ret_winner_pip,mean_ret_loser_pip,max_drawdown
from Email_generation import send_email


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


def get_hist_data_numeric_index(mt5, symbol, timeframe, start_pos=0, num_candles=200):
    """
    Parameters
    ----------
    symbol : TYPE str - e.g "USDCAD"
    timeframe : TYPE str - e.g. "TIMEFRAME_M15"
    start_pos : TYPE int -e.g. 0 means data till current time
    num_candles : TYPE int
    Returns
    -------
    historical data dataframe
    """
    hist_data = mt5.copy_rates_from_pos(symbol, getattr(mt5, timeframe), start_pos, num_candles)   
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL INDICATOR WE ARE GOING TO GET DATAs FOR THE STRATEGY BACK-TESTING

params = pd.read_csv("C:\\Users\\user\\Downloads\\params.csv")
symbols = params.Symbol.to_list()
print(params)

#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL UTILITIES WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING

def place_bracket_order(symbol,vol,buy_sell,sl_price,tp_price):
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask

    else:
        direction = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid

    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": vol,
        "type": direction,
        "sl": sl_price,
        "tp": tp_price,
        "price": price,
        "type_time": mt5.ORDER_TIME_GTC
    }
    
    result = mt5.order_send(request)
    return result

def close_position(symbol,ticket=None):
    return mt5.Close(symbol,ticket=ticket)

def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        pos_df.type = np.where(pos_df.type==0,1,-1)
    else:
        pos_df = pd.DataFrame()
        
    return pos_df


def trade_signal(candle_data,l_s):
    signal = ""
    macd_index = candle_data.columns.to_list().index("macd")
    
    if l_s == "":
        if candle_data.iloc[-2,macd_index]>0 and candle_data.iloc[-3,macd_index]>0 and (candle_data.iloc[-10:-3,macd_index] < 0).all(): #-2 refers to the last completed candle because in all likelihood the last candle in ohlc dataframe would be an unfinished candle.
            signal = "Buy"
        elif candle_data.iloc[-2,macd_index]<0 and candle_data.iloc[-3,macd_index]<0 and (candle_data.iloc[-10:-3,macd_index] > 0).all():
            signal = "Sell"
            
    elif l_s == "long":
        if (candle_data.iloc[-4:-1,macd_index] < 0).all():
            signal = "Close"
            
    elif l_s == "short":
        if (candle_data.iloc[-4:-1,macd_index] > 0).all():
            signal = "Close"
    
    return signal

def main(symbol):
    hist_timeframe = params.loc[params.Symbol==symbol,"backtest_timeframe"].to_list()[0]
    supp_res_timeframe = params.loc[params.Symbol==symbol,"supp_res_timeframe"].to_list()[0]
    
    try:
        open_pos = get_position_df()
        long_short = ""
        if len(open_pos) > 0:
            open_pos_cur = open_pos[open_pos.symbol==symbol]
            if len(open_pos_cur) > 0:
                if (open_pos_cur.type * open_pos_cur.volume).sum() > 0:
                    long_short = "long"
                elif (open_pos_cur.type * open_pos_cur.volume).sum() < 0:
                    long_short = "short"
                    
        ohlc = get_hist_data_numeric_index(symbol, hist_timeframe)
        ohlc[["macd","signal","histogram"]] = MACD(ohlc)
        signal = trade_signal(ohlc,long_short)
        pos_size = get_pos_size(symbol)
        
        if signal == "Buy":
            place_bracket_order(symbol,pos_size,signal,supp,res)
            print("{}: New {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), signal, symbol))
            send_email("{}: New {} position initiated for {}".format(dt.datetime.now(), signal, symbol))
            
        elif signal == "Sell":
            place_bracket_order(symbol,pos_size,signal,res,supp)
            print("{}: New {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), signal, symbol))
            send_email("{}: New {} position initiated for {}".format(dt.datetime.now(), signal, symbol))
            
        elif signal == "Close":
            close_position(symbol)
            print("{}: Existing {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), long_short, symbol))
            send_email("{}: Existing {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), long_short, symbol))
       
    except Exception as e:
        print(e)
        send_email("{}: Error received for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),symbol))
            

# Continuous execution  
tz = pytz.timezone("Europe/Kyiv") #MT5 server timezone      
starttime=time.time()
timeout = time.time() + 60*60*24*5  # Run from Monday 12:00 am to Friday 11:59 pm
params["passthrough"] = 0
while time.time() <= timeout and dt.datetime.now(tz=tz).weekday() in [0,1,2,3,4]: #weekday 0 is monday and 6 is sunday
    try:
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        for symbol in symbols:
            pt = params.loc[params.Symbol==symbol,"passthrough"].to_list()[0]
            tf = params.loc[params.Symbol==symbol,"backtest_timeframe"].to_list()[0]
            if (time.time() - starttime) // 14400 == pt and tf =="TIMEFRAME_H4":
                print("starting passthrough for: ",symbol)
                main(symbol)
                params.loc[params.Symbol==symbol,"passthrough"] +=1
            elif (time.time() - starttime) // 3600 == pt and tf =="TIMEFRAME_H1":
                print("starting passthrough for: ",symbol)
                main(symbol)
                params.loc[params.Symbol==symbol,"passthrough"] +=1
            elif (time.time() - starttime) // 1800 == pt and tf =="TIMEFRAME_M30":
                print("starting passthrough for: ",symbol)
                main(symbol)
                params.loc[params.Symbol==symbol,"passthrough"] +=1                  
        time.sleep(1800 - ((time.time() - starttime) % 1800.0)) # 30 minute interval between each new execution
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()
        
