import requests
import pandas as pd

def extraer_id_desde_url(url):
    partes = url.strip("/").split("/")
    return partes[-1] if partes else None

def descargar_deck_json(deck_id):
    api_url = f"https://api2.moxfield.com/v2/decks/all/{deck_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al descargar el deck: {response.status_code}")
        return None

def procesar_y_guardar_deck(data, deck_id):
    cartas = []

    # Navegar por cada sección del mainboard
    for seccion in data.get("mainboard", {}).values():
        for carta_id, carta_info in seccion.items():
            nombre = carta_info["card"]["name"]
            cantidad = carta_info["quantity"]
            tipo = carta_info["card"]["type_line"]
            mana = carta_info["card"]["mana_value"]
            cartas.append({
                "Nombre": nombre,
                "Cantidad": cantidad,
                "Tipo": tipo,
                "CMC": mana
            })

    # Guardar como CSV
    df = pd.DataFrame(cartas)
    df.to_csv(f"deck_{deck_id}.csv", index=False)

    # Guardar como TXT estilo Moxfield
    with open(f"deck_{deck_id}.txt", "w", encoding="utf-8") as f:
        for carta in cartas:
            f.write(f"{carta['Cantidad']} {carta['Nombre']}
")

    print(f"✅ Deck guardado como 'deck_{deck_id}.csv' y 'deck_{deck_id}.txt'")

if __name__ == "__main__":
    url = input("🔗 Pega el link del mazo de Moxfield: ").strip()
    deck_id = extraer_id_desde_url(url)
    if deck_id:
        data = descargar_deck_json(deck_id)
        if data:
            procesar_y_guardar_deck(data, deck_id)
    else:
        print("⚠️ No se pudo extraer el ID del deck.")
