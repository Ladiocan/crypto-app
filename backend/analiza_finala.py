import talib
import numpy as np

def calculeaza_RSI(prețuri, perioada=14):
    # Asigură-te că prețurile sunt de tipul np.float64
    prețuri = np.array(prețuri, dtype=np.float64)
    rsi = talib.RSI(prețuri, timeperiod=perioada)
    return rsi

# Exemplu de date
prețuri = [93000.0, 94000.0, 95000.0, 94000.0, 93500.0, 92000.0, 93000.0, 92500.0, 91500.0, 90000.0, 91000.0, 92000.0, 91500.0, 92500.0]
rsi = calculeaza_RSI(prețuri)
print(rsi)
