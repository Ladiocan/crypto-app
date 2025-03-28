import os
import pandas as pd
import pandas_ta as ta

# Directorul cu fișierele CSV actualizate
DIRECTOR_CSV = "crypto_data"

def calculeaza_indicatori_pentru_fisier(fisier):
    """
    Calculează indicatorii tehnici pentru un fișier CSV și salvează rezultatul.
    """
    try:
        # Citește datele din fișier
        df = pd.read_csv(fisier)

        # Calculează indicatorii
        df = calculeaza_RSI(df)
        df = calculeaza_SMA(df)
        df = calculeaza_MACD(df)
        df = calculeaza_ATR(df)
        df = calculeaza_OBV(df)
        df = calculeaza_EMA(df)

        # Salvează datele actualizate
        fisier_salveaza = os.path.join(DIRECTOR_CSV, f"indicatori_{os.path.basename(fisier)}")
        df.to_csv(fisier_salveaza, index=False)
        print(f"Indicatorii pentru {fisier} au fost salvați în {fisier_salveaza}.")
    except Exception as e:
        print(f"Eroare la procesarea fișierului {fisier}: {e}")

def calculeaza_indicatori_pentru_toate():
    """
    Calculează indicatorii tehnici pentru toate fișierele din directorul `crypto_data`.
    """
    for fisier in os.listdir(DIRECTOR_CSV):
        if fisier.endswith(".csv"):
            cale_fisier = os.path.join(DIRECTOR_CSV, fisier)
            calculeaza_indicatori_pentru_fisier(cale_fisier)

# Funcțiile pentru indicatori individuali
def calculeaza_RSI(df, perioada=14):
    try:
        df['RSI'] = ta.rsi(df['Preț închidere'], length=perioada)
    except Exception as e:
        print(f"Eroare la calcularea RSI: {e}")
        df['RSI'] = None
    return df

def calculeaza_SMA(df, perioada=20):
    try:
        df['SMA'] = ta.sma(df['Preț închidere'], length=perioada)
    except Exception as e:
        print(f"Eroare la calcularea SMA: {e}")
        df['SMA'] = None
    return df

def calculeaza_MACD(df):
    try:
        macd = ta.macd(df['Preț închidere'])
        df['MACD'] = macd['MACD_12_26_9']
        df['Signal'] = macd['MACDs_12_26_9']
        df['Histogram'] = macd['MACDh_12_26_9']
    except Exception as e:
        print(f"Eroare la calcularea MACD: {e}")
        df['MACD'] = df['Signal'] = df['Histogram'] = None
    return df

def calculeaza_ATR(df, perioada=14):
    try:
        df['ATR'] = ta.atr(high=df['Preț maxim'], low=df['Preț minim'], close=df['Preț închidere'], length=perioada)
    except Exception as e:
        print(f"Eroare la calcularea ATR: {e}")
        df['ATR'] = None
    return df

def calculeaza_OBV(df):
    try:
        df['OBV'] = ta.obv(close=df['Preț închidere'], volume=df['Volum'])
    except Exception as e:
        print(f"Eroare la calcularea OBV: {e}")
        df['OBV'] = None
    return df

def calculeaza_EMA(df, perioada=9):
    try:
        df['EMA'] = ta.ema(df['Preț închidere'], length=perioada)
    except Exception as e:
        print(f"Eroare la calcularea EMA: {e}")
        df['EMA'] = None
    return df

if __name__ == "__main__":
    calculeaza_indicatori_pentru_toate()
