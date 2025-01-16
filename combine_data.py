import pandas as pd
import os

# Actualizează calea pentru fișierele preprocesate Binance
DIRECTOR_CRYPTOCOMPARE = "/Users/ladislau/Documents/cryptapp/crypto_data"
DIRECTOR_BINANCE = "/Users/ladislau/Documents/cryptapp/crypto_data/binance_processed"
DIRECTOR_SALVARE = "/Users/ladislau/Documents/cryptapp/crypto_data/combined"

# Creează directorul de salvare dacă nu există
if not os.path.exists(DIRECTOR_SALVARE):
    os.makedirs(DIRECTOR_SALVARE)

def verifica_si_incarca(fisier, sursa):
    """
    Încarcă un fișier CSV și verifică existența coloanei 'Timp început'.
    """
    try:
        df = pd.read_csv(fisier, parse_dates=["Timp început"], low_memory=False)
        return df
    except ValueError as e:
        print(f"Eroare la citirea fișierului {fisier} ({sursa}): {e}")
        print("Verific structura fișierului...")
        df = pd.read_csv(fisier, low_memory=False)
        if "Timp început" not in df.columns:
            print(f"Fișierul {fisier} nu conține coloana 'Timp început'. Verifică formatul sursei ({sursa}).")
            return None
        df["Timp început"] = pd.to_datetime(df["Timp început"])
        return df

def combina_date(pereche):
    """
    Combină datele din CryptoCompare și Binance pentru o pereche specifică.
    """
    fisier_crypto = os.path.join(DIRECTOR_CRYPTOCOMPARE, f"crypto_compare_{pereche}_USDC.csv")
    fisier_binance = os.path.join(DIRECTOR_BINANCE, f"date_{pereche}USDC.csv")

    if not os.path.exists(fisier_crypto):
        print(f"Fișierul CryptoCompare pentru {pereche} nu există.")
        return
    if not os.path.exists(fisier_binance):
        print(f"Fișierul Binance pentru {pereche} nu există.")
        return

    # Încarcă datele
    df_crypto = verifica_si_incarca(fisier_crypto, "CryptoCompare")
    df_binance = verifica_si_incarca(fisier_binance, "Binance")

    if df_crypto is None or df_binance is None:
        print(f"Nu se pot combina datele pentru {pereche} din cauza erorilor.")
        return

    # Combina datele
    df_combinat = pd.concat([df_crypto, df_binance]).drop_duplicates(subset=["Timp început"]).sort_values(by="Timp început")
    
    # Salvează datele combinate
    fisier_salveaza = os.path.join(DIRECTOR_SALVARE, f"combined_{pereche}_USDC.csv")
    df_combinat.to_csv(fisier_salveaza, index=False)
    print(f"Datele pentru {pereche} au fost combinate și salvate în {fisier_salveaza}.")

if __name__ == "__main__":
    # Extrage lista completă a perechilor pe baza fișierelor disponibile
    perechi_crypto = [f.split('_')[2] for f in os.listdir(DIRECTOR_CRYPTOCOMPARE) if f.startswith("crypto_compare_")]
    perechi_binance = [f.split('_')[1].replace("USDC.csv", "") for f in os.listdir(DIRECTOR_BINANCE) if f.startswith("date_")]
    perechi_comune = list(set(perechi_crypto) & set(perechi_binance))

    print(f"Perechi disponibile: {perechi_comune}")

    # Procesează toate perechile
    for pereche in perechi_comune:
        combina_date(pereche)
