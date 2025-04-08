# -*- coding: utf-8 -*-
"""
Technical indicators

@author: Mayank
"""
import numpy as np

def SMA(DF, n=200):
    df = DF.copy()
    df["sma"] = df["close"].rolling(n).mean()
    return df["sma"]
    

def EMA(ser, n=9):
    multiplier = 2/(n+1)    
    sma = ser.rolling(n).mean()
    ema = np.full(len(ser), np.nan)
    ema[len(sma) - len(sma.dropna())] = sma.dropna()[0]
    for i in range(len(ser)):
        if not np.isnan(ema[i-1]):
            ema[i] = ((ser.iloc[i] - ema[i-1])*multiplier) + ema[i-1]
    ema[len(sma) - len(sma.dropna())] = np.nan
    return ema

def RMA(ser, n=9):
    multiplier = 1/n    
    sma = ser.rolling(n).mean()
    ema = np.full(len(ser), np.nan)
    ema[len(sma) - len(sma.dropna())] = sma.dropna()[0]
    for i in range(len(ser)):
        if not np.isnan(ema[i-1]):
            ema[i] = ((ser.iloc[i] - ema[i-1])*multiplier) + ema[i-1]
    ema[len(sma) - len(sma.dropna())] = np.nan
    return ema

def RSI(DF, n=5):
    "function to calculate RSI"
    df = DF.copy()
    df["change"] = df["close"] - df["close"].shift(1)
    df["gain"] = np.where(df["change"]>=0, df["change"], 0)
    df["loss"] = np.where(df["change"]<0, -1*df["change"], 0)
    df["avgGain"] = RMA(df["gain"],n)
    df["avgLoss"] = RMA(df["loss"],n)
    df["rs"] = df["avgGain"]/df["avgLoss"]
    df["rsi"] = 100 - (100/ (1 + df["rs"]))
    return df["rsi"]

def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["ma_fast"] = EMA(df["close"],a)
    df["ma_slow"] = EMA(df["close"],b)
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = EMA(df["macd"],c)
    df["histogram"] = df["macd"] - df["signal"]
    return df[["macd","signal","histogram"]]

def stochastic(DF, lookback=14, k=3, d=3):
    """function to calculate Stochastic Oscillator
       lookback = lookback period
       k and d = moving average window for %K and %D"""
    df = DF.copy()
    df["HH"] = df["high"].rolling(lookback).max()
    df["LL"] = df["low"].rolling(lookback).min()
    df["%k"] = (100 * (df["close"] - df["LL"])/(df["HH"]-df["LL"])).rolling(k).mean()
    df["%d"] = df["%k"].rolling(d).mean()
    return df[["%k","%d"]]
