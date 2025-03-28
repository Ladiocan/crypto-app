import pickle
import csv
from datetime import datetime
import numpy as np

# Încarcă modelul antrenat
with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)

def prezice_pret(df, symbol):
    """
    Prezice prețul viitor pe baza ultimelor date din DataFrame.
    """
    if df is None or df.empty:
        print("Eroare: Datele de intrare sunt goale.")
        return None
    try:
        # Verifică dacă toate coloanele necesare există
        required_columns = ["RSI", "SMA", "MACD", "Signal", "Histogram", "ATR", "OBV", "EMA"]
        if not all(col in df.columns for col in required_columns):
            print("Eroare: Datele de intrare nu conțin toate coloanele necesare.")
            return None

        # Extrage ultimul rând pentru predicție
        X = df[required_columns].tail(1)
        if X.isnull().values.any():
            print(f"Datele de intrare conțin valori lipsă:\n{X.isnull().sum()}")
            return None

        # Afișează datele utilizate pentru predicție
        print(f"Datele utilizate pentru predicție:\n{X}")

        # Calculează predicția
        predicted_price = model.predict(X)[0]

        # Salvează predicția
        current_price = df["Preț închidere"].iloc[-1]
        salveaza_predictie(symbol, current_price, predicted_price)

        return predicted_price
    except Exception as e:
        print(f"Eroare la predicție: {e}")
        return None

def salveaza_predictie(symbol, current_price, predicted_price):
    """
    Salvează predicția într-un fișier CSV.
    """
    with open("istoric_predictii.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([symbol, current_price, predicted_price, datetime.now()])
        print(f"Predicția pentru {symbol} a fost salvată.")
