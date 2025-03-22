import MetaTrader5 as mt5
import os
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

# get all symbols
symbols=mt5.symbols_get()
print('Symbols: ', len(symbols))
print(symbols[0])

# get all symbols with "EUR"
symbols1=mt5.symbols_get("*EUR*")
print('Symbols: ', len(symbols1))
print(symbols1[0].name)

# get all symbols where "EUR" is the base currency pair
#symbols1=mt5.symbols_get("EUR*")
# get all symbols where "EUR" is the counterfeit pair
symbols2=mt5.symbols_get("*EUR")
print('Symbols: ', len(symbols2))
print(symbols2[0].name)


#we can call and get the bid and ask price
symbols=mt5.symbols_get()
print('Symbols: ', len(symbols))

for symbol in symbols:
    print(f"{symbol.name}:-- ask-price:{symbol.ask}  bid-price:{symbol.bid}")
    #print(f"{symbol.name}")


#_______________________________________________________________________________________________________________________________________
#get same information as above but for a specific symbol  
info = mt5.symbol_info("EURGBP")
#print(info)        


#get current price of a symbol
def get_current_price(symboll):
    #to add the typed/input currency pair to the watch list
    selected=mt5.symbol_select(symboll,True)
    if not selected:
        print("Failed to select symbol, error code =",mt5.last_error())
        return False
    else:
        tick_info = mt5.symbol_info_tick(symboll)
        return (tick_info.bid + tick_info.ask)/2

print(get_current_price("AUDJPY"))


#get current pip point of a symbol
def get_pip(symbol):
    #to add the typed/input currency pair to the watch list
    selected1=mt5.symbol_select(symbol,True)
    if not selected1:
        print("Failed to select symbol, error code =",mt5.last_error())
        return False
    else:
        pip_info = mt5.symbol_info(symbol)
        return pip_info.point

print(get_pip("NZDJPY"))


#________________________________________________________________________________________________________________________________________________
#no we would explore how to request account information
acc_info = mt5.account_info()

#print(acc_info)
#to get the free margin in the account
def free_margin():
    fmargin = mt5.account_info().margin_free
    print(fmargin)


def info_acc():
    Acc_det = mt5.account_info()
    return {"Balance":Acc_det.balance,
            "Equity":Acc_det.equity,
            "Margin":Acc_det.margin,
            "Free-margin":Acc_det.margin_free}
"""Acc_component = {"Balance":Acc_det.balance,
                    "Equity":Acc_det.equity,
                    "Margin":Acc_det.margin,
                    "Free-margin":Acc_det.margin_free}
    for com in Acc_component:
        return Acc_component.get(com)"""

free_margin()
print(info_acc())

#_____________________________________________________________________________________________________________________________
#This program is to find position per lot size
# Ensure the symbol is in the market watch
def get_pos_size(symbol, req_pip_pnl=10, lot=100000):
    if mt5.symbol_info(symbol) is None:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to add {symbol} to market watch list")
            return None
    
    # Get pip value in account currency
    pip_value = mt5.symbol_info(symbol).point * lot
            
    if pip_value == 0:
        print(f"Error: Invalid pip value for {symbol}")
        return None

    # Calculate position size
    pos_size = (req_pip_pnl / pip_value) * lot
            
    #mt5.shutdown()
            
    return pos_size

# Example Usage
print("Optimal Position Size:", get_pos_size("EURUSD"))
