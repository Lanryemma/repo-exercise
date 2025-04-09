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
from Get_position_size import get_pos_size
from market_structure_breakout import parabolic_sar,calculate_volatility, MACD, calculate_heikin_ashi,calculate_atr_trailing, generate_signals,calculate_zigzag, detect_msb


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

cumulative_pnl = []
PROFIT_TARGET = 1000    # Set your desired profit target in account currency
LOSS_LIMIT = -500       # Set your maximum acceptable loss in account currency
MAX_HOLD_TIME = timedelta(hours=4)  # 4-hour maximum holding period
tz = pytz.timezone("Europe/Kyiv")   # Your existing timezone definition


#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL INDICATOR WE ARE GOING TO GET DATAs FOR THE STRATEGY BACK-TESTING

params = pd.read_csv("C:\\Users\\user\\Downloads\\params.csv")
symbols = params.Symbol.to_list()
print(params)


def get_hist_data_numeric_index(symbol, timeframe, start_pos=0, num_candles=200):
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



#_____________________________________________________________________________________________________________________________________________________________________


#________________________________________________________________________________________________________________________________________________



#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL UTILITIES WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING


def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  


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




#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#THIS IS THE MAIN MARKET EXECUTION CODE
def trade_signal(data,l_s):
    signal = ""
    hstgrm_index = data.columns.to_list().index("histogram")
    signal_index = data.columns.to_list().index("signal")
    buy_signal_index = data.columns.to_list().index('buy_signal')
    sell_signal_index = data.columns.to_list().index('sell_signal')
    ha_color = data.columns.to_list().index("color")
    
    if l_s == "":
        if data.iloc[-2,hstgrm_index] > 0 and data.iloc[-2,buy_signal_index] == True  and\
            data.iloc[-2,signal_index] == 1 and data.iloc[-2,ha_color] == 'green': #-2 refers to the last completed candle because in all likelihood the last candle in ohlc dataframe would be an unfinished candle.
            signal = "Buy"
        elif data.iloc[-2,hstgrm_index] < 0 and data.iloc[-2,sell_signal_index] == True  and\
            data.iloc[-2,signal_index] == -1 and data.iloc[-2,ha_color] == 'red':
            signal = "Sell"
            
    # elif l_s == "long":
    #     if (candle_data.iloc[-4:-1,macd_index] < 0).all():
    #         signal = "Close"
            
    # elif l_s == "short":
    #     if (candle_data.iloc[-4:-1,macd_index] > 0).all():
    #         signal = "Close"
    
    return signal


# Add this function above the main trading loop
def check_pnl_threshold():
    global cumulative_pnl
    total = sum(cumulative_pnl)
    
    if total >= PROFIT_TARGET:
        print(f"Profit target reached! Total profit: {total}")
        send_email(f"Profit target achieved! Total P&L: {total}")
        return True
    elif total <= LOSS_LIMIT:
        print(f"Loss limit triggered! Total loss: {total}")
        send_email(f"Loss limit breached! Total P&L: {total}")
        return True
    return False


def main(symbol):
    hist_timeframe = params.loc[params.Symbol==symbol,"backtest_timeframe"].to_list()[0]
    
    try:
        # Single data fetch at beginning
        data = get_hist_data_numeric_index(symbol, hist_timeframe)
        
        # Calculate all indicators once
        ha_data = calculate_heikin_ashi(data)
        data[['ha_open', 'ha_close', 'color']] = ha_data[['ha_open', 'ha_close', 'color']]
        data[["macd","signal","histogram"]] = MACD(data)
        data['trailing_stop'] = calculate_atr_trailing(data)
        data['ema1'] = data['close'].ewm(span=1).mean()
        data['buy_signal'] = (data['close'] > data['trailing_stop']) & (data['ema1'] > data['trailing_stop'])
        data['sell_signal'] = (data['close'] < data['trailing_stop']) & (data['ema1'] < data['trailing_stop'])
        data['zigzag'] = calculate_zigzag(data)
        msb_lines = detect_msb(data, data['zigzag'])
        data = generate_signals(data, msb_lines)
        data['volatility'] = calculate_volatility(data, 34, 2.4)
        data['sar'] = parabolic_sar(data)
        current_sar = data.iloc[-1]['sar']

        open_pos = get_position_df()
        long_short = ""
        signal = ""
        pos_size = get_pos_size(symbol)
        atr = data['volatility'] / get_pip(symbol)
        
        # Position management
        if len(open_pos) > 0:
            open_pos_cur = open_pos[open_pos.symbol==symbol]
            if len(open_pos_cur) > 0:
                position_type = "long" if (open_pos_cur.type * open_pos_cur.volume).sum() > 0 else "short"
                long_short = position_type
                entry_time = open_pos_cur.iloc[0].time.to_pydatetime()
                current_time = datetime.now(tz)
                hold_duration = current_time - entry_time
                
                # Time-based exit check
                if hold_duration >= MAX_HOLD_TIME:
                    print(f"Time-based exit triggered for {symbol}")
                    signal = "Close"
                
                # SAR Trailing Stop Update
                ticket = open_pos_cur.iloc[0].ticket
                current_sl = open_pos_cur.iloc[0].sl
                if (position_type == "long" and current_sar > current_sl) or \
                    (position_type == "short" and current_sar < current_sl):
                    new_sl = current_sar
                    request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol": symbol,
                        "sl": new_sl,
                        "tp": open_pos_cur.iloc[0].tp,
                        "ticket": ticket
                    }
                    mt5.order_send(request)
                    print(f"Updated SL to SAR value: {new_sl}")
                    send_email(f"SAR Trailing Stop Update: {symbol} SL moved to {new_sl}")

        # Generate trading signal if no time-based exit
        if not signal:
            signal = trade_signal(data, long_short)

        # Order execution logic
        if signal == "Buy":
            Bsl_pips = data["open"].iloc[-1] - 1.5 * atr.iloc[-1]
            Btp_pips = data["open"].iloc[-1] + 3.0 * atr.iloc[-1]
            place_bracket_order(symbol, pos_size, signal, Bsl_pips, Btp_pips)
            # ... (rest of buy logic)
            print("{}: New {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), signal, symbol))
            send_email("{}: New {} position initiated for {}".format(dt.datetime.now(), signal, symbol))

        elif signal == "Sell":
            Ssl_pips = data["open"].iloc[-1] + 1.5 * atr.iloc[-1]
            Stp_pips = data["open"].iloc[-1] - 3.0 * atr.iloc[-1]
            place_bracket_order(symbol, pos_size, signal, Ssl_pips, Stp_pips)
            # ... (rest of sell logic)
            print("{}: New {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), signal, symbol))
            send_email("{}: New {} position initiated for {}".format(dt.datetime.now(), signal, symbol))

        elif signal == "Close":
            # ... (existing close logic)
            result = close_position(symbol)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                closed_pos = mt5.positions_get(ticket=result.order)
                if closed_pos:
                    profit = closed_pos[0].profit
                    cumulative_pnl.append(profit)
                    print(f"Closed position P&L: {profit} | Running Total: {sum(cumulative_pnl)}")
            print("{}: Existing {} position closed for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), long_short, symbol))
            send_email("{}: Existing {} position closed for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), long_short, symbol))
            print(f"{datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}: Position closed for {symbol} (Reason: {'Time Exit' if hold_duration >= MAX_HOLD_TIME else 'Strategy Exit'})")
            send_email(f"{datetime.now(tz)}: Position closed for {symbol} (Reason: {'Time Exit' if hold_duration >= MAX_HOLD_TIME else 'Strategy Exit'})")

    except Exception as e:
        print(e)
        send_email(f"At{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Error for {symbol}: {str(e)}")
        #send_email("{}: Error received for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),symbol))

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
            tf = params.loc[params.Symbol==symbol,"backtest_timeframe15M"].to_list()[0]
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
            elif (time.time() - starttime) // 900 == pt and tf =="TIMEFRAME_M15":
                print("starting passthrough for: ",symbol)
                main(symbol)
                params.loc[params.Symbol==symbol,"passthrough"] +=1
            elif (time.time() - starttime) // 300 == pt and tf =="TIMEFRAME_M5":
                print("starting passthrough for: ",symbol)
                main(symbol)
                params.loc[params.Symbol==symbol,"passthrough"] +=1 
        if check_pnl_threshold():
            mt5.shutdown()
            break
        time.sleep(1800 - ((time.time() - starttime) % 1800.0)) # 30 minute interval between each new execution
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()
        
