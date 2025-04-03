from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import time

def extraer_cartas_moxfield(url):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Ejecutar sin abrir ventana
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )

    try:
        print("🌐 Cargando página...")
        driver.get(url)

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
