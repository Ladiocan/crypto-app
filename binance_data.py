import requests
import pandas as pd

BASE_URL = "https://api.binance.com"

def obtine_perechi_usdc():
    """
    Obține toate perechile de criptomonede care includ USDC.
    Returnează o listă cu simbolurile perechilor.
    """
    url = f"{BASE_URL}/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    perechi = [
        simbol["symbol"] for simbol in data["symbols"]
        if "USDC" in simbol["symbol"] and simbol["status"] == "TRADING"
    ]
    return perechi

def obtine_preturi_curente():
    """
    Obține prețurile curente pentru toate perechile de criptomonede.
    Returnează un dicționar cu perechile și prețurile lor.
    """
    url = f"{BASE_URL}/api/v3/ticker/price"
    response = requests.get(url)
    data = response.json()
    preturi = {item["symbol"]: float(item["price"]) for item in data}
    return preturi

def obtine_date_binance(symbol="BTCUSDT", interval="1h", limit=100):
    """
    Obține date istorice de la Binance pentru o anumită pereche.
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Transformă datele în DataFrame
    columns = ["Timp început", "Preț deschidere", "Preț închidere", "Preț maxim", "Preț minim", "Volum"]
    df = pd.DataFrame(data, columns=[
        "Timp început", "Preț deschidere", "Preț închidere", "Preț maxim", "Preț minim", "Volum",
        "_", "_", "_", "_", "_", "_"
    ])
    df = df[columns]

    # Convertim coloanele relevante la float
    numeric_columns = ["Preț deschidere", "Preț închidere", "Preț maxim", "Preț minim", "Volum"]
    df[numeric_columns] = df[numeric_columns].astype(float)

    df["Timp început"] = pd.to_datetime(df["Timp început"], unit='ms')
    df.set_index("Timp început", inplace=True)
    return df


    # Transformă datele în DataFrame
    columns = ["Timp început", "Preț deschidere", "Preț închidere", "Preț maxim", "Preț minim", "Volum"]
    df = pd.DataFrame(data, columns=[
        "Timp început", "Preț deschidere", "Preț închidere", "Preț maxim", "Preț minim", "Volum",
        "_", "_", "_", "_", "_", "_"
    ])
    df = df[columns]
    df["Timp început"] = pd.to_datetime(df["Timp început"], unit='ms')
    df.set_index("Timp început", inplace=True)
    return df

# Test simplu
if __name__ == "__main__":
    # Testare perechi USDC
    perechi = obtine_perechi_usdc()
    print(f"Perechi USDC: {perechi}")

    # Testare prețuri curente
    preturi = obtine_preturi_curente()
    print(f"Prețuri curente: {preturi}")

    # Testare date istorice
    date = obtine_date_binance(symbol="BTCUSDT", interval="1h", limit=10)
    print(f"Date istorice BTCUSDT:\n{date}")
