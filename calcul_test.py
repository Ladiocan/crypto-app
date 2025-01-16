import talib
import numpy as np

# Exemplu de date pentru prețuri (acum sunt mai multe de 14)
prețuri = np.array([
    93000.0, 94000.0, 95000.0, 94000.0, 93500.0, 
    92000.0, 93000.0, 92500.0, 91500.0, 90000.0,
    91000.0, 92000.0, 91500.0, 92500.0, 93000.0,
    94000.0, 95000.0
])

# Calcularea RSI pentru datele de preț
rsi = talib.RSI(prețuri, timeperiod=14)

# Afișează doar valorile valide după 14 perioade
print(f"RSI valid: {rsi[13:]}")  # Afișează valorile RSI după 14 perioade
