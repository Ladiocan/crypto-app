import os
import pandas as pd
import requests
from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime

# Încarcă cheile API din fișierul .env
load_dotenv("cheie.env")
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Creează clientul Binance
client = Client(api_key, api_secret)

# Configurare directoare
DIRECTOR_DATE = os.path.join(os.getcwd(), "crypto_data")
os.makedirs(DIRECTOR_DATE, exist_ok=True)

def obtine_perechi_usdc():
    """
    Obține toate perechile de criptomonede care includ USDC.
    """
    try:
        exchange_info = client.get_exchange_info()
        perechi = [symbol["symbol"] for symbol in exchange_info["symbols"] if symbol["quoteAsset"] == "USDC"]
        return perechi
    except Exception as e:
        print(f"Eroare la obținerea perechilor USDC: {e}")
        return []

def obtine_preturi_binance(symbol, interval="1h", limit=1000):
    """
    Obține datele istorice de preț pentru o pereche de criptomonede.
    """
    try:
        candlesticks = client.get_historical_klines(symbol, interval, limit=limit)
        date = [
            {
                "Timp început": datetime.fromtimestamp(kline[0] / 1000),
                "Preț deschidere": float(kline[1]),
                "Preț maxim": float(kline[2]),
                "Preț minim": float(kline[3]),
                "Preț închidere": float(kline[4]),
                "Volum": float(kline[5]),
            }
            for kline in candlesticks
        ]
        return pd.DataFrame(date)
    except Exception as e:
        print(f"Eroare la obținerea datelor pentru {symbol}: {e}")
        return pd.DataFrame()

def actualizeaza_fisier_csv(symbol, interval="1h"):
    """
    Actualizează sau creează fișierul CSV pentru o pereche de criptomonede.
    """
    fisier = os.path.join(DIRECTOR_DATE, f"{symbol}.csv")
    date_noi = obtine_preturi_binance(symbol, interval=interval)

    if not date_noi.empty:
        if os.path.exists(fisier):
            date_existente = pd.read_csv(fisier)
            date_existente["Timp început"] = pd.to_datetime(date_existente["Timp început"])

            date_noi["Timp început"] = pd.to_datetime(date_noi["Timp început"])
            date_actualizate = pd.concat([date_existente, date_noi]).drop_duplicates(subset=["Timp început"])
            date_actualizate = date_actualizate.sort_values(by="Timp început")
        else:
            date_actualizate = date_noi

        date_actualizate.to_csv(fisier, index=False)
        print(f"Fișierul {symbol}.csv a fost actualizat.")
    else:
        print(f"Nu există date noi pentru {symbol}.")

if __name__ == "__main__":
    # Obține perechile USDC și actualizează datele
    perechi = obtine_perechi_usdc()
    if perechi:
        print(f"Procesăm {len(perechi)} perechi USDC...")
        for pereche in perechi:
            try:
                actualizeaza_fisier_csv(pereche)
            except Exception as e:
                print(f"Eroare la procesarea perechii {pereche}: {e}")
    else:
        print("Nu au fost găsite perechi USDC.")
