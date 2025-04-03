import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://mtgtop8.com"

def obtener_cartas_de_mazo(deck_url):
    cartas = []
    try:
        r = requests.get(deck_url)
        soup = BeautifulSoup(r.text, "html.parser")
        secciones = soup.find_all("table", {"class": "Stable"})

        for seccion in secciones:
            filas = seccion.find_all("tr")
            for fila in filas:
                cols = fila.find_all("td")
                if len(cols) >= 2:
                    cantidad = cols[0].text.strip()
                    nombre = cols[1].text.strip()
                    if cantidad.isdigit():
                        cartas.append({
                            "nombre": nombre,
                            "cantidad": int(cantidad)
                        })
    except Exception as e:
        print(f"❌ Error al procesar mazo {deck_url}: {e}")
    return cartas

def procesar_base_mazos(df_mazos):
    registros = []
    for _, row in df_mazos.iterrows():
        print(f"🔄 Procesando mazo: {row['comandante']} - {row['deck_url']}")
        cartas = obtener_cartas_de_mazo(row["deck_url"])
        for carta in cartas:
            registros.append({
                "evento": row["evento"],
                "fecha": row["fecha"],
                "comandante": row["comandante"],
                "deck_url": row["deck_url"],
                "carta": carta["nombre"],
                "cantidad": carta["cantidad"]
            })
    df_cartas = pd.DataFrame(registros)
    df_cartas.to_csv("base_cartas_mtgtop8.csv", index=False)
    print("✅ Base de datos guardada como 'base_cartas_mtgtop8.csv'")

if __name__ == "__main__":
    df = pd.read_csv("analisis_mazos_mtgtop8.csv")
    procesar_base_mazos(df)
