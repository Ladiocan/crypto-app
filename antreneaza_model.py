import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
import os

DIRECTOR_COMBINAT = "/Users/ladislau/Documents/cryptapp/crypto_data/combined"
DIRECTOR_UPDATE = "/Users/ladislau/Documents/cryptapp/crypto_data/updates"

def incarca_date():
    """
    Încarcă toate fișierele combinate și actualizările din Binance.
    """
    df_total = pd.DataFrame()
    # Date combinate
    for fisier in os.listdir(DIRECTOR_COMBINAT):
        if fisier.endswith(".csv"):
            df = pd.read_csv(os.path.join(DIRECTOR_COMBINAT, fisier))
            df_total = pd.concat([df_total, df], ignore_index=True)
    # Actualizări
    for fisier in os.listdir(DIRECTOR_UPDATE):
        if fisier.endswith(".csv"):
            df = pd.read_csv(os.path.join(DIRECTOR_UPDATE, fisier))
            df_total = pd.concat([df_total, df], ignore_index=True)
    return df_total

if __name__ == "__main__":
    df = incarca_date()
    print(f"Date totale: {df.shape[0]} rânduri")

    # Caracteristici și țintă
    X = df[["Preț maxim", "Preț minim", "Volum"]]
    y = df["Preț închidere"]

    # Antrenare
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Salvează modelul
    with open("random_forest_model.pkl", "wb") as file:
        pickle.dump(model, file)
    print("Modelul a fost salvat.")
