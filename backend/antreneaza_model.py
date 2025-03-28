import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from indicatori_tehnici import genereaza_date_antrenament  # Importă funcția de generare a datelor

# Generează fișierul de antrenament
genereaza_date_antrenament()

# Încarcă datele de antrenament
FISIER_ANRENAMENT = "date_antrenament.csv"
df = pd.read_csv(FISIER_ANRENAMENT)
df.dropna(inplace=True)

# Caracteristici și ținta
X = df[["RSI", "SMA", "MACD", "Signal", "Histogram", "ATR", "OBV", "EMA"]]
y = df["target"]

# Împarte datele în seturi de antrenament și testare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creează și antrenează modelul Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluează modelul
score = model.score(X_test, y_test)
print(f"Precizia modelului pe datele de testare: {score:.2f}")

# Salvează modelul într-un fișier
with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Modelul a fost salvat în 'random_forest_model.pkl'")
