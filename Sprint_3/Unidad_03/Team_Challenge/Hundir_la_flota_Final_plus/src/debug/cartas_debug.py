
import os
import json
import requests
import pandas as pd
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(page_title="cEDH Cartas Debug", layout="wide")

MAZOS_DIR = "mazos_completos"
CARTAS_DIR = "cartas_por_mazo"
RESPALDO_DIR = os.path.join(CARTAS_DIR, "respaldos_json")
os.makedirs(CARTAS_DIR, exist_ok=True)
os.makedirs(RESPALDO_DIR, exist_ok=True)

st.title("🧙 cEDH Analyzer - DEBUG Cartas desde Moxfield")

mazos = [f for f in os.listdir(MAZOS_DIR) if f.endswith(".csv")]
if not mazos:
    st.warning("No hay mazos disponibles.")
    st.stop()

mazo_sel = st.selectbox("Selecciona un mazo", mazos)
df = pd.read_csv(os.path.join(MAZOS_DIR, mazo_sel))

if df.empty or "URL Mazo" not in df.columns:
    st.error("Archivo inválido o sin URL.")
    st.stop()

url = df.loc[0, "URL Mazo"]
st.markdown(f"🔗 URL Mazo: `{url}`")

deck_id = url.split("/")[-1]
api_url = f"https://api2.moxfield.com/v2/decks/all/{deck_id}"

try:
    response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    data = response.json()

    # Guardar JSON crudo para inspección
    raw_path = os.path.join(RESPALDO_DIR, f"{deck_id}_raw.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    st.success("✅ JSON recibido correctamente.")
    st.markdown("### Fragmento del JSON crudo:")
    st.json(data.get("boards", {}), expanded=False)

    # Extraer cartas si existen
    cartas = []
    for zona, cartas_zona in data.get("boards", {}).items():
        for carta_id, carta_data in cartas_zona.items():
            nombre = carta_data.get("card", {}).get("name", "desconocido")
            cartas.append({
                "zona": zona,
                "nombre": nombre,
                "cantidad": carta_data.get("quantity", 1),
                "isCommander": carta_data.get("isCommander", False)
            })

    if cartas:
        df_cartas = pd.DataFrame(cartas)
        st.markdown("### 📄 Cartas extraídas:")
        st.dataframe(df_cartas)
        json_path = os.path.join(CARTAS_DIR, f"{deck_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(cartas, f, indent=2, ensure_ascii=False)
    else:
        st.warning("⚠️ JSON recibido pero no se encontraron cartas.")

except Exception as e:
    st.error(f"❌ Error al conectar con Moxfield: {e}")
