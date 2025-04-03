import requests

def extraer_id_desde_url(url):
    partes = url.strip("/").split("/")
    return partes[-1] if partes else None

def descargar_deck_json(deck_id):
    api_url = f"https://api.moxfield.com/v2/decks/{deck_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://www.moxfield.com/decks/{deck_id}",
        "Origin": "https://www.moxfield.com",
        "Connection": "keep-alive"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al descargar el deck: {response.status_code}")
        return None

def guardar_nombres_txt(data, deck_id):
    nombres = []
    for section in data.get("mainboard", {}).values():
        for card_id, card_info in section.items():
            nombre = card_info["card"]["name"]
            cantidad = card_info["quantity"]
            nombres.extend([nombre] * cantidad)

    with open(f"deck_{deck_id}_nombres.txt", "w", encoding="utf-8") as f:
        for nombre in nombres:
            f.write(nombre + "\n")

    print(f"✅ Nombres de cartas guardados en 'deck_{deck_id}_nombres.txt'")

if __name__ == "__main__":
    url = input("🔗 Pega el link del mazo de Moxfield: ").strip()
    deck_id = extraer_id_desde_url(url)
    if deck_id:
        data = descargar_deck_json(deck_id)
        if data:
            guardar_nombres_txt(data, deck_id)
    else:
        print("⚠️ No se pudo extraer el ID del deck.")
