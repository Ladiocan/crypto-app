import pandas as pd
import os
from flask import Flask, render_template, jsonify
from indicatori_tehnici import calculeaza_RSI, calculeaza_SMA, calculeaza_MACD, calculeaza_ATR, calculeaza_OBV, calculeaza_EMA
from predictie import prezice_pret

app = Flask(__name__)
DIRECTOR_DATE = os.path.join(os.getcwd(), "crypto_data")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    try:
        perechi = [f.split(".")[0] for f in os.listdir(DIRECTOR_DATE) if f.endswith(".csv")]
        rezultate = []

        for pereche in perechi:
            fisier = os.path.join(DIRECTOR_DATE, f"{pereche}.csv")
            try:
                df = pd.read_csv(fisier, parse_dates=["Timp început"])
                df = calculeaza_RSI(df)
                df = calculeaza_SMA(df)
                df = calculeaza_MACD(df)
                df = calculeaza_ATR(df)
                df = calculeaza_OBV(df)
                df = calculeaza_EMA(df)

                pret_curent = df["Preț închidere"].iloc[-1]
                predicted_price = prezice_pret(df)

                rsi = df["RSI"].iloc[-1]
                sma = df["SMA"].iloc[-1]

                recomandare = "N/A"
                if predicted_price and pret_curent:
                    if abs(predicted_price - pret_curent) / pret_curent > 0.5:
                        print(f"Predicție improbabilă pentru {pereche}.")
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
                print(f"Eroare la procesarea perechii {pereche}: {e}")
                continue

        return jsonify(results=rezultate)
    except Exception as e:
        print(f"Eroare în endpoint-ul /update: {e}")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
