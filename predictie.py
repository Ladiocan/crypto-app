import pickle
import pandas as pd

# Încarcă modelul Random Forest
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

def prezice_pret(dataframe):
    """
    Folosește modelul Random Forest pentru a prezice prețul.
    """
    # Selectează caracteristicile relevante
    caracteristici = ['RSI', 'SMA', 'MACD', 'Signal', 'Histogram', 'ATR', 'OBV', 'EMA']
    if not all(col in dataframe.columns for col in caracteristici):
        raise ValueError("DataFrame-ul trebuie să conțină toți indicatorii necesari.")

    # Pregătește datele pentru model
    input_model = dataframe[caracteristici].iloc[-1:].fillna(0)
    predicție = model.predict(input_model)[0]
    return predicție
