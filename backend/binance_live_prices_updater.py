import time
import requests
from binance.client import Client
from dotenv import load_dotenv
import os

# Încarcă cheile API din fișierul .env
load_dotenv("cheie.env")
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Creează clientul Binance
client = Client(api_key, api_secret)

def obtine_preturi_curente():
    """
    Obține prețurile curente pentru toate perechile USDC.
    """
    try:
        ticker_prices = client.get_all_tickers()
        preturi_curente = {item["symbol"]: float(item["price"]) for item in ticker_prices if "USDC" in item["symbol"]}
        return preturi_curente
    except Exception as e:
        print(f"Eroare la obținerea prețurilor curente: {e}")
        return {}

def actualizeaza_afisarea():
    """
    Actualizează prețurile curente la fiecare minut și le afișează.
    """
    while True:
        preturi = obtine_preturi_curente()
        if preturi:
            print("\nPrețuri curente pentru perechile USDC:")
            for simbol, pret in preturi.items():
                print(f"{simbol}: {pret}")
        else:
            print("Nu s-au putut obține prețurile curente.")
        
        # Așteaptă 60 de secunde înainte de următoarea actualizare
        time.sleep(60)

if __name__ == "__main__":
    print("Pornim actualizarea prețurilor curente...")
    actualizeaza_afisarea()
