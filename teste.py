from os import link
from re import search
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from pathlib import Path

chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver_win32\chromedriver.exe')
options = Options()
options.add_argument("--window-size=1920x1800")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)

def seleciona_tipo(tipo_imovel):
    time.sleep(3)
    if tipo_imovel == "Apartamento" or tipo_imovel  == "Apartamento Cobertura":
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkbox-Apartamento - 2"]')))[0].click()
    elif tipo_imovel == "Casa Condomínio" or tipo_imovel == "Casa Residencial": 
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkbox-Casa - 1"]')))[1].click()
    elif tipo_imovel == "Sala Comercial" or tipo_imovel == "Casa Comercial":
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkbox-Comercial - 1005"]')))[3].click()
    elif tipo_imovel == "Terreno":
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="checkbox-Terreno - 1003"]')))[2].click()


def properties_url(search_str, tipo_imovel):
        driver.get('https://www.imovelweb.com.br/imoveis-venda.html')

        # Remove erro
        time.sleep(10)
        try:
            driver.find_element_by_xpath('//*[@id="modalContent"]/div/button').click()
        except:
            pass

        # Clica em ver filtros  
        time.sleep(2)
        ver_filtros = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'listFilterButton')]")))[0]
        ver_filtros.click()

        # Colocar string de pesquisa 
        search_box = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="filter-list"]/div[2]/fieldset[1]/div[2]/div/div[2]/div/div[1]/input')))[0]
        search_box.send_keys(search_str)

        # Esperar tempo para aparecer as sugestões
        time.sleep(3)

        # Selecionar a primeira sugestão 
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.RETURN)

        # Abrir Caixa de Seleção dos tipos de imóveis 
        div_selecao = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//fieldset[contains(@class, ' realestateType ')]")))[0]
        driver.execute_script("arguments[0].scrollIntoView();", div_selecao)

        time.sleep(3)
        ver_mais = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'ViewmoreButton-sifqb3-1 knMuqW')]")))[0]
        ver_mais.click()
        driver.execute_script("arguments[0].scrollIntoView();", div_selecao)

        # Seleciona Imóveis
        driver.execute_script("arguments[0].scrollIntoView();", div_selecao)
        seleciona_tipo(tipo_imovel)
        time.sleep(4)

        # Aplica filtros 
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'filter-result-button')]")))[0].click()

        return driver.current_url


url = properties_url("Campo Limpo, São Paulo", "Apartamento")
print(url)
time.sleep(2)
"""
for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'Imovel_Imovel__')]"))):
    informacoes = my_elem.text.split('\n')

    

    #url = my_elem.find_element_by_xpath(".//a[contains(@class, 'Imovel_tituloLink')]").get_attribute('href')

    
    #print(cidade, bairro, rua, area, quarto, banheiro, preco, url)
    print('==================================================')

"""
driver.quit()