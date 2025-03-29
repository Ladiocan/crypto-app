import os
import pickle
import csv
from datetime import datetime
import numpy as np

# Încarcă modelul din folderul principal models/
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "random_forest_model.pkl"))

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

def prezice_pret(df, symbol):
    if df is None or df.empty:
        print("❌ Datele de intrare sunt goale.")
        return None
    try:
        required_columns = ["RSI", "SMA", "MACD", "Signal", "Histogram", "ATR", "OBV", "EMA"]
        if not all(col in df.columns for col in required_columns):
            print(f"❌ Lipsesc coloane în {symbol}: {set(required_columns) - set(df.columns)}")
            return None

        X = df[required_columns].tail(1)
        if X.isnull().values.any():
            print(f"⚠️ Valori lipsă la {symbol}:\n{X.isnull().sum()}")
            return None

        predicted_price = model.predict(X)[0]
        current_price = df["Preț închidere"].iloc[-1]
        salveaza_predictie(symbol, current_price, predicted_price)

        return predicted_price
    except Exception as e:
        print(f"❌ Eroare la predicție {symbol}: {e}")
        return None

def salveaza_predictie(symbol, current_price, predicted_price):
    try:
        with open("istoric_predictii.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([symbol, current_price, predicted_price, datetime.now()])
            print(f"💾 Predicția salvată pentru {symbol}")
    except Exception as e:
        print(f"❌ Eroare la salvarea predicției: {e}")
