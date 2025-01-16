from binance.client import Client
import pandas as pd

# Cheile API (înlocuiește-le cu ale tale)
api_key = '0iXgUnCsEbUp1c97aa16ikNja0HgP9Cu3aFtuVuY4jYgPkXnycOatJ6phgCQ4bzK'
api_secret = 'Cz4MvpSw30grggvmcWFWXVtxHpa8epH2xwm75uApMe0kUfNA9JEbRS6PcoWN1ylT'

# Crearea clientului Binance
client = Client(api_key, api_secret)

# Funcție pentru a obține simbolurile raportate la USDC
def obtine_simboluri():
    exchange_info = client.get_exchange_info()  # Obține informațiile despre schimburile disponibile
    simboluri_usdc = []

    # Parcurge toate simbolurile și filtrează-le doar pe cele raportate la USDC
    for symbol in exchange_info['symbols']:
        if symbol['quoteAsset'] == 'USDC':  # Verifică dacă simbolul este raportat la USDC
            simboluri_usdc.append(symbol['symbol'])  # Adaugă simbolul în listă

    return simboluri_usdc

# Funcție pentru a prelua date istorice pentru o criptomonedă
def preia_date_istorice(symbol, interval='1d', limit=100):
    candlesticks = client.get_historical_klines(symbol, interval, limit=limit)  # Preia datele istorice
    date_istorica = []
    
    # Prelucrarea datelor și crearea unei liste cu timestamp și prețuri de închidere
    for candlestick in candlesticks:
        timestamp = candlestick[0] / 1000  # Conversie timestamp în secunde
        preț_inchidere = float(candlestick[4])  # Prețul de închidere
        date_istorica.append([timestamp, preț_inchidere])
    
    return date_istorica

# Obține lista de simboluri raportate la USDC
print("Obțin lista de simboluri raportate la USDC...")
simboluri = obtine_simboluri()
print(f"Simboluri obținute: {simboluri}")

# Afișează simbolurile raportate la USDC
# Acestea sunt criptomonedele care vor fi folosite pentru procesul de analiză
