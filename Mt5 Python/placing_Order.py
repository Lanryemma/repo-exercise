import MetaTrader5 as mt5
import os
import datetime as dt 
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
def place_market_order(symbol,vol,buy_sell):
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
        "price": price,
        "type_time": mt5.ORDER_TIME_GTC,
    }
    
    result = mt5.order_send(request)
    
    #To check if the order waa palce successfully
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed! Error Code: {result.retcode if result else 'No response'}")
    else:
        print(f"Order successful! Order Ticket: {result.order}")
    
    return result

place_market_order("USDCAD",0.05,"BUY")

def place_limit_order(symbol,vol,buy_sell,pips_away):
    
    pip_unit = 10*mt5.symbol_info(symbol).point
    
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY_LIMIT
        #incase you want to use an exactly price that you saw on the chat, 
        # you can just specify, you dont need this "price = mt5.symbol_info_tick(symbol).ask - pips_away*pip_unit"
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
    
    #To check if the order waa palce successfully
    if result is None or result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed! Error Code: {result.retcode if result else 'No response'}")
    else:
        print(f"Order successful! Order Ticket: {result.order}")
    
    return result


place_limit_order("GBPUSD",0.02,"Buy",8)
"""



#______________________________________________________________________________________________________________________________
#NOW WE SHOW HOW TO PLACE ORDERS WITH STOP LOSS AND TAKE PROFIT
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


#IF WE WANT TO PLACE THE STOP-LOSS AND TAKE-PROFIT USING PIP
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
    
    
#place_bracket_order("USDCAD",0.1,"buy",1.3317,1.3347)
place_bracket_order_pip("GBPUSD",0.1,"sell",20,40)


#_________________________________________________________________________________________________________________________________
#IF WE WANT TO CLOSE THE ORDER THAT HAS ALREADY BEEN PLACED 
def close_position(symbol,ticket=None):
    return mt5.Close(symbol,ticket=ticket)

    
#close_position("GBPUSD")#This will close all the USDCAD order that is opened 
#if you want to close a specific order you have to provide the ticket number"""


"""
def check_symbol_info(symbol):
    info = mt5.symbol_info(symbol)
    if info is None:
        print(f"Symbol {symbol} not found!")
        return
    
    print(f"Symbol: {symbol}")
    print(f"Min lot: {info.volume_min}, Max lot: {info.volume_max}, Step: {info.volume_step}")

check_symbol_info("EURUSD")

account_info = mt5.account_info()
if account_info is not None:
    print(f"Trading Allowed: {account_info.trade_allowed}")
    print(f"Balance: {account_info.balance}, Free Margin: {account_info.margin_free}")
else:
    print("Failed to get account info!")
"""