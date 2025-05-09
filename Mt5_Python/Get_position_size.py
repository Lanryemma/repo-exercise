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


#get current price of a symbol
def get_current_price(symbol):
    tick_info = mt5.symbol_info_tick(symbol)
    return (tick_info.bid + tick_info.ask)/2

def usd_conversion_factor(currency):
    if currency == "USD":
        return 1
    
    currency_data = mt5.symbols_get("*{}*".format(currency))
    for symbol in currency_data:
        if symbol.name[:3] == "USD" or symbol.name[3:] == "USD":
            base_currency = symbol.name[:3]
            counter_currency = symbol.name[3:]
            break
    currency_data = mt5.symbol_info(base_currency+counter_currency)
    current_price = get_current_price(base_currency+counter_currency)
    if base_currency == "USD":
        return 1/current_price
    else:
        return current_price
   
def get_pos_size(symbol,reqd_per_pip_pnl=1,lot_size=100000):
    base_currency = symbol[:3]
    symbol_data = mt5.symbol_info(symbol)
    usd_factor = usd_conversion_factor(base_currency)
    pip = 10*symbol_data.point
    current_price = get_current_price(symbol)
    per_pip_pnl = pip/(current_price+pip)
    pos_size = reqd_per_pip_pnl/(lot_size*usd_factor*per_pip_pnl)
    return (pos_size//symbol_data.volume_step)/(1/symbol_data.volume_step)

 
pos_size = get_pos_size(symbol = "NZDUSD")  
print(pos_size)