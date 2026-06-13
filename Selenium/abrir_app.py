"""
Script simple: abre la aplicacion en Chrome usando Selenium + chromedriver,
registra un usuario nuevo desde el formulario de la pagina y se queda 5
segundos inactivo antes de cerrar.

Uso:
    1) Levantar la app en otra terminal:
         uvicorn app.main:app --reload
    2) Ejecutar este script:
         python Selenium/abrir_app.py
"""

import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "http://127.0.0.1:8000"
USERNAME = f"alumno_{int(time.time())}"
PASSWORD = "test123"

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
        print(f"Usuario enviado: {USERNAME}")
        pausa()

        status = wait.until(EC.visibility_of_element_located((By.ID, "status")))
        print(f"Registro: {status.text}")
        pausa()

        driver.find_element(By.ID, "loginUsername").send_keys(USERNAME)
        pausa()
        driver.find_element(By.ID, "loginPassword").send_keys(PASSWORD)
        pausa()
        driver.find_element(By.ID, "loginButton").click()
        print(f"Login enviado: {USERNAME}")
        pausa()

        session = wait.until(
            EC.text_to_be_present_in_element((By.ID, "sessionInfo"), USERNAME)
        )
        print(f"Sesion iniciada: {driver.find_element(By.ID, 'sessionInfo').text}")

        time.sleep(5)
        print("Listo (5 segundos de espera completados)")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
