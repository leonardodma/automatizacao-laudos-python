# Author - Leonardo Duarte Malta de Abreu 
# Github - leonardodma

# Imports Bibliotecas Básicas
import math
from numpy.lib.function_base import append
import pandas as pd 
import numpy as np
import time
import os, os.path
from pathlib import Path
import re
import json
from statistics import mean


# Imports Selenium (Navegador Web) - Obter Links dos imóveis 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# Imports Web Scraper - Obter Base de dados 
from bs4 import BeautifulSoup
from lxml import etree
import requests
import warnings
from fake_useragent import UserAgent
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Crawler_ZapImoveis():
    def __init__(self, webdriver):
        # Variável para guardar os dados coletados
        self.data_zap_imoveis = {}

        # Chrome Driver
        self.driver = webdriver

        # Dom Xpath
        warnings.simplefilter('ignore', InsecureRequestWarning)
        self.ua = UserAgent()
    
    def obtem_elemento(self, xpath):
        return wait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def seleciona_tipo(self, elemento, tipo_imovel):
        if tipo_imovel == "Apartamento":
            elemento.send_keys(Keys.DOWN)
        elif tipo_imovel  == "Apartamento Cobertura":
            for i in range(7):
                elemento.send_keys(Keys.RETURN)
        elif tipo_imovel == "Casa Condomínio": 
            for i in range(5):
                elemento.send_keys(Keys.RETURN)
        elif tipo_imovel == "Casa Residencial":
            for i in range(4):
                elemento.send_keys(Keys.RETURN)
        elif tipo_imovel == "Sala Comercial":
            for i in range(13):
                elemento.send_keys(Keys.RETURN)
        elif tipo_imovel == "Casa Comercial":
            for i in range(14):
                elemento.send_keys(Keys.RETURN)
        elif tipo_imovel == "Terreno":
            for i in range(10):
                elemento.send_keys(Keys.RETURN)



    def properties_url(self, search_str, tipo_imovel):

        self.driver.get('https://www.zapimoveis.com.br/')

        # Aceitar Cookies
        aceitar_cookies = self.obtem_elemento('//*[@id="cookie-notifier-cta"]')
        aceitar_cookies.click()
        
        # Ajudar pra div de pesquisa
        div_pesquisa = self.obtem_elemento('//*[@id="app"]/section/section[2]/div/section/form')
        self.driver.execute_script("arguments[0].scrollIntoView();", div_pesquisa)

        # Colocar string de pesquisa 
        search_box = self.obtem_elemento('//*[@id="app"]/section/section[2]/div/section/form/div/div[2]/div/div/div/input')
        search_box.send_keys(search_str)

        # Selecionar a primeira sugestão 
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)

        # Abrir Caixa de Seleção dos tipos de imóveis 
        elemento = self.obtem_elemento('//*[@id="l-select1"]')
        elemento.click()
        self.seleciona_tipo(elemento, tipo_imovel)
        elemento.send_keys(Keys.RETURN)

        # Finaliza pesquisa
        self.obtem_elemento('//*[@id="app"]/section/section[2]/div/section/form/div/div[2]/button').click()

        barra = str(r' / ')[1]

        time.sleep(5)
        url = self.driver.current_url

        return barra.join(url.split(barra)[0:6])
    

    def qtd_anuncios(self, dom):
        qtd = 1
        idx_li = 1
        final = False

        while not final:
            try:
                dom.xpath(f'/html/body/main/section/div[3]/div[2]/section/div/div[{idx_li}]')[0]
                qtd += 1
                idx_li += 1
            except:
                final = True
        
        return qtd
    

    def next_page(self, dom):
        try:
            dom.xpath(f'/html/body/div[2]/main/div[4]/div[5]/div/ul/li[7]/a')[0]
            return True
        except:
            return False


    def get_data(self, search_str, tipo_imovel):
        main_URL = self.properties_url(search_str, tipo_imovel)
        time.sleep(2)
        self.driver.quit()
        print('\n\n')
        estados = []
        cidades = []
        bairros = []
        enderecos = []
        areas = []
        quartos = []
        banheiros = []
        vagas = [] 
        precos = []
        links = []

        end = False
        pagina = 1

        while not end:
            if pagina == 1:
                URL = main_URL
            else:
                URL = main_URL+f'/?pagina={pagina}'

            print(URL)
            session = requests.Session()
            page = session.get(URL, headers={"User-Agent": str(self.ua.chrome)})

            if page.status_code == 200:
                soup = str(BeautifulSoup(page.content, 'html.parser'))
                dom = etree.HTML(soup)
                
                data = re.search(r'window.__INITIAL_STATE__=({.*})', soup).group(1)
                a = "".join(data.split(";")[0:-3])
                data = json.loads(a)['results']["listings"]

                for i in range(len(data)):
                    # Endereço
                    estados.append(data[i]["listing"]["address"]["stateAcronym"])
                    cidades.append(data[i]["link"]["data"]["city"])
                    bairros.append(data[i]["link"]["data"]["neighborhood"])

                    rua = data[i]["link"]["data"]["street"]
                    numero = str(data[i]["link"]["data"]["streetNumber"])

                    if len(rua) > 0 and len(numero) > 0:
                        enderecos.append(rua+', '+numero)
                    elif len(rua) > 0 and len(numero) != 0:
                        enderecos.append(rua)
                    else:
                        enderecos.append("")
                    
                    # Área
                    areas.append(int(mean(list(map(int, data[i]["listing"]["usableAreas"])))))

                    # Quartos
                    try:
                        quartos.append(int(mean(list(map(int, data[i]["listing"]["bedrooms"])))))
                    except:
                        quartos.append(0)

                    # Banheiros
                    try:
                        banheiros.append(int(mean(list(map(int, data[i]["listing"]["bathrooms"])))))
                    except:
                        banheiros.append(0)
                        
                    # Vagas
                    try:
                        vagas.append(int(mean(list(map(int, data[i]["listing"]["parkingSpaces"])))))
                    except:
                        vagas.append(0)
                    
                    # Preços
                    precos.append(data[i]["listing"]["pricingInfo"]["price"])

                    # Links
                    links.append('https://www.zapimoveis.com.br'+data[i]["listing"]["link"])

                end = self.next_page(dom)
                    
            pagina += 1

            if pagina > 8:
                end = True

        self.data_zap_imoveis['Estado'] = estados
        self.data_zap_imoveis['Cidade'] = cidades
        self.data_zap_imoveis['Bairro'] = bairros
        self.data_zap_imoveis['Endereço'] = enderecos
        self.data_zap_imoveis['Área'] = areas
        self.data_zap_imoveis['Quarto'] = quartos
        self.data_zap_imoveis['Banheiro'] = banheiros
        self.data_zap_imoveis['Vaga'] = vagas
        self.data_zap_imoveis['Preço'] = precos
        self.data_zap_imoveis['Link'] = links

        return self.data_zap_imoveis
