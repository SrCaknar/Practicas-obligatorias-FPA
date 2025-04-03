from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def extraer_cartas_moxfield(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Ejecutar en modo headless moderno
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )  # Versión fija según Chrome local

    try:
        print("🌐 Cargando página...")
        driver.get(url)

        # Esperar a que las cartas se carguen
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.card-row"))
        )

        time.sleep(2)

        filas = driver.find_elements(By.CSS_SELECTOR, "tr.card-row")
        print(f"📄 Filas encontradas: {len(filas)}")

        cartas = []
        for fila in filas:
            try:
                cantidad = fila.find_element(By.CSS_SELECTOR, ".quantity-col").text.strip()
                nombre = fila.find_element(By.CSS_SELECTOR, ".card-name-col").text.strip()
                tipo = fila.find_element(By.CSS_SELECTOR, ".type-col").text.strip()
                cartas.append({"Cantidad": cantidad, "Nombre": nombre, "Tipo": tipo})
            except Exception as e:
                print("⚠️ Error leyendo fila:", e)
                continue

        if cartas:
            df = pd.DataFrame(cartas)
            df.to_csv("cartas_extraidas.csv", index=False)
            print("✅ Cartas extraídas y guardadas en 'cartas_extraidas.csv'.")
        else:
            print("⚠️ No se extrajo ninguna carta. Verifica la estructura de la página.")

    except Exception as err:
        print("❌ Error general:", err)

    finally:
        driver.quit()

if __name__ == "__main__":
    url = input("🔗 Pega el link del mazo de Moxfield: ").strip()
    extraer_cartas_moxfield(url)
