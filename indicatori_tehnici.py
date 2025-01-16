import pandas as pd
import pandas_ta as ta

def calculeaza_RSI(df, perioada=14):
    df['RSI'] = ta.rsi(df['Preț închidere'], length=perioada)
    return df

def calculeaza_SMA(df, perioada=20):
    df['SMA'] = ta.sma(df['Preț închidere'], length=perioada)
    return df

def calculeaza_MACD(df):
    macd = ta.macd(df['Preț închidere'])
    df['MACD'] = macd['MACD_12_26_9']
    df['Signal'] = macd['MACDs_12_26_9']
    df['Histogram'] = macd['MACDh_12_26_9']
    return df

def calculeaza_ATR(df, perioada=14):
    df['ATR'] = ta.atr(high=df['Preț maxim'], low=df['Preț minim'], close=df['Preț închidere'], length=perioada)
    return df

def calculeaza_OBV(df):
    df['OBV'] = ta.obv(close=df['Preț închidere'], volume=df['Volum'])
    return df

def calculeaza_EMA(df, perioada=9):
    df['EMA'] = ta.ema(df['Preț închidere'], length=perioada)
    return df
