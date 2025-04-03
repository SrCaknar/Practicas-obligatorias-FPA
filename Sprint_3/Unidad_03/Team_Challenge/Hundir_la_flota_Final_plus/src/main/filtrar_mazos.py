
import os
import json
import requests
import pandas as pd
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(page_title="cEDH Analyzer - Mazos Accesibles", layout="wide")

MAZOS_DIR = "mazos_completos"
CARTAS_DIR = "cartas_por_mazo"
RESPALDO_DIR = os.path.join(CARTAS_DIR, "respaldos_json")
LOG_PATH = os.path.join(CARTAS_DIR, "mazos_inaccesibles.csv")

os.makedirs(CARTAS_DIR, exist_ok=True)
os.makedirs(RESPALDO_DIR, exist_ok=True)

st.title("🧙 Filtrado de Mazos Accesibles desde Moxfield")

mazos = [f for f in os.listdir(MAZOS_DIR) if f.endswith(".csv")]
accesibles = []
inaccesibles = []

for mazo in mazos:
    ruta = os.path.join(MAZOS_DIR, mazo)
    df = pd.read_csv(ruta)
    if df.empty or "URL Mazo" not in df.columns:
        continue
    url = df.loc[0, "URL Mazo"]
    deck_id = url.split("/")[-1]
    api_url = f"https://api2.moxfield.com/v2/decks/all/{deck_id}"

    try:
        response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        # Guarda respaldo del JSON válido
        raw_path = os.path.join(RESPALDO_DIR, f"{deck_id}_raw.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        accesibles.append({"mazo": mazo, "url": url, "deck_id": deck_id})
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            inaccesibles.append({"mazo": mazo, "url": url, "motivo": "403 Forbidden"})
        else:
            inaccesibles.append({"mazo": mazo, "url": url, "motivo": str(e)})

# Guardar los inaccesibles como CSV
if inaccesibles:
    pd.DataFrame(inaccesibles).to_csv(LOG_PATH, index=False)

# Mostrar resultados
st.success(f"✅ Mazos accesibles: {len(accesibles)}")
st.warning(f"⚠️ Mazos inaccesibles: {len(inaccesibles)}")

if accesibles:
    st.markdown("### 🟢 Mazos accesibles:")
    st.dataframe(pd.DataFrame(accesibles))

if inaccesibles:
    st.markdown("### 🔴 Mazos inaccesibles:")
    st.dataframe(pd.DataFrame(inaccesibles))
