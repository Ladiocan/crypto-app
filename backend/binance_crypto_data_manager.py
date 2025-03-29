import os
import pandas as pd
from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv("cheie.env")
client = Client(api_key=os.getenv("BINANCE_API_KEY"), api_secret=os.getenv("BINANCE_API_SECRET"))

DIRECTOR_DATE = os.path.join(os.getcwd(), "crypto_data")
os.makedirs(DIRECTOR_DATE, exist_ok=True)

def obtine_perechi_usdc():
    exchange_info = client.get_exchange_info()
    return [symbol["symbol"] for symbol in exchange_info["symbols"] if symbol["quoteAsset"] == "USDC"]

def obtine_preturi_binance(symbol, interval="1h", limit=1000):
    klines = client.get_historical_klines(symbol, interval, limit=limit)
    return pd.DataFrame([
        {
            "Timp început": datetime.fromtimestamp(k[0] / 1000),
            "Preț deschidere": float(k[1]),
            "Preț maxim": float(k[2]),
            "Preț minim": float(k[3]),
            "Preț închidere": float(k[4]),
            "Volum": float(k[5])
        }
        for k in klines
    ])

def actualizeaza_fisier_csv(symbol):
    path = os.path.join(DIRECTOR_DATE, f"{symbol}.csv")
    date = obtine_preturi_binance(symbol)
    if not date.empty:
        date.to_csv(path, index=False)
        print(f"✅ Actualizat {symbol}")

if __name__ == "__main__":
    for simbol in obtine_perechi_usdc():
        try:
            actualizeaza_fisier_csv(simbol)
        except Exception as e:
            print(f"❌ Eroare la {simbol}: {e}")
