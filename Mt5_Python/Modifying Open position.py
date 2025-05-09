import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pandas as pd #This is used to put our data in an organized format/frame
import numpy as np

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

def place_bracket_order_pip(symbol,vol,buy_sell,sl_pip,tp_pip):
    pip_unit = 10*mt5.symbol_info(symbol).point
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
        sl = price - sl_pip*pip_unit
        tp = price + tp_pip*pip_unit

    else:
        direction = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
        sl = price + sl_pip*pip_unit
        tp = price - tp_pip*pip_unit

    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": vol,
        "type": direction,
        "sl": sl,
        "tp": tp,
        "price": price,
        "type_time": mt5.ORDER_TIME_GTC
    }
    
    result = mt5.order_send(request)
    return result
    
def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
    else:
        pos_df = pd.DataFrame()
        
    return pos_df
    
#place_bracket_order_pip("USDCAD",1.0,"buy",20,40) #place bracket orders

pos_df = get_position_df() #get position dataframe

def update_sl_tp_pos(pos,sl_new,tp_new):    
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": pos.symbol,
        "position": int(pos.ticket),
        "sl": sl_new,
        "tp": tp_new
    }
    
    result = mt5.order_send(request)
    return result
    
pos = pos_df.loc[pos_df.symbol=="USDCAD",:].iloc[0] #identify the specific position in the dataframe that needs to be updated


update_sl_tp_pos(pos,1.42972,1.43533) #update the position