from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from binance_data import obtine_perechi_usdc, obtine_preturi_curente, obtine_date_binance
from indicatori_tehnici import calculeaza_RSI, calculeaza_SMA, calculeaza_MACD, calculeaza_ATR, calculeaza_OBV, calculeaza_EMA
from predictie import prezice_pret
import concurrent.futures
import pandas as pd
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Directorul unde salvăm actualizările
DIRECTOR_UPDATE = "/Users/ladislau/Documents/cryptapp/crypto_data/updates"
if not os.path.exists(DIRECTOR_UPDATE):
    os.makedirs(DIRECTOR_UPDATE)

# Funcție pentru salvarea predicțiilor într-un fișier CSV
def salveaza_predictii(symbol, current_price, predicted_price, timestamp):
    try:
        with open("istoric_predictii.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([symbol, current_price, predicted_price, timestamp])
    except Exception as e:
        print(f"Eroare la salvarea predicțiilor: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    try:
        perechi_usdc = obtine_perechi_usdc()
        preturi_curente = obtine_preturi_curente()

        def proceseaza_pereche(pereche):
            try:
                if pereche in preturi_curente:
                    pret_curent = preturi_curente[pereche]
                    date = obtine_date_binance(symbol=pereche, interval="1h", limit=100)
                    date = calculeaza_RSI(date)
                    date = calculeaza_SMA(date)
                    date = calculeaza_MACD(date)
                    date = calculeaza_ATR(date)
                    date = calculeaza_OBV(date)
                    date = calculeaza_EMA(date)

                    predicted_price = prezice_pret(date)
                    return {
                        "symbol": pereche,
                        "current_price": pret_curent,
                        "predicted_price": predicted_price
                    }
            except Exception as e:
                print(f"Eroare la procesarea perechii {pereche}: {e}")
                return None

        with concurrent.futures.ThreadPoolExecutor() as executor:
            rezultate = list(executor.map(proceseaza_pereche, perechi_usdc))

        return jsonify(results=[r for r in rezultate if r])
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/raport')
def raport():
    try:
        raport_df = pd.read_csv("raport_predictii.csv")
        raport_html = raport_df.to_html(index=False, escape=False)
        return render_template('raport.html', tabel=raport_html)
    except FileNotFoundError:
        return "Raportul nu există. Te rog să rulezi predicțiile și verificarea acestora."

# Programator pentru actualizare periodică
scheduler = BackgroundScheduler()
scheduler.add_job(func=update, trigger="interval", minutes=60)  # Actualizare orară
scheduler.start()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
