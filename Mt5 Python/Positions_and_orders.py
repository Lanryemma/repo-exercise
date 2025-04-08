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

"""
def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
    else:
        pos_df = pd.DataFrame()
        
    return pos_df
"""

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

print(get_orders_df())

#incase you want it to display the table in your browser
"""
web_Order = ord_df.to_html("orders.html")
import webbrowser
webbrowser.open("orders.html")
return web_Order
"""
