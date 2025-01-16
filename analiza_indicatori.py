import talib
import numpy as np

# Funcție pentru calculul RSI
def calculeaza_RSI(prețuri, perioada=14):
    return talib.RSI(np.array(prețuri), timeperiod=perioada)

# Funcție pentru calculul SMA
def calculeaza_SMA(prețuri, perioada=30):
    return talib.SMA(np.array(prețuri), timeperiod=perioada)
