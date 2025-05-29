import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ==================== CONFIGURAÇÃO DE LOGIN ====================
INSTAGRAM_USER = ""
INSTAGRAM_PASS = ""

def criar_pastas():
    categorias = ['posters', 'redes_sociais','youtube']
    for cat in categorias:
        os.makedirs(f'referencias/{cat}', exist_ok=True)

def login_instagram(driver, espera=5):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(espera)
    try:
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys(INSTAGRAM_USER)
        password_input.send_keys(INSTAGRAM_PASS)

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        time.sleep(espera)

        try:
            not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Agora não')]")
            not_now.click()
            time.sleep(espera)
        except:
            pass
    except Exception as e:
        print("Erro ao fazer login no Instagram:", e)


def rolar_pagina(driver, vezes=5, intervalo=2):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    for i in range(vezes):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(intervalo)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            print(f"[Scroll {i+1}] Nenhuma mudança detectada. Encerrando scroll.")
            break
        last_height = new_height
        print(f"[Scroll {i+1}] Scroll realizado, nova altura da página: {new_height}")



def capturar_pagina(url, categoria, nome_arquivo, rolar=False, espera=5, multiplos=False, qtd_prints=1, login=False):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--headless") 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1920, 1080)

    try:
        if login:
            login_instagram(driver, espera=espera)

        driver.get(url)
        time.sleep(espera)

        try:
            driver.execute_script("""
                let modal = document.querySelector('div[role="dialog"]');
                if (modal) { modal.remove(); }
            """)
        except Exception as e:
            print("Erro ao tentar remover o popup:", e)

        for i in range(qtd_prints):
            if rolar and i > 0:
                rolar_pagina(driver, vezes=1, intervalo=2)

            nome_final = f'{nome_arquivo}_{i+1}.png' if multiplos else f'{nome_arquivo}.png'
            caminho = f'referencias/{categoria}/{nome_final}'
            driver.save_screenshot(caminho)
            print(f'Screenshot salva em: {caminho}')

    finally:
        driver.quit()
