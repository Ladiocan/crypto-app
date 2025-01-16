{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import pandas as pd\
from indicatori_tehnici import calculeaza_RSI, calculeaza_SMA, calculeaza_MACD, calculeaza_ATR, calculeaza_OBV, calculeaza_EMA\
import os\
\
DIRECTOR_COMBINAT = "/Users/ladislau/Documents/cryptapp/crypto_data/combined"\
DIRECTOR_PROCESAT = "/Users/ladislau/Documents/cryptapp/crypto_data/processed"\
\
if not os.path.exists(DIRECTOR_PROCESAT):\
    os.makedirs(DIRECTOR_PROCESAT)\
\
def proceseaza_date(pereche):\
    """\
    Proceseaz\uc0\u259  datele combinate \u537 i calculeaz\u259  indicatorii tehnici.\
    """\
    fisier_comb = os.path.join(DIRECTOR_COMBINAT, f"combined_\{pereche\}_USDC.csv")\
\
    if not os.path.exists(fisier_comb):\
        print(f"Fi\uc0\u537 ierul combinat pentru \{pereche\} nu exist\u259 .")\
        return\
\
    # \'cencarc\uc0\u259  datele combinate\
    df = pd.read_csv(fisier_comb, parse_dates=["Timp \'eenceput"])\
\
    # Calculeaz\uc0\u259  indicatorii tehnici\
    df = calculeaza_RSI(df)\
    df = calculeaza_SMA(df)\
    df = calculeaza_MACD(df)\
    df = calculeaza_ATR(df)\
    df = calculeaza_OBV(df)\
    df = calculeaza_EMA(df)\
\
    # Salveaz\uc0\u259  datele procesate\
    fisier_salveaza = os.path.join(DIRECTOR_PROCESAT, f"processed_\{pereche\}_USDC.csv")\
    df.to_csv(fisier_salveaza, index=False)\
    print(f"Datele procesate pentru \{pereche\} au fost salvate \'een \{fisier_salveaza\}.")\
\
if __name__ == "__main__":\
    perechi = ["BTC", "ETH", "BNB", "XRP", "ADA"]  # Adaug\uc0\u259  toate perechile relevante\
    for pereche in perechi:\
        proceseaza_date(pereche)\
}