
import os
import re
import json
import requests
import pandas as pd
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(page_title="cEDH Cartas por Mazo", layout="wide")

MAZOS_DIR = "mazos_completos"
CARTAS_DIR = "cartas_por_mazo"
RESPALDO_DIR = os.path.join(CARTAS_DIR, "respaldos_json")

os.makedirs(CARTAS_DIR, exist_ok=True)
os.makedirs(RESPALDO_DIR, exist_ok=True)

st.title("🧙 cEDH Analyzer - Cartas por Mazo desde Moxfield")

mazos_csv = [f for f in os.listdir(MAZOS_DIR) if f.endswith(".csv")]

if not mazos_csv:
    st.warning("No hay archivos en 'mazos_completos/'. Ejecuta primero el scraping de EDHTop16.")
    st.stop()

mazo_sel = st.selectbox("Selecciona un mazo para procesar/ver:", mazos_csv)
ruta_csv = os.path.join(MAZOS_DIR, mazo_sel)
df = pd.read_csv(ruta_csv)

if df.empty or "URL Mazo" not in df.columns:
    st.error("Archivo de mazo inválido o sin URL.")
    st.stop()

# Obtener deck ID de Moxfield
url = df.loc[0, "URL Mazo"]
parsed = urlparse(url)
deck_id = parsed.path.split("/")[-1]
api_url = f"https://api2.moxfield.com/v2/decks/all/{deck_id}"
json_path = os.path.join(CARTAS_DIR, f"{deck_id}.json")
respaldo_path = os.path.join(RESPALDO_DIR, f"{deck_id}_raw.json")

# Scraping de cartas desde Moxfield API
try:
    response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    data = response.json()
    with open(respaldo_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    cartas = []
    for zona, cartas_zona in data.get("boards", {}).items():
        for carta_id, carta_data in cartas_zona.items():
            nombre = carta_data.get("card", {}).get("name", "desconocido")
            if not nombre:
                continue
            cartas.append({
                "zona": zona,
                "nombre": nombre,
                "cantidad": carta_data.get("quantity", 1),
                "isCommander": carta_data.get("isCommander", False)
            })

    if not cartas:
        st.warning("No se encontraron cartas para este mazo.")
    else:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(cartas, f, indent=2, ensure_ascii=False)

        df_cartas = pd.DataFrame(cartas)
        st.success(f"✅ {len(cartas)} cartas extraídas y guardadas.")
        st.dataframe(df_cartas)

except Exception as e:
    st.error(f"❌ Error al obtener datos de Moxfield: {e}")
