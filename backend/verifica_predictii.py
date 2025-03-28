import pandas as pd
from binance_data import obtine_preturi_curente
from datetime import datetime

def verifica_predictii():
    try:
        # Încarcă predicțiile salvate
        df = pd.read_csv("istoric_predictii.csv", names=["symbol", "current_price", "predicted_price", "timestamp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Obține prețurile curente
        preturi_curente = obtine_preturi_curente()
        df["real_price"] = df["symbol"].map(preturi_curente).fillna(df["current_price"])

        # Compară predicțiile cu prețurile reale
        df["accuracy"] = ((df["predicted_price"] - df["real_price"]).abs() / df["real_price"]) * 100
        df["trend_match"] = ((df["predicted_price"] > df["current_price"]) == (df["real_price"] > df["current_price"]))

        # Analiză pe ultimele 24 de ore
        cutoff_time = datetime.now() - pd.Timedelta(hours=24)
        recent_df = df[df["timestamp"] > cutoff_time]

        # Agregare: precizia medie pe fiecare simbol
        analiza = recent_df.groupby("symbol").agg(
            accuracy_mediu=("accuracy", "mean"),
            trend_corect=("trend_match", "mean"),  # Procentul de predicții corecte
            numar_predicții=("trend_match", "count")
        )
        analiza["trend_corect"] = (analiza["trend_corect"] * 100).round(2)

        print("Analiza performanței în ultimele 24 de ore:")
        print(analiza)

        # Salvează rezultatul într-un fișier
        analiza.to_csv("analiza_24h.csv")
    except FileNotFoundError:
        print("Fișierul 'istoric_predictii.csv' nu există. Nu există date pentru verificare.")
