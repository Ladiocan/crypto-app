import os
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
from indicatori_tehnici import calculeaza_RSI, calculeaza_SMA, calculeaza_MACD
from predictii import prezice_pret

app = Flask(__name__)
CORS(app)
DIRECTOR_DATE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "crypto_data"))

@app.route("/api/update")
def update():
    try:
        perechi = [f.split(".")[0] for f in os.listdir(DIRECTOR_DATE) if f.endswith(".csv")]
        rezultate = []

        for pereche in perechi:
            fisier = os.path.join(DIRECTOR_DATE, f"{pereche}.csv")
            try:
                df = pd.read_csv(fisier)
                df = calculeaza_RSI(df)
                df = calculeaza_SMA(df)
                df = calculeaza_MACD(df)

                pret_curent = df["Preț închidere"].iloc[-1]
                predicted_price = prezice_pret(df, pereche)
                rsi = df["RSI"].iloc[-1]
                sma = df["SMA"].iloc[-1]

                recomandare = "N/A"
                if predicted_price and pret_curent:
                    if abs(predicted_price - pret_curent) / pret_curent > 0.5:
                        recomandare = "N/A"
                    else:
                        if predicted_price > pret_curent and rsi < 30:
                            recomandare = "Cumpărare"
                        elif predicted_price < pret_curent and rsi > 70:
                            recomandare = "Vânzare"
                        else:
                            recomandare = "Păstrare"

                rezultate.append({
                    "symbol": pereche,
                    "current_price": pret_curent,
                    "predicted_price": predicted_price,
                    "RSI": rsi,
                    "SMA": sma,
                    "Recommendation": recomandare
                })
            except Exception as e:
                print(f"❌ Eroare la {pereche}: {e}")
                continue

        return jsonify(results=rezultate)

    except Exception as e:
        print(f"❌ Eroare generală: {e}")
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
