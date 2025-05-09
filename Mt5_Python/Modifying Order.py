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


def place_limit_order(symbol,vol,buy_sell,pips_away):
    
    pip_unit = 10*mt5.symbol_info(symbol).point
    
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY_LIMIT
        price = mt5.symbol_info_tick(symbol).ask - pips_away*pip_unit
    else:
        direction = mt5.ORDER_TYPE_SELL_LIMIT
        price = mt5.symbol_info_tick(symbol).bid + pips_away*pip_unit
        
    
    
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": vol,
        "type": direction,
        "price": price,
        "type_time": mt5.ORDER_TIME_GTC,
    }
    
    result = mt5.order_send(request)
    return result

#place_limit_order("USDCAD",1.0,"buy",40) #place limit orders

def get_orders_df():
    orders = mt5.orders_get()
    if len(orders) > 0:
        ord_df = pd.DataFrame(list(orders),columns=orders[0]._asdict().keys())
        ord_df.time_setup = pd.to_datetime(ord_df.time_setup , unit="s")
        ord_df.drop(['type_filling',"time_expiration",'time_done_msc','time_done',
                    'magic','comment', 'external_id','state','position_id', 'position_by_id', 'reason',], axis=1, inplace=True)
    else:
        ord_df = pd.DataFrame()
        
    return ord_df

orders_df = get_orders_df() #get open orders dataframe
order = orders_df.loc[orders_df.symbol=="USDCAD",:].iloc[0] #identify the specific order in the dataframe that needs to be updated
"""
orders_df.loc[orders_df.symbol=="USDCAD", :]

This filters the orders_df DataFrame, selecting only rows where the symbol column is "USDCAD".

It returns a DataFrame containing all orders for USDCAD.

.iloc[0]

.iloc[0] selects the first row (index 0) from the filtered DataFrame.

This ensures that we pick only one order (the first one available).
"""

def modify_open_order(order,price):
    request = {
        "action": mt5.TRADE_ACTION_MODIFY,
        "symbol": order.symbol,
        "order": int(order.ticket),
        "price": price
    }
    
    result = mt5.order_send(request)
    return result


modify_open_order(order,1.42864)
#i.42864