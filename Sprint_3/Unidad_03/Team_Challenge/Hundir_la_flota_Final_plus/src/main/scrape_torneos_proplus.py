
import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(page_title="Scraper EDHTop16 Pro + Log", layout="wide")

BASE_URL = "https://edhtop16.com"
TORNEOS_URL = f"{BASE_URL}/tournaments"
MAZOS_DIR = "mazos_completos"
CARTAS_DIR = "cartas_por_mazo"
RESPALDO_DIR = os.path.join(CARTAS_DIR, "respaldos_json")
LOG_PATH = os.path.join(CARTAS_DIR, "log_scraping_mazos.csv")

os.makedirs(MAZOS_DIR, exist_ok=True)
os.makedirs(CARTAS_DIR, exist_ok=True)
os.makedirs(RESPALDO_DIR, exist_ok=True)

st.title("📊 Scraper EDHTop16 + Progreso y Log Detallado")

def limpiar_nombre(nombre):
    return "".join(c for c in nombre if c.isalnum() or c in "._-").replace(" ", "_")

def obtener_lista_torneos():
    try:
        r = requests.get(TORNEOS_URL, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        torneos = []
        grupos = soup.find_all("div", class_="group")

        for grupo in grupos:
            enlace = grupo.find("a", href=True)
            span = grupo.find("span")
            if not enlace or not span:
                continue
            fecha_texto = span.text.strip()
            try:
                fecha = datetime.strptime(fecha_texto.replace("st", "").replace("nd", "").replace("rd", "").replace("th", ""), "%B %d %Y")
            except:
                continue
            if fecha >= datetime.today() - timedelta(days=7):
                torneos.append({
                    "fecha": fecha,
                    "slug": enlace["href"],
                    "nombre": enlace.text.strip()
                })
        return torneos
    except Exception as e:
        st.error(f"❌ Error al obtener lista de torneos: {e}")
        return []

def obtener_html_torneo(slug):
    try:
        r = requests.get(BASE_URL + slug, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        return r.text
    except:
        return ""

def extraer_mazos(html):
    soup = BeautifulSoup(html, "html.parser")
    enlaces = soup.select("a[href*='moxfield.com/decks']")
    mazos = []
    for link in enlaces:
        contenedor = link.find_parent("div", class_="group")
        if not contenedor:
            continue
        jugador = link.text.strip("🥇🥈🥉 ").strip()
        url_mazo = link["href"]
        comandante = contenedor.find_all("a")[1].text.strip()
        spans = contenedor.find_all("span")
        posicion = spans[0].text.strip() if len(spans) > 0 else ""
        resultado = spans[1].text.strip() if len(spans) > 1 else ""
        wins = losses = draws = 0
        for part in resultado.split("/"):
            if "Wins" in part:
                wins = int(part.split(":")[1].strip())
            elif "Losses" in part:
                losses = int(part.split(":")[1].strip())
            elif "Draws" in part:
                draws = int(part.split(":")[1].strip())
        mazos.append({
            "Jugador": jugador,
            "Comandante": comandante,
            "Posición": posicion,
            "Wins": wins,
            "Losses": losses,
            "Draws": draws,
            "URL Mazo": url_mazo
        })
    return mazos

def verificar_mazo_publico(url):
    deck_id = url.split("/")[-1]
    api_url = f"https://api2.moxfield.com/v2/decks/all/{deck_id}"
    try:
        response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return True, deck_id, response.json(), 200, ""
    except requests.exceptions.HTTPError as http_err:
        return False, deck_id, None, response.status_code, str(http_err)
    except Exception as e:
        return False, deck_id, None, -1, str(e)

def guardar_cartas(deck_id, data):
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
    with open(os.path.join(CARTAS_DIR, f"{deck_id}.json"), "w", encoding="utf-8") as f:
        json.dump(cartas, f, indent=2, ensure_ascii=False)
    with open(os.path.join(RESPALDO_DIR, f"{deck_id}_raw.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return cartas

if st.button("🚀 Iniciar scraping"):
    torneos = obtener_lista_torneos()
    total_torneos = len(torneos)
    st.info(f"📅 Torneos encontrados: {total_torneos}")

    progress_bar = st.progress(0)
    text_bar = st.empty()

    log = []
    total_mazos = 0
    total_guardados = 0

    for i, torneo in enumerate(torneos):
        html = obtener_html_torneo(torneo["slug"])
        mazos = extraer_mazos(html)
        for mazo in mazos:
            total_mazos += 1
            ok, deck_id, data, status, error_msg = verificar_mazo_publico(mazo["URL Mazo"])
            resultado = {
                "Jugador": mazo["Jugador"],
                "Comandante": mazo["Comandante"],
                "URL": mazo["URL Mazo"],
                "DeckID": deck_id,
                "Status": status,
                "Error": error_msg
            }
            if ok:
                guardar_cartas(deck_id, data)
                jugador = limpiar_nombre(mazo["Jugador"])
                comandante = limpiar_nombre(mazo["Comandante"])
                nombre_csv = f"{jugador}_{comandante}.csv"
                df = pd.DataFrame([mazo])
                df.to_csv(os.path.join(MAZOS_DIR, nombre_csv), index=False)
                resultado["Guardado"] = True
                total_guardados += 1
            else:
                resultado["Guardado"] = False
            log.append(resultado)

        progreso = int((i + 1) / total_torneos * 100)
        progress_bar.progress(progreso)
        text_bar.markdown(f"🔄 Procesando torneo {i+1}/{total_torneos} — Mazos públicos: {total_guardados} / {total_mazos}")

    pd.DataFrame(log).to_csv(LOG_PATH, index=False)
    st.success(f"✅ Scraping completado: {total_guardados} mazos públicos descargados de {total_mazos} detectados.")
    st.download_button("📥 Descargar Log CSV", data=pd.DataFrame(log).to_csv(index=False), file_name="log_scraping_mazos.csv")
