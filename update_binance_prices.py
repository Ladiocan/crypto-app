import requests
import pandas as pd
import os
from datetime import datetime

# Director pentru actualizări
DIRECTOR_UPDATE = "/Users/ladislau/Documents/cryptapp/crypto_data/updates"
if not os.path.exists(DIRECTOR_UPDATE):
    os.makedirs(DIRECTOR_UPDATE)

# URL-ul Binance
BASE_URL = "https://api.binance.com"

def obtine_preturi_zilnice(symbol, interval="1d"):
    """
    Obține prețurile maxime, minime și medii zilnice de la Binance.
    """
    url = f"{BASE_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    if len(data) > 0:
        kline = data[0]
        return {
            "date": datetime.fromtimestamp(kline[0] / 1000).strftime('%Y-%m-%d'),
            "high": float(kline[2]),
            "low": float(kline[3]),
            "close": float(kline[4]),
            "volume": float(kline[5])
        }
    return None

def actualizeaza_preturi(pereche):
    """
    Actualizează fișierul cu prețurile zilnice pentru o pereche.
    """
    fisier_update = os.path.join(DIRECTOR_UPDATE, f"daily_{pereche}_USDC.csv")
    simbol_binance = f"{pereche}USDC"

    preturi = obtine_preturi_zilnice(simbol_binance)
    if preturi:
        df_update = pd.DataFrame([preturi])
        if os.path.exists(fisier_update):
            df_existent = pd.read_csv(fisier_update)
            df_update = pd.concat([df_existent, df_update]).drop_duplicates(subset=["date"]).sort_values(by="date")
        df_update.to_csv(fisier_update, index=False)
        print(f"Prețurile pentru {pereche} au fost actualizate și salvate în {fisier_update}.")
    else:
        print(f"Nu s-au putut obține prețurile pentru {pereche}.")

if __name__ == "__main__":
    perechi = ["BTC", "ETH", "BNB", "XRP", "ADA"]  # Adaugă toate perechile relevante
    for pereche in perechi:
        actualizeaza_preturi(pereche)
