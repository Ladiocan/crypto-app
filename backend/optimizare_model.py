import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle

# Calea către fișierul date_antrenament.csv
DIRECTOR_CSV = "crypto_data"
FISIER_ANRENAMENT = os.path.join(DIRECTOR_CSV, "date_antrenament.csv")

# Verifică dacă fișierul de antrenament există
if not os.path.exists(FISIER_ANRENAMENT):
    print(f"Fișierul '{FISIER_ANRENAMENT}' nu există. Asigură-te că a fost generat corect.")
    exit()

# Încarcă datele de antrenament
df = pd.read_csv(FISIER_ANRENAMENT)
print(f"Fișierul de antrenament '{FISIER_ANRENAMENT}' a fost încărcat cu succes.")

# Caracteristici și ținta
try:
    X = df[["RSI", "SMA", "MACD", "Signal", "Histogram", "ATR", "OBV", "EMA"]]
    y = df["target"]
except KeyError as e:
    print(f"Eroare: Coloana lipsă în datele de antrenament: {e}")
    exit()

# Împarte datele în seturi de antrenament și testare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definește modelul și grila de hiperparametri
model = RandomForestRegressor(random_state=42)
parametri = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

# Optimizare cu Grid Search
print("Optimizăm modelul... Acest proces poate dura câteva minute.")
grid_search = GridSearchCV(model, parametri, cv=3, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Afișează cei mai buni hiperparametri
print("Cei mai buni parametri:", grid_search.best_params_)

# Salvează hiperparametrii într-un fișier
with open("best_hyperparameters.txt", "w") as file:
    file.write(str(grid_search.best_params_))
print("Hiperparametrii optimi au fost salvați în 'best_hyperparameters.txt'")

# Salvează modelul optimizat
best_model = grid_search.best_estimator_
with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(best_model, file)

# Afișează scorul modelului optimizat
score = grid_search.best_score_
print(f"Performanța modelului optimizat: {abs(score):.2f} (Mean Squared Error)")

print("Modelul optimizat a fost salvat în 'random_forest_model.pkl'")
