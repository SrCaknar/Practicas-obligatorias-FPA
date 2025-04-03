import requests
import pandas as pd
import json

def extraer_id_desde_url(url):
    partes = url.strip("/").split("/")
    return partes[-1] if partes else None

def descargar_deck(deck_id):
    api_url = f"https://api2.moxfield.com/v2/decks/all/{deck_id}/export"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al descargar el deck: {response.status_code}")
        return None

def guardar_deck(deck_json, deck_id):
    # Guardar como JSON crudo
    with open(f"deck_{deck_id}.json", "w", encoding="utf-8") as f:
        json.dump(deck_json, f, indent=2)

    # Convertir a CSV simple
    cards = []
    for section in deck_json.get("mainboard", []):
        for card in deck_json["mainboard"][section]:
            entry = deck_json["mainboard"][section][card]
            cards.append({
                "Nombre": entry["card"]["name"],
                "Cantidad": entry["quantity"],
                "Tipo": entry["card"]["type_line"],
                "Costo de maná": entry["card"]["mana_value"],
            })

    df = pd.DataFrame(cards)
    df.to_csv(f"deck_{deck_id}.csv", index=False)
    print(f"✅ Deck guardado como 'deck_{deck_id}.csv' y 'deck_{deck_id}.json'")

if __name__ == "__main__":
    url = input("🔗 Pega el link del mazo de Moxfield: ").strip()
    deck_id = extraer_id_desde_url(url)
    if deck_id:
        deck_data = descargar_deck(deck_id)
        if deck_data:
            guardar_deck(deck_data, deck_id)
    else:
        print("⚠️ No se pudo extraer el ID del deck.")
