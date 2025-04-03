import requests

def extraer_id_desde_url(url):
    partes = url.strip("/").split("/")
    return partes[-1] if partes else None

def descargar_deck_txt(deck_id, export_id):
    api_url = f"https://api.moxfield.com/v2/decks/all/{deck_id}/download?exportId={export_id}&arenaOnly=false"
    response = requests.get(api_url)
    if response.status_code == 200:
        file_name = f"deck_{deck_id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Deck guardado como '{file_name}'")
    else:
        print(f"❌ Error al descargar el deck: {response.status_code}")

if __name__ == "__main__":
    url = input("🔗 Pega el link del mazo de Moxfield: ").strip()
    export_id = input("🔁 Pega el exportId del deck (parámetro exportId en la URL): ").strip()
    deck_id = extraer_id_desde_url(url)
    if deck_id and export_id:
        descargar_deck_txt(deck_id, export_id)
    else:
        print("⚠️ Faltan datos: asegúrate de proporcionar URL y exportId.")
