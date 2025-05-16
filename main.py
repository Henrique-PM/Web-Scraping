# from chat_posters import analise_chat_posters
# from chat_redes_sociais import analise_chat_redes
# from chat_youtube import analise_chat_youtube
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

INSTAGRAM_USER = ""
INSTAGRAM_PASS = ""


def criar_pastas():
    categorias = ['basket_posters', 'basket_redes_sociais', 'basket_youtube']
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

        # Remover popups, se existirem
        try:
            driver.execute_script("""
                let modal = document.querySelector('div[role="dialog"]');
                if (modal) { modal.remove(); }
            """)
        except Exception as e:
            print("Erro ao tentar remover o popup:", e)

        if 'pinterest.com' in url:
            try:
                # Scroll para carregar mais imagens (melhorado)
                for _ in range(5):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    # Tentar fechar pop-ups se aparecerem
                    try:
                        driver.find_element(By.CSS_SELECTOR, '[data-test-id="close-button"]').click()
                    except:
                        pass

                # Encontrar todos os elementos de imagem (seletor mais confiável)
                images = driver.find_elements(By.CSS_SELECTOR, 'img[src*="pinimg.com"]')
                
                # Filtrar URLs únicas
                urls = list({img.get_attribute('src') for img in images if img.get_attribute('src')})
                
                # Substituir por URL de maior resolução quando possível
                urls = [url.replace('/236x/', '/originals/') for url in urls]
                
                print(f'Pinterest: {len(urls)} imagens encontradas para download.')

                os.makedirs(f'referencias/{categoria}', exist_ok=True)

                for i, url_img in enumerate(urls[:4]):  # baixando só 4 primeiras
                    try:
                        response = requests.get(url_img, headers={'User-Agent': 'Mozilla/5.0'})
                        if response.status_code == 200:
                            caminho_img = f'referencias/{categoria}/{nome_arquivo}_img_{i}.jpg'
                            with open(caminho_img, 'wb') as f:
                                f.write(response.content)
                            print(f'Imagem Pinterest salva: {caminho_img}')
                        else:
                            print(f'Erro ao baixar {url_img}: status {response.status_code}')
                    except Exception as e:
                        print(f'Erro ao baixar {url_img}: {e}')
                        
            except Exception as e:
                print(f'Erro geral ao processar Pinterest: {e}')
        # Depois, tirar screenshots normalmente
        for i in range(qtd_prints):
            if rolar and i > 0:
                rolar_pagina(driver, vezes=1, intervalo=2)

            nome_final = f'{nome_arquivo}_{i+1}.png' if multiplos else f'{nome_arquivo}.png'
            caminho = f'referencias/{categoria}/{nome_final}'
            driver.save_screenshot(caminho)
            print(f'Screenshot salva em: {caminho}')

    finally:
        driver.quit()



if __name__ == "__main__":
    criar_pastas()

    urls = {
        'basket_posters': [
            {
                'nome': 'flyer_basquete',
                'url': 'https://br.pinterest.com/search/pins/?q=basketball%20flyer&rs=guide&journey_depth=1',
                'rolar': True,
                'espera': 7,
                'multiplos': True,
                'qtd_prints': 4,
                'login': False
            },
            {
                'nome': 'basquete_design',
                'url': 'https://br.pinterest.com/search/pins/?q=basketball%20design&rs=ac',
                'rolar': True,
                'espera': 7,
                'multiplos': True,
                'qtd_prints': 4,
                'login': False
            },
        ],
        'basket_redes_sociais': [
            {
                'nome': 'nba',
                'url': 'https://www.instagram.com/nba/',
                'rolar': True,
                'espera': 8,
                'multiplos': True,
                'qtd_prints': 2,
                'login': True
            },
            {
                'nome': 'espn_basketball',
                'url': 'https://www.instagram.com/nbaonespn/',
                'rolar': True,
                'espera': 8,
                'multiplos': True,
                'qtd_prints': 2,
                'login': True
            }
        ],
        'basket_youtube': [
            {
                'nome': 'nba_official',
                'url': 'https://www.youtube.com/@NBA/videos',
                'rolar': True,
                'espera': 3,
                'multiplos': True,
                'qtd_prints': 3,
                'login': False
            },
            {
                'nome': 'nba_brasil basketball',
                'url': 'https://www.youtube.com/@nbabrasil/videos',
                'rolar': True,
                'espera': 3,
                'multiplos': True,
                'qtd_prints': 3,
                'login': False
            }
        ]
    }

    for categoria, itens in urls.items():
        for item in itens:
            capturar_pagina(
                url=item['url'],
                categoria=categoria,
                nome_arquivo=item['nome'],
                rolar=item['rolar'],
                espera=item['espera'],
                multiplos=item['multiplos'],
                qtd_prints=item['qtd_prints'],
                login=item.get('login', False)
            )

    # Análises ao final
    # analise_chat_redes('referencias/basket_redes_sociais')
    # analise_chat_posters('referencias/basket_posters')
    # analise_chat_youtube('referencias/basket_youtube')
