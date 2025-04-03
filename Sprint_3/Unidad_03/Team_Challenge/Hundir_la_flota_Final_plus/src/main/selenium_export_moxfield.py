from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import os

def descargar_txt_desde_moxfield(deck_url, nombre_archivo):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        print(f"🌐 Cargando {deck_url}")
        driver.get(deck_url)

        # Esperar que el botón Export esté visible y hacer clic
        try:
            export_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export')]"))
            )
            export_btn.click()
        except:
            print("⚠️ Botón 'Export' no encontrado con texto. Intentando por testid...")
            export_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='export-button']"))
            )
            export_btn.click()
        time.sleep(1)

        # Hacer clic en la opción "Text"
        text_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Text')]"))
        )
        text_btn.click()
        time.sleep(1)

        # Capturar el contenido del modal
        pre_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "pre"))
        )
        contenido = pre_element.text

        # Guardar el contenido en un archivo .txt
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

        print(f"✅ Guardado como {nombre_archivo}")

    except Exception as e:
        print(f"❌ Error con {deck_url}: {e}")
        # Intento adicional: guardar HTML visible para depurar
        try:
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("📄 HTML visible guardado en debug_page.html")
        except:
            pass
    finally:
        driver.quit()

if __name__ == "__main__":
    # Puedes cambiar esta URL por cualquier deck
    test_url = "https://www.moxfield.com/decks/G876JvoAV0OLvmszByXm2g"
    descargar_txt_desde_moxfield(test_url, "deck_exportado.txt")
