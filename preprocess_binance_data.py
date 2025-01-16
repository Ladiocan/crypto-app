import pandas as pd
import os
from datetime import datetime, timedelta

DIRECTOR_BINANCE = "/Users/ladislau/Documents/cryptapp/crypto_data"
DIRECTOR_PROCESAT_BINANCE = "/Users/ladislau/Documents/cryptapp/crypto_data/binance_processed"

if not os.path.exists(DIRECTOR_PROCESAT_BINANCE):
    os.makedirs(DIRECTOR_PROCESAT_BINANCE)

def preproceseaza_fisier_binance(fisier, data_inceput="2023-01-01 00:00:00", interval="1h"):
    """
    Preprocesează un fișier Binance și adaugă coloana 'Timp început'.
    """
    try:
        df = pd.read_csv(fisier)

        # Generează coloana 'Timp început' pornind de la data_inceput
        timp_inceput = datetime.strptime(data_inceput, "%Y-%m-%d %H:%M:%S")
        df["Timp început"] = [timp_inceput + timedelta(hours=i) for i in range(len(df))]

        # Renumește coloanele pentru a le standardiza
        df = df.rename(columns={
            "Preț deschidere": "Preț deschidere",
            "Preț închidere": "Preț închidere",
            "Preț maxim": "Preț maxim",
            "Preț minim": "Preț minim",
            "Volum": "Volum"
        })

        # Salvează fișierul preprocesat
        fisier_salveaza = os.path.join(DIRECTOR_PROCESAT_BINANCE, os.path.basename(fisier))
        df.to_csv(fisier_salveaza, index=False)
        print(f"Fișierul {fisier} a fost preprocesat și salvat în {fisier_salveaza}.")
    except Exception as e:
        print(f"Eroare la preprocesarea fișierului {fisier}: {e}")

if __name__ == "__main__":
    # Procesează toate fișierele Binance
    for fisier in os.listdir(DIRECTOR_BINANCE):
        if fisier.startswith("date_") and fisier.endswith(".csv"):
            cale_fisier = os.path.join(DIRECTOR_BINANCE, fisier)
            preproceseaza_fisier_binance(cale_fisier, data_inceput="2023-01-01 00:00:00")
