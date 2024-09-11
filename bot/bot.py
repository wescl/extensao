from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import subprocess

CHROME_DRIVER_PATH = './chromedriver.exe'
CHROME_PROFILE_PATH = 'C:/Users/wescl/AppData/Local/Google/Chrome/User Data'
PROFILE_NAME = 'Default'

def open_and_fill_email():
    try:
        service = Service(CHROME_DRIVER_PATH)
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-data-dir={CHROME_PROFILE_PATH}')
        options.add_argument(f'profile-directory={PROFILE_NAME}')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--remote-debugging-address=0.0.0.0') 

        print("Inicializando o WebDriver...")
        driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver iniciado com sucesso.")

        url = "https://www.themachinesarena.com/dashboard/teams"
        print(f"Navegando para {url}...")
        driver.get(url)
        time.sleep(5) 

        # Clicar no primeiro elemento
        select_element = driver.find_element(By.CSS_SELECTOR, 'div[role="combobox"]')
        select_element.click()
        time.sleep(2)

        # Clicar no item do menu
        menu_item = driver.find_element(By.CSS_SELECTOR, 'li[data-value="50"]')
        menu_item.click()
        time.sleep(2)

        # Lista para armazenar todos os dados
        all_td_data = []

        # Função para listar todos os <td> dentro do elemento específico
        def list_table_data_within_element():
            nonlocal all_td_data
            # Localizar o elemento específico
            specific_element = driver.find_element(By.CSS_SELECTOR, '#__next > div.MuiBox-root.mui-frpz03 > div > div.MuiBox-root.mui-kjafn5 > main > div > div > div > div > div.MuiBox-root.mui-aaygnb > div:nth-child(4) > div.MuiBox-root.mui-15pe2ue')
            
            # Encontrar a tabela dentro do elemento específico
            table = specific_element.find_element(By.CSS_SELECTOR, 'table.MuiTable-root')
            rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
            for row in rows:
                cells = row.find_elements(By.CSS_SELECTOR, 'td')
                cell_texts = [cell.text for cell in cells]
                all_td_data.append(cell_texts)

        # Lista inicial dos dados da tabela
        list_table_data_within_element()

        # Loop para clicar no botão e listar os dados
        while True:
            try:
                # Localizar o botão de navegação
                nav_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')
                
                # Verificar se o botão está visível e clicável
                if not nav_button.is_displayed() or not nav_button.is_enabled():
                    print("Botão de navegação não está mais visível ou não está habilitado. Encerrando o script.")
                    break

                # Clicar no botão de navegação
                nav_button.click()
                time.sleep(2)  # Esperar a página atualizar

                # Listar todos os <td> novamente
                list_table_data_within_element()

            except Exception as e:
                print(f"Erro ao tentar clicar no botão de navegação ou listar os dados: {e}")
                break

        # Salvar os dados em um arquivo JSON
        with open('table_data.json', 'w') as f:
            json.dump(all_td_data, f, indent=4)

        print("Dados salvos em 'table_data.json'.")

        # Executar o script insert.py
        subprocess.run(['python', 'insert.py'], check=True)
        print("Script 'insert.py' executado com sucesso.")

        print("Script em execução. Pressione Ctrl + C para sair.")
        while True:
            time.sleep(1)  # Dormir por 1 segundo para não consumir 100% da CPU

    except Exception as e:
        print(f"Erro: {e}")
    except KeyboardInterrupt:
        print("Interrupção recebida. Fechando o WebDriver...")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("WebDriver fechado.")

if __name__ == "__main__":
    open_and_fill_email()
