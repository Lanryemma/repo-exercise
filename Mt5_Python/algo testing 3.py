import MetaTrader5 as mt5
import os
import datetime as dt 
import pandas as pd #This is used to put our data in an organized format/frame
import pytz

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


#we are gonna use api to request/extract historical data
Hist_data = mt5.copy_rates_from("EURUSD",mt5.TIMEFRAME_M15,dt.datetime(2025,2, 15 ),100) # mt5.copy_rates_from(symbol,timeframe,date_from,count)
#print(Hist_data)
Data_Hist = pd.DataFrame(Hist_data)
print(Data_Hist)

#to convert the time column elements to Datetime format
pd.to_datetime(Data_Hist.time, unit = "s") #this is because the time on the "Data_Hist" table is in seconds
#now we would override the time column on the "Data_Hist" table
Data_Hist.time = pd.to_datetime(Data_Hist.time, unit = "s")
print(Data_Hist)

#to set the time column as the index 
Data_Hist.set_index("time",inplace=True)


#Function to extract historical data
# establish MetaTrader 5 connection to a specified trading account
#extract historical data
"""def get_hist_data(symbol, timeframe, time_till=None, num_candles=200):
    
    Parameters
    ----------
    symbol : TYPE str - e.g "USDCAD"
    timeframe : TYPE str - e.g. "TIMEFRAME_M15"
    time_till : TYPE str -e.g. "YYYY-MM-DD HH:MM:SS"
    num_candles : TYPE int

    Returns
    -------
    historical data dataframe"

    if time_till == None:
        time_till = dt.datetime.now()
    else:
        # we use "strptime"when we want to convert string-input to time 
        # and "strftime" when its digit input
        time_till = dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")
    
    hist_data = mt5.copy_rates_from(symbol, getattr(mt5, timeframe), time_till, num_candles)   
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df

print(get_hist_data("USDCAD", "TIMEFRAME_M30")) #get data till current time"""


#_________________________________________________________________________________________________________________________
#since the last function we created gave us data in the 
def get_hist_data1(symbol, timeframe, time_till=None, num_candles=200):
    """
    Parameters
    ----------
    symbol : TYPE str - e.g "USDCAD"
    timeframe : TYPE str - e.g. "TIMEFRAME_M15"
    time_till : TYPE str -e.g. "YYYY-MM-DD HH:MM:SS"
    num_candles : TYPE int

    Returns
    -------
    historical data dataframe"""
    
    current_time_zone = pytz.timezone("Africa/Lagos")
    eet_tz = pytz.timezone("Europe/Kyiv")
    data_time_zone = pytz.timezone("Etc/UTC")
    if time_till == None:
        #if we print the present time it will give us the ETC time and we want our current location timezone
        #time_till = dt.datetime.now()
        time_till = current_time_zone.localize(dt.datetime.now()).replace(tzinfo= data_time_zone)
        
        
    else:
        # we use "strptime"when we want to convert string-input to time 
        # and "strftime" when its digit input
        #time_till = dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")
        time_till = eet_tz.localize(dt.datetime.strptime(time_till, "%Y-%m-%d %H:%M:%S")).replace(tzinfo=data_time_zone)
    
    
    hist_data = mt5.copy_rates_from(symbol, getattr(mt5, timeframe), time_till, num_candles)   
    hist_data_df = pd.DataFrame(hist_data) 
    hist_data_df.time = pd.to_datetime(hist_data_df.time, unit="s")
    hist_data_df.set_index("time", inplace=True)
    return hist_data_df
#print(pytz.all_timezones)
hist_data = get_hist_data1("USDJPY", "TIMEFRAME_M30") #get data till current time
index = hist_data.index
hist_data2 = get_hist_data1("USDJPY", "TIMEFRAME_M30", dt.datetime.strftime(index[1], "%Y-%m-%d %H:%M:%S")) #get data till a specified time
print(hist_data)
print(hist_data2)



#_____________________________________________________________________________________________________________________________________________
def get_hist_data_numeric_index(symbol, timeframe, start_pos=0, num_candles=200):
    #The numbering of bars goes from present to past. Thus, 
    # the zero bar means the current one. Required unnamed parameter.
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

hist1_data = get_hist_data_numeric_index("USDCAD", "TIMEFRAME_M30") #get data till current time
print(hist1_data)


