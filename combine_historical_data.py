import pandas as pd
import os

DIRECTOR_CRYPTOCOMPARE = "/Users/ladislau/Documents/cryptapp/crypto_data"
DIRECTOR_BINANCE = "/Users/ladislau/Documents/cryptapp/crypto_data/binance_processed"
DIRECTOR_SALVARE = "/Users/ladislau/Documents/cryptapp/crypto_data/combined"

if not os.path.exists(DIRECTOR_SALVARE):
    os.makedirs(DIRECTOR_SALVARE)

def combina_date_istorice(pereche):
    """
    Combină datele istorice din CryptoCompare și Binance pentru o pereche.
    """
    fisier_crypto = os.path.join(DIRECTOR_CRYPTOCOMPARE, f"crypto_compare_{pereche}_USDC.csv")
    fisier_binance = os.path.join(DIRECTOR_BINANCE, f"date_{pereche}USDC.csv")

    # Verifică existența fișierelor
    exista_crypto = os.path.exists(fisier_crypto)
    exista_binance = os.path.exists(fisier_binance)

    if not exista_crypto and not exista_binance:
        print(f"Fișierele pentru {pereche} nu există în niciuna dintre surse.")
        return

    # Încarcă datele
    df_crypto = pd.read_csv(fisier_crypto, parse_dates=["Timp început"]) if exista_crypto else pd.DataFrame()
    df_binance = pd.read_csv(fisier_binance, parse_dates=["Timp început"]) if exista_binance else pd.DataFrame()

    # Combina datele
    df_combinat = pd.concat([df_crypto, df_binance]).drop_duplicates(subset=["Timp început"]).sort_values(by="Timp început")
    
    # Salvează datele combinate
    fisier_salveaza = os.path.join(DIRECTOR_SALVARE, f"combined_{pereche}_USDC.csv")
    df_combinat.to_csv(fisier_salveaza, index=False)
    print(f"Datele pentru {pereche} au fost combinate și salvate în {fisier_salveaza}.")

if __name__ == "__main__":
    # Extrage toate perechile disponibile
    perechi_crypto = [f.split('_')[2] for f in os.listdir(DIRECTOR_CRYPTOCOMPARE) if f.startswith("crypto_compare_")]
    perechi_binance = [f.split('_')[1].replace("USDC.csv", "") for f in os.listdir(DIRECTOR_BINANCE) if f.startswith("date_")]
    perechi_total = list(set(perechi_crypto + perechi_binance))

    print(f"Perechi disponibile: {perechi_total}")

    # Procesează toate perechile
    for pereche in perechi_total:
        combina_date_istorice(pereche)
