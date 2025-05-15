import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np
import datetime as dt
import pytz
from pandas import Series
import time
from Email_generation import send_email
#from Get_position_size import get_pos_size
from market_structure_breakout import parabolic_sar,calculate_volatility, MACD, calculate_heikin_ashi,calculate_atr_trailing, generate_signals,calculate_zigzag, detect_msb
import os
from openpyxl import Workbook


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

cumulative_pnl = []
weekly_trades = []
PROFIT_TARGET = 1000    # Set your desired profit target in account currency
LOSS_LIMIT = -500       # Set your maximum acceptable loss in account currency
MAX_HOLD_TIME = timedelta(hours=24)  # 24-hour maximum holding period
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
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s").dt.tz_localize('UTC').dt.tz_convert(tz)
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df



#_____________________________________________________________________________________________________________________________________________________________________


#________________________________________________________________________________________________________________________________________________
# Add this function anywhere in the utilities section
def generate_weekly_report():
    global weekly_trades
    if not weekly_trades:
        return None
    
    # Create DataFrame
    report_df = pd.DataFrame(weekly_trades)
    
    # Calculate duration
    report_df['duration'] = report_df['close_time'] - report_df['open_time']
    
    # Format columns
    numeric_cols = ['open_price', 'close_price', 'sl', 'tp', 'pnl']
    report_df[numeric_cols] = report_df[numeric_cols].round(5)
    
    # Create filename with week number
    now = datetime.now(tz)
    week_num = now.isocalendar()[1]
    filename = f"Weekly_Trade_Report_Week_{week_num}.xlsx"
    filepath = os.path.join(os.getcwd(), filename)
    
    # Save to Excel with formatting
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        report_df.to_excel(writer, index=False)
        
        # Access worksheet and apply formatting
        worksheet = writer.sheets['Sheet1']
        for column in ['D', 'E', 'F', 'G', 'H']:
            worksheet.column_dimensions[column].width = 15
            
    return filepath


#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________________________________
#TECHNICAL UTILITIES WE ARE GOING TO USE FOR THE STRATEGY BACK-TESTING


def get_pip(symbol):
    return 10*mt5.symbol_info(symbol).point  


def place_bracket_order(symbol,vol,buy_sell,sl_price,tp_price):
    # Ensure symbol is selected in Market Watch
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to add {symbol} to Market Watch")
        return None
    
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        print(f"Symbol info not found for {symbol}")
        return None

    # Handle missing stops_level attribute
    # if not hasattr(symbol_info, 'stops_level'):
    #     print(f"Warning: stops_level not available for {symbol}, using default 10 pips")
    #     stops_level = 15  # Default to 10 pips if attribute missing
    # else:
    #     stops_level = symbol_info.stops_level
    
    # # Calculate min_stop using stops_level
    # point = symbol_info.point
    # min_stop = stops_level * point
    
    digits = symbol_info.digits
    sl_price = round(sl_price, digits)
    tp_price = round(tp_price, digits)
    
    
    current_price = mt5.symbol_info_tick(symbol).ask if buy_sell == "Buy" else mt5.symbol_info_tick(symbol).bid
    price = round(current_price, digits)
    
    if buy_sell == "Buy":
        # if (price - sl_price) < min_stop:
        #     print(f"Buy SL too close! Required distance: {min_stop} Current: {price - sl_price}")
        #     return None
        direction = mt5.ORDER_TYPE_BUY
    else:
        # if (sl_price - price) < min_stop:
        #     print(f"Sell SL too close! Required distance: {min_stop} Current: {sl_price - price}")
        #     return None
        direction = mt5.ORDER_TYPE_SELL
    # if buy_sell.capitalize()[0] == "B":
    #     direction = mt5.ORDER_TYPE_BUY
    #     price = mt5.symbol_info_tick(symbol).ask

    # else:
    #     direction = mt5.ORDER_TYPE_SELL
    #     price = mt5.symbol_info_tick(symbol).bid

    
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
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: {result.comment}")
        print(mt5.last_error())
    return result


def close_position(symbol,ticket=None):
    return mt5.Close(symbol,ticket=ticket)

def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s").dt.tz_localize('UTC').dt.tz_convert(tz)
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
        if data.iloc[-2,hstgrm_index] > 0 and data.iloc[-3,hstgrm_index] > 0 and data.iloc[-2,buy_signal_index] == True  and\
            data.iloc[-2,signal_index] == 1 and data.iloc[-2,ha_color] == 'green': #-2 refers to the last completed candle because in all likelihood the last candle in ohlc dataframe would be an unfinished candle.
            signal = "Buy"
        elif data.iloc[-2,hstgrm_index] < 0 and data.iloc[-3,hstgrm_index] < 0 and data.iloc[-2,sell_signal_index] == True  and\
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

def get_pip_value1(symbol, lot_size=100000):
    """Calculate the value of 1 pip in USD for a given symbol"""
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise ValueError(f"Symbol {symbol} not found")
    
    # Get basic price information
    point = symbol_info.point
    pip_size = 10 * point  # 1 pip = 10 points
    quote_currency = symbol[3:]  # Last 3 letters = quote currency
    
    # Calculate pip value in quote currency
    pip_value_quote = pip_size * lot_size  # Value per standard lot
    
    if quote_currency == "USD":
        return pip_value_quote
    
    # Find conversion rate to USD
    conversion_symbol = f"{quote_currency}USD"
    conversion_symbol_info = mt5.symbol_info(conversion_symbol)
    
    if not conversion_symbol_info:
        # Try inverse pair (e.g., USDJPY instead of JPYUSD)
        conversion_symbol = f"USD{quote_currency}"
        conversion_symbol_info = mt5.symbol_info(conversion_symbol)
        if not conversion_symbol_info:
            raise ValueError(f"Cannot find conversion pair for {quote_currency}")
        
        conversion_rate = mt5.symbol_info_tick(conversion_symbol).ask
        return pip_value_quote / conversion_rate  # Convert via inverse pair
    
    conversion_rate = mt5.symbol_info_tick(conversion_symbol).ask
    return pip_value_quote * conversion_rate

def get_pos_size2(symbol, risk_amount, stop_loss_pips):
    """
    Calculate position size based on risk parameters
    :param symbol: Trading symbol (e.g., "EURUSD")
    :param risk_amount: Maximum risk amount in USD (e.g., 10)
    :param stop_loss_pips: Stop loss distance in pips (e.g., 80)
    :return: Position size in lots
    """
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        raise ValueError(f"Symbol {symbol} not found")
    
    # Calculate pip value in USD for 1 standard lot
    pip_value_per_lot = get_pip_value1(symbol)
    
    # Calculate risk per standard lot
    risk_per_lot = stop_loss_pips * pip_value_per_lot
    
    # Handle potential division by zero
    if risk_per_lot <= 0:
        raise ValueError("Invalid risk calculation - check stop loss parameters")
    
    # Calculate raw position size
    raw_position_size = risk_amount / risk_per_lot
    
    # Round to broker's allowed lot steps
    volume_step = symbol_info.volume_step
    position_size = round(raw_position_size / volume_step) * volume_step
    
    # Ensure position size stays within broker limits
    position_size = max(position_size, symbol_info.volume_min)
    position_size = min(position_size, symbol_info.volume_max)
    
    return position_size


def main(symbol):
    hist_timeframe = params.loc[params.Symbol==symbol,"backtest_timeframe15M"].to_list()[0]
    
    try:
        # Single data fetch at beginning
        data1 = get_hist_data_numeric_index(symbol, hist_timeframe)
        
        # Calculate all indicators once
        ha_data = calculate_heikin_ashi(data1)
        data1[['ha_open', 'ha_close', 'color']] = ha_data[['ha_open', 'ha_close', 'color']]
        data1[["macd","signalm","histogram"]] = MACD(data1)
        data1['trailing_stop'] = calculate_atr_trailing(data1)
        data1['ema1'] = data1['close'].ewm(span=1).mean()
        data1['buy_signal'] = (data1['close'] > data1['trailing_stop']) & (data1['ema1'] > data1['trailing_stop'])
        data1['sell_signal'] = (data1['close'] < data1['trailing_stop']) & (data1['ema1'] < data1['trailing_stop'])
        data1['zigzag'] = calculate_zigzag(data1)
        msb_lines = detect_msb(data1, data1['zigzag'])
        data1 = generate_signals(data1, msb_lines)
        data1['volatility'] = calculate_volatility(data1, 34, 2.4)
        data1['sar'] = parabolic_sar(data1,step=0.04, max_step=0.3)
        current_sar = data1.iloc[-1]['sar']

        open_pos = get_position_df()
        
        long_short = ""
        signal = ""
        #pos_size = get_pos_size(symbol)
        atr = data1['volatility'] / get_pip(symbol)
        
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
            signal = trade_signal(data1, long_short)


        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            print(f"Symbol info not found for {symbol}")
            return
        
        # Calculate minimum stop distance in pips
        stops_level = symbol_info.stops_level if hasattr(symbol_info, 'stops_level') else 15
        point = symbol_info.point
        min_stop_pips = (stops_level * point) / get_pip(symbol)  # Convert to pips

        # [Existing position management code...]

        # Order execution logic with adjusted stop-loss
        if signal == "Buy":
            current_price = mt5.symbol_info_tick(symbol).ask
            sl_pips = max(1.5 * atr.iloc[-2], min_stop_pips)  # Ensure minimum stop
            Bsl_pips = current_price - sl_pips * get_pip(symbol)
            Btp_pips = current_price + 3.0 * atr.iloc[-2] * get_pip(symbol)
            stop_loss_pips = (current_price - Bsl_pips)/get_pip(symbol)
            pos_size = get_pos_size2(symbol, 10, stop_loss_pips)
            place_bracket_order(symbol, pos_size, signal, Bsl_pips, Btp_pips)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                order = mt5.orders_get(ticket=result.order)[0]
                weekly_trades.append({
                    'ticket': order.ticket,
                    'symbol': symbol,
                    'type': signal,
                    'lot_size': order.volume,
                    'open_time': order.time_setup,
                    'open_price': order.price_open,
                    'sl': order.sl,
                    'tp': order.tp,
                    'close_time': None,
                    'close_price': None,
                    'pnl': None,
                    'close_type': None
                })
            # ... (rest of buy logic)
            print("{}: New {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), signal, symbol))
            send_email("{}: New {} position initiated for {}".format(dt.datetime.now(), signal, symbol))


        elif signal == "Sell":
            current_price = mt5.symbol_info_tick(symbol).bid
            sl_pips = max(1.5 * atr.iloc[-2], min_stop_pips)  # Ensure minimum stop
            Ssl_pips = current_price + sl_pips * get_pip(symbol)
            Stp_pips = current_price - 3.0 * atr.iloc[-2] * get_pip(symbol)
            stop_loss_pips1 = (Ssl_pips - current_price)/get_pip(symbol)
            pos_size1 = get_pos_size2(symbol, 15, stop_loss_pips1)
            place_bracket_order(symbol, pos_size1, signal, Ssl_pips, Stp_pips)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                order = mt5.orders_get(ticket=result.order)[0]
                weekly_trades.append({
                    'ticket': order.ticket,
                    'symbol': symbol,
                    'type': signal,
                    'lot_size': order.volume,
                    'open_time': order.time_setup,
                    'open_price': order.price_open,
                    'sl': order.sl,
                    'tp': order.tp,
                    'close_time': None,
                    'close_price': None,
                    'pnl': None,
                    'close_type': None
                })
            # ... (rest of sell logic)
            print("{}: New {} position initiated for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), signal, symbol))
            send_email("{}: New {} position initiated for {}".format(dt.datetime.now(), signal, symbol))

        # Order execution logic
        elif signal == "Close":
            # ... (existing close logic)
            result = close_position(symbol)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                closed_pos = mt5.positions_get(ticket=result.order)
                if closed_pos:
                    pos = closed_pos[0]
                    profit = pos[0].profit
                    cumulative_pnl.append(profit)
                    # Update trade record
                    trade = next((t for t in weekly_trades if t['ticket'] == pos.ticket), None)
                    if trade:
                        trade.update({
                            'close_time': pos.time,
                            'close_price': pos.price_current,
                            'pnl': profit,
                            'close_type': 'Time Exit' if hold_duration >= MAX_HOLD_TIME else 'Strategy Exit'
                        })
                    print(f"Closed position P&L: {profit} | Running Total: {sum(cumulative_pnl)}")
            print("{}: Existing {} position closed for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), long_short, symbol))
            send_email("{}: Existing {} position closed for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), long_short, symbol))
            print(f"{datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')}: Position closed for {symbol} (Reason: {'Time Exit' if hold_duration >= MAX_HOLD_TIME else 'Strategy Exit'})")
            send_email(f"{datetime.now(tz)}: Position closed for {symbol} (Reason: {'Time Exit' if hold_duration >= MAX_HOLD_TIME else 'Strategy Exit'})")

    except Exception as e:
        print(e)
        send_email(f"At {dt.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")} Error for {symbol}: {str(e)}")
        #send_email("{}: Error received for {}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),symbol))

"""
if __name__ == "__main__":
    # Continuous execution  
    tz = pytz.timezone("Europe/Kyiv")  
    starttime = time.time()
    timeout = time.time() + 60*60*24*5  
    params["passthrough"] = 0
    
    while time.time() <= timeout and dt.datetime.now(tz=tz).weekday() in [0,1,2,3,4]:
        try:
            # Get current timestamp at loop start
            current_time = time.time()  # <-- NEW: Track current time
            
            print("passthrough at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time)))
            
            for symbol in symbols:
                pt = params.loc[params.Symbol==symbol,"passthrough"].to_list()[0]
                tf = params.loc[params.Symbol==symbol,"backtest_timeframe15M"].to_list()[0]
                
                # Calculate interval based on timeframe
                interval = {
                    "TIMEFRAME_H4": 14400,
                    "TIMEFRAME_H1": 3600,
                    "TIMEFRAME_M30": 1800,
                    "TIMEFRAME_M15": 900,
                    "TIMEFRAME_M5": 300
                }[tf]  # <-- NEW: Dynamic interval mapping
                
                # Check if enough time has passed since last execution
                if (current_time - starttime) // interval == pt:  # <-- Uses current_time instead of time.time()
                    print(f"starting passthrough for: {symbol}")
                    main(symbol)
                    params.loc[params.Symbol==symbol,"passthrough"] +=1
            
            if check_pnl_threshold():
                mt5.shutdown()
                break
                
            # Align sleep to next 15-minute mark (wall-clock time)
            sleep_time = 900 - (current_time % 900)  # <-- FIX: Use current_time, not elapsed
            print(f"Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)  # <-- Now perfectly aligns to :00, :15, :30, :45
            
        except KeyboardInterrupt:
            print('\n\nKeyboard exception received. Exiting.')
            exit()
"""

#============================================================================================================================

#To close the market when its weekend/ch
def market_is_closed(tz):
    now = datetime.now(tz)
    
    # Weekend check (Saturday=5, Sunday=6)
    if now.weekday() >= 5:
        return True
    
    # Holiday check (example: Christmas Day)
    if now.month == 12 and now.day == 25:
        return True
    
    # Session hours check (e.g., FX market closed 21:00-21:15 daily)
    if dt.time(21, 0) <= now.time() < dt.time(21, 15):
        return True
    
    return False

def is_near_weekly_close(tz):
    """Check if current time is 5 minutes before weekly market close"""
    now = datetime.now(tz)
    return (
        now.weekday() == 4 and  # Friday
        now.hour == 20 and      # 20:55-21:00 Kyiv time
        now.minute >= 55
    )

def close_all_positions():
    """Close all open positions"""
    positions = mt5.positions_get()
    if len(positions) > 0:
        print(f"{datetime.now(tz)}: Closing all positions before market close")
        send_email("Closing all positions before weekly market closure")
        
        for pos in positions:
            close_position(pos.symbol, pos.ticket)
            if pos.profit != 0:
                cumulative_pnl.append(pos.profit)
        send_email(f"This week cumulative profit or loss is{cumulative_pnl} ")
        # Update trade record
        trade = next((t for t in weekly_trades if t['ticket'] == pos.ticket), None)
        if trade and trade['close_time'] is None:
            trade.update({
                'close_time': pos.time,
                'close_price': pos.price_current,
                'pnl': pos.profit,
                'close_type': 'Weekly Close'
            })
            
        # Generate and send report
        report_path = generate_weekly_report()
        if report_path:
            send_email("Weekly Trade Report", attachments=[report_path])
            os.remove(report_path)  # Clean up file after sending
            
        send_email(f"This week cumulative P&L: {sum([t['pnl'] for t in weekly_trades if t['pnl'] is not None])}")
        weekly_trades = []
    else:
        print("No positions to close")
        send_email("No positions to close")
        send_email(f"This week cumulative profit or loss is{cumulative_pnl} ")
        # Generate and send report
        report_path = generate_weekly_report()
        if report_path:
            send_email("Weekly Trade Report", attachments=[report_path])
            os.remove(report_path)  # Clean up file after sending
            
        send_email(f"This week cumulative P&L: {sum([t['pnl'] for t in weekly_trades if t['pnl'] is not None])}")
        weekly_trades = []

def calculate_sleep_duration(tz):
    """Returns seconds until market reopens"""
    now = datetime.now(tz)
    
    # 1. Daily maintenance break (21:00-21:15)
    if dt.time(21, 0) <= now.time() < dt.time(21, 15):
        next_open = now.replace(hour=21, minute=15, second=0, microsecond=0)
        return max((next_open - now).total_seconds(), 0)
    
    # 2. Christmas holiday
    if now.month == 12 and now.day == 25:
        next_day = now.replace(hour=0, minute=0, second=0) + timedelta(days=1)
        return max((next_day - now).total_seconds(), 0)
    
    # 3. Weekend closure
    if now.weekday() >= 5:  # Saturday or Sunday
        next_monday = now + timedelta(days=(7 - now.weekday()))
        next_monday = next_monday.replace(hour=0, minute=0, second=0)
        return max((next_monday - now).total_seconds(), 0)
    
    # Market is open now (shouldn't reach here if market_is_closed=True)
    return 0

if __name__ == "__main__":
    # Continuous execution  
    tz = pytz.timezone("Europe/Kyiv")  
    starttime = time.time()
    timeout = time.time() + 60*60*24*5  
    params["passthrough"] = 0
    #time.time() <= timeout and dt.datetime.now(tz=tz).weekday() in [0,1,2,3,4]
    kyiv_tz = pytz.timezone('Europe/Kyiv')
    
    while True:
        # if time.time() > timeout:  # Global timeout first
        #     print("Maximum runtime reached")
        #     break
        if is_near_weekly_close(kyiv_tz):
            close_all_positions()
            # Sleep through market closure period
            continue
        
        if market_is_closed(kyiv_tz):
            sleep_sec = calculate_sleep_duration(kyiv_tz)
            print(f"Market closed. Sleeping {sleep_sec//3600} hours")
            time.sleep(sleep_sec)
            continue
        
        try:
            print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            current_time = time.time()  # <-- NEW LINE 1: Capture current timestamp
            
            for symbol in symbols:
                pt = params.loc[params.Symbol==symbol,"passthrough"].to_list()[0]
                tf = params.loc[params.Symbol==symbol,"backtest_timeframe15M"].to_list()[0]
                
                # CHANGED LINE: Use current_time instead of time.time() in calculations
                elapsed_since_start = current_time - starttime  
                
                if (elapsed_since_start) // 14400 == pt and tf =="TIMEFRAME_H4":
                    print("starting passthrough for: ",symbol)
                    main(symbol)
                    params.loc[params.Symbol==symbol,"passthrough"] +=1
                elif (elapsed_since_start) // 3600 == pt and tf =="TIMEFRAME_H1":
                    print("starting passthrough for: ",symbol)
                    main(symbol)
                    params.loc[params.Symbol==symbol,"passthrough"] +=1
                elif (elapsed_since_start) // 1800 == pt and tf =="TIMEFRAME_M30":
                    print("starting passthrough for: ",symbol)
                    main(symbol)
                    params.loc[params.Symbol==symbol,"passthrough"] +=1 
                elif (elapsed_since_start) // 900 == pt and tf =="TIMEFRAME_M15":
                    print("starting passthrough for: ",symbol)
                    main(symbol)
                    params.loc[params.Symbol==symbol,"passthrough"] +=1
                elif (elapsed_since_start) // 300 == pt and tf =="TIMEFRAME_M5":
                    print("starting passthrough for: ",symbol)
                    main(symbol)
                    params.loc[params.Symbol==symbol,"passthrough"] +=1 
            
            if check_pnl_threshold():
                mt5.shutdown()
                break
                
            
            # CHANGED LINE 2: Align sleep to wall-clock 15-minute marks
            time.sleep(900 - (current_time % 900))  # Exact 15-minute alignment

        except KeyboardInterrupt:
            print('\n\nKeyboard exception received. Exiting.')
            exit()
