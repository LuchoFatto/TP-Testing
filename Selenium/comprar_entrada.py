"""
Script Selenium: registra un cliente nuevo, inicia sesion y compra una
entrada a un evento activo. Cada accion esta espaciada 1-2 segundos.

Uso:
    1) Levantar la app en otra terminal:
         uvicorn app.main:app --reload
    2) Ejecutar este script:
         python Selenium/comprar_entrada.py
"""

import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


URL = "http://127.0.0.1:8000"

USERNAME = f"comprador_{int(time.time())}"
PASSWORD = "test123"

EVENT_ID = 1
QUANTITY = "1"


def pausa():
    """Espera entre 1 y 2 segundos para espaciar las acciones."""
    time.sleep(random.uniform(1, 2))


def main():
    driver = webdriver.Chrome(service=Service())

    try:
        driver.get(URL)
        print(f"Aplicacion abierta en {URL}")
        pausa()

        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.ID, "registerUsername")))
        driver.find_element(By.ID, "registerUsername").send_keys(USERNAME)
        pausa()
        driver.find_element(By.ID, "registerPassword").send_keys(PASSWORD)
        pausa()
        driver.find_element(By.ID, "registerButton").click()
        print(f"Usuario registrado: {USERNAME}")
        pausa()

        driver.find_element(By.ID, "loginUsername").send_keys(USERNAME)
        pausa()
        driver.find_element(By.ID, "loginPassword").send_keys(PASSWORD)
        pausa()
        driver.find_element(By.ID, "loginButton").click()
        print(f"Login enviado: {USERNAME}")
        pausa()

        wait.until(EC.text_to_be_present_in_element((By.ID, "sessionInfo"), USERNAME))
        print("Sesion iniciada")
        pausa()

        qty_input = wait.until(
            EC.visibility_of_element_located((By.ID, f"qty-{EVENT_ID}"))
        )
        qty_input.clear()
        qty_input.send_keys(QUANTITY)
        pausa()
        driver.find_element(
            By.XPATH, f"//button[contains(@onclick, 'buyTickets({EVENT_ID})')]"
        ).click()
        print(f"Compra enviada: evento {EVENT_ID}, cantidad {QUANTITY}")
        pausa()

        status = wait.until(EC.visibility_of_element_located((By.ID, "status")))
        print(f"Respuesta de la app: {status.text}")

        time.sleep(5)
        print("Listo (5 segundos de espera completados)")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
