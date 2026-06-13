"""
Script Selenium: inicia sesion como organizador y crea un evento nuevo
desde el formulario de la pagina. Cada accion esta espaciada 1-2 segundos.

Crear eventos solo esta permitido para roles admin u organizer, por eso
se loguea con un usuario organizador semilla.

Uso:
    1) Levantar la app en otra terminal:
         uvicorn app.main:app --reload
    2) Ejecutar este script:
         python Selenium/crear_evento.py
"""

import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


URL = "http://127.0.0.1:8000"

USERNAME = "organizer1"
PASSWORD = "org123"

EVENT_NAME = f"Evento Selenium {int(time.time())}"
EVENT_DATE = "2026-12-01"
EVENT_CAPACITY = "150"
EVENT_PRICE = "5000"


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

        wait.until(EC.presence_of_element_located((By.ID, "loginUsername")))
        driver.find_element(By.ID, "loginUsername").send_keys(USERNAME)
        pausa()
        driver.find_element(By.ID, "loginPassword").send_keys(PASSWORD)
        pausa()
        driver.find_element(By.ID, "loginButton").click()
        print(f"Login enviado: {USERNAME}")
        pausa()

        wait.until(EC.text_to_be_present_in_element((By.ID, "sessionInfo"), USERNAME))
        print("Sesion iniciada como organizador")
        pausa()

        wait.until(EC.visibility_of_element_located((By.ID, "eventName")))
        driver.find_element(By.ID, "eventName").send_keys(EVENT_NAME)
        pausa()
        driver.find_element(By.ID, "eventDate").send_keys(EVENT_DATE)
        pausa()
        driver.find_element(By.ID, "eventCapacity").send_keys(EVENT_CAPACITY)
        pausa()
        driver.find_element(By.ID, "eventPrice").send_keys(EVENT_PRICE)
        pausa()
        driver.find_element(By.ID, "createEventButton").click()
        print(f"Evento enviado: {EVENT_NAME}")
        pausa()

        status = wait.until(EC.visibility_of_element_located((By.ID, "status")))
        print(f"Respuesta de la app: {status.text}")

        time.sleep(5)
        print("Listo (5 segundos de espera completados)")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
