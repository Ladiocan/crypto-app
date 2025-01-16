from binance_data import obtine_perechi_usdc, obtine_date_binance
from indicatori_tehnici import calculeaza_RSI, calculeaza_SMA, calculeaza_MACD, calculeaza_ATR, calculeaza_OBV, calculeaza_EMA
import pandas as pd
import os

# Directorul unde vor fi salvate datele
DIRECTOR_SALVARE = "/Users/ladislau/Documents/cryptapp/crypto_data"

# Creează directorul dacă nu există
if not os.path.exists(DIRECTOR_SALVARE):
    os.makedirs(DIRECTOR_SALVARE)

def colecteaza_date_antrenament():
    """
    Colectează date recente pentru antrenament și le salvează într-un fișier CSV unic.
    """
    perechi_usdc = obtine_perechi_usdc()  # Obține toate perechile USDC
    date_antrenament = []

    for pereche in perechi_usdc:
        print(f"Procesăm date pentru: {pereche}")
        try:
            # Obține datele istorice recente
            date = obtine_date_binance(symbol=pereche, interval="1h", limit=100)
            date = calculeaza_RSI(date)
            date = calculeaza_SMA(date)
            date = calculeaza_MACD(date)
            date = calculeaza_ATR(date)
            date = calculeaza_OBV(date)
            date = calculeaza_EMA(date)

            for i in range(len(date)):
                if not pd.isnull(date['RSI'].iloc[i]):
                    date_antrenament.append({
                        "symbol": pereche,
                        "RSI": date['RSI'].iloc[i],
                        "SMA": date['SMA'].iloc[i],
                        "MACD": date['MACD'].iloc[i],
                        "Signal": date['Signal'].iloc[i],
                        "Histogram": date['Histogram'].iloc[i],
                        "ATR": date['ATR'].iloc[i],
                        "OBV": date['OBV'].iloc[i],
                        "EMA": date['EMA'].iloc[i],
                        "target": date['Preț închidere'].iloc[i]
                    })
        except Exception as e:
            print(f"Eroare la procesarea perechii {pereche}: {e}")

    # Creează un DataFrame din datele colectate
    df_antrenament = pd.DataFrame(date_antrenament)
    print(f"Date de antrenament colectate: {len(df_antrenament)} intrări")
    # Salvează datele în directorul specificat
    fisier_antrenament = os.path.join(DIRECTOR_SALVARE, "date_antrenament.csv")
    df_antrenament.to_csv(fisier_antrenament, index=False)
    print(f"Datele de antrenament au fost salvate în {fisier_antrenament}")

def colecteaza_istoric_complet(symbol, interval="1h"):
    """
    Colectează toate datele istorice disponibile de la Binance și le salvează într-un fișier CSV separat pentru fiecare pereche.
    """
    fisier = os.path.join(DIRECTOR_SALVARE, f"date_{symbol}.csv")

    try:
        if os.path.exists(fisier):
            try:
                # Încarcă datele existente
                df_vechi = pd.read_csv(fisier, parse_dates=["Timp început"])
                ultima_data = df_vechi["Timp început"].max()
                print(f"Ultima dată colectată pentru {symbol}: {ultima_data}")
            except Exception as e:
                print(f"Eroare la citirea fișierului {fisier}: {e}")
                df_vechi = pd.DataFrame()
                ultima_data = None
        else:
            df_vechi = pd.DataFrame()
            ultima_data = None

        # Colectează date noi
        print(f"Colectez date pentru {symbol}...")
        df_nou = obtine_date_binance(symbol=symbol, interval=interval, limit=1000)

        if not df_vechi.empty:
            df_complet = pd.concat([df_vechi, df_nou]).drop_duplicates(subset=["Timp început"]).sort_values(by="Timp început")
        else:
            df_complet = df_nou

        # Salvează datele în fișier
        df_complet.to_csv(fisier, index=False)
        print(f"Datele pentru {symbol} au fost salvate în {fisier}.")

    except Exception as e:
        print(f"Eroare la procesarea perechii {symbol}: {e}")

if __name__ == "__main__":
    # Colectează datele pentru antrenament pentru toate perechile USDC
    colecteaza_date_antrenament()

    # Colectează istoricul complet pentru toate perechile USDC
    perechi = obtine_perechi_usdc()  # Obține toate perechile USDC
    for pereche in perechi:
        colecteaza_istoric_complet(symbol=pereche, interval="1h")
