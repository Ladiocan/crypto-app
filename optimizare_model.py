import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle

# Încarcă datele de antrenament
df = pd.read_csv("date_antrenament.csv")

# Caracteristici și ținta
X = df[["RSI", "SMA", "MACD", "Signal", "Histogram", "ATR", "OBV", "EMA"]]
y = df["target"]

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
grid_search = GridSearchCV(model, parametri, cv=3, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Afișează cei mai buni hiperparametri
print("Cei mai buni parametri:", grid_search.best_params_)

# Salvează modelul optimizat
best_model = grid_search.best_estimator_
with open("random_forest_model.pkl", "wb") as file:
    pickle.dump(best_model, file)

print("Modelul optimizat a fost salvat în 'random_forest_model.pkl'")
