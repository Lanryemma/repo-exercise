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


# Forex sessions in UTC
FOREX_SESSIONS = {
    "Sydney": {"start": 22, "end": 7},    # 10:00 PM - 7:00 AM UTC
    "Tokyo": {"start": 0, "end": 9},      # 12:00 AM - 9:00 AM UTC
    "London": {"start": 7, "end": 16},    # 7:00 AM - 4:00 PM UTC
    "New York": {"start": 12, "end": 21}  # 12:00 PM - 9:00 PM UTC
}


#
def get_active_session():
    now = datetime.now(timezone.utc)  # Get current UTC time
    current_hour = now.hour

    active_sessions = []
    
    for session, hours in FOREX_SESSIONS.items():
        if hours["start"] <= current_hour < hours["end"] or (hours["end"] < hours["start"] and (current_hour >= hours["start"] or current_hour < hours["end"])):
            active_sessions.append(session)

    return active_sessions

# Example usage
active_sessions = get_active_session()
print(f"Active Forex Sessions: {active_sessions}")


#Fetch Trading Hours for a Specific Symbol (e.g., EURUSD)
def get_trading_hours(symbol="EURUSD"):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info:
        return {
            "trading_hours": symbol_info.trade_time,
            "session_open": symbol_info.session_deals,
            "session_close": symbol_info.session_orders
        }
    else:
        return "Symbol not found"

# Example usage
trading_hours = get_trading_hours("EURUSD")
print(trading_hours)
