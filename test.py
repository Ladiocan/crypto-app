import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# Configurația API
CRYPTOCOMPARE_API_KEY = "00528d1430dcf301a63031b7e186dbe0129ec13fa59622ba1e05b44fe3d270b2"  # Înlocuiește cu cheia ta API
BASE_URL = "https://min-api.cryptocompare.com/data/v2/histohour"

# Director de salvare
DIRECTOR_SALVARE = "/Users/ladislau/Documents/cryptapp/crypto_data"
if not os.path.exists(DIRECTOR_SALVARE):
    os.makedirs(DIRECTOR_SALVARE)

# Data limită pentru descărcare (1 ianuarie 2022)
DATA_LIMITA = datetime(2022, 1, 1)

def obtine_date_crypto_compare(symbol, fiat="USDC", limit=2000, to_timestamp=None):
    """
    Obține date istorice de la CryptoCompare pentru o anumită pereche.
    """
    params = {
        "fsym": symbol,
        "tsym": fiat,
        "limit": limit,
        "api_key": CRYPTOCOMPARE_API_KEY
    }
    if to_timestamp:
        params["toTs"] = int(to_timestamp.timestamp())

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "Success":
        df = pd.DataFrame(data["Data"]["Data"])
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.rename(columns={"time": "Timp început", "high": "Preț maxim", "low": "Preț minim",
                           "open": "Preț deschidere", "close": "Preț închidere", "volumeto": "Volum"}, inplace=True)
        return df
    else:
        raise Exception(f"Eroare la obținerea datelor pentru {symbol}: {data.get('Message', 'Nicio informație suplimentară')}")

def descarca_date_complet(symbol, fiat="USDC", limit=2000):
    """
    Descarcă date istorice complete de la CryptoCompare până la data limită.
    """
    fisier = os.path.join(DIRECTOR_SALVARE, f"crypto_compare_{symbol}_{fiat}.csv")
    df_total = pd.DataFrame()

    # Începe descărcarea din prezent
    to_timestamp = datetime.now()

    while True:
        try:
            df = obtine_date_crypto_compare(symbol, fiat, limit=limit, to_timestamp=to_timestamp)
            if df.empty:
                break  # Oprește dacă nu mai sunt date
            df_total = pd.concat([df_total, df])
            to_timestamp = df["Timp început"].min() - timedelta(hours=1)
            print(f"Descărcat până la: {to_timestamp}")

            # Oprește descărcarea dacă s-a ajuns la data limită
            if to_timestamp < DATA_LIMITA:
                print(f"Am ajuns la data limită pentru {symbol}: {DATA_LIMITA}")
                break

            # Evită descărcările redundante
            if len(df) < limit:
                break
        except Exception as e:
            print(f"Eroare la descărcarea datelor pentru {symbol}: {e}")
            break

    # Salvează datele
    df_total = df_total.drop_duplicates(subset=["Timp început"]).sort_values(by="Timp început")
    df_total.to_csv(fisier, index=False)
    print(f"Datele complete pentru {symbol} au fost salvate în {fisier}.")

if __name__ == "__main__":
    perechi = [
        "MOVE", "PHA", "PLN", "STEEM", "USUAL"
    ]
    print(f"Descărcăm date pentru {len(perechi)} perechi: {perechi}")

    for pereche in perechi:
        descarca_date_complet(symbol=pereche, fiat="USDC", limit=2000)
