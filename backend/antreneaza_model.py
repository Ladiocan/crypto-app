import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from indicatori_tehnici import calculeaza_RSI, calculeaza_SMA, calculeaza_MACD

DIRECTOR = os.path.join(os.getcwd(), "crypto_data")
date_finale = []

for fisier in os.listdir(DIRECTOR):
    if fisier.endswith(".csv"):
        try:
            df = pd.read_csv(os.path.join(DIRECTOR, fisier))
            df = calculeaza_RSI(df)
            df = calculeaza_SMA(df)
            df = calculeaza_MACD(df)
            df["target"] = df["Preț închidere"].shift(-1)

            df = df.dropna(subset=["RSI", "SMA", "MACD", "Signal", "Histogram", "target"])
            date_finale.append(df[["RSI", "SMA", "MACD", "Signal", "Histogram", "target"]])
        except Exception as e:
            print(f"Eroare la {fisier}: {e}")

df_total = pd.concat(date_finale)
X = df_total.drop(columns=["target"])
y = df_total["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Model antrenat și salvat.")
