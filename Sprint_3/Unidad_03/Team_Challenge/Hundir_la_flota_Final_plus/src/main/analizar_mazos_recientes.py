import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Simulación de proceso: se espera recibir un CSV con columnas: url
def descargar_y_analizar_mazos(csv_path):
    df = pd.read_csv(csv_path)
    data_total = []

    for _, row in df.iterrows():
        url = row["url"]
        deck_id = url.strip("/").split("/")[-1]
        api_url = f"https://api.moxfield.com/v2/decks/{deck_id}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": url,
            "Origin": "https://www.moxfield.com",
        }

        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code != 200:
                print(f"⚠️ No se pudo descargar {url}")
                continue
            data = response.json()

            for section in data.get("mainboard", {}).values():
                for card_id, card_info in section.items():
                    data_total.append({
                        "deck_url": url,
                        "card_name": card_info["card"]["name"],
                        "quantity": card_info["quantity"],
                        "date": datetime.today().strftime("%Y-%m-%d")
                    })

        except Exception as e:
            print(f"❌ Error con {url}: {e}")

    if data_total:
        result_df = pd.DataFrame(data_total)
        result_df.to_csv("analisis_mazos_ultimos_3dias.csv", index=False)
        print("✅ Análisis guardado como 'analisis_mazos_ultimos_3dias.csv'")
    else:
        print("⚠️ No se pudo generar análisis.")

if __name__ == "__main__":
    entrada = input("📥 Ruta del archivo CSV con links de mazos recientes: ").strip()
    if os.path.exists(entrada):
        descargar_y_analizar_mazos(entrada)
    else:
        print("❌ Archivo no encontrado.")
