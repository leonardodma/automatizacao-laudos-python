# Author - Leonardo Duarte Malta de Abreu 
# Github - leonardodma

# Imports Bibliotecas Básicas
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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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

    def seleciona_tipo(self, tipo_imovel):
        if tipo_imovel == "Apartamento":
            self.driver.find_element_by_xpath('//*[@id="l-select1"]/optgroup[2]/option[1]').click()
        elif tipo_imovel  == "Apartamento Cobertura":
            self.driver.find_element_by_xpath('//*[@id="l-select1"]/optgroup[2]/option[7]').click()
        elif tipo_imovel == "Casa Condomínio": 
            self.driver.find_element_by_xpath('//*[@id="l-select1"]/optgroup[2]/option[5]').click()
        elif tipo_imovel == "Casa Residencial":
            self.driver.find_element_by_xpath('//*[@id="l-select1"]/optgroup[2]/option[4]').click()
        elif tipo_imovel == "Sala Comercial":
            self.driver.find_element_by_xpath('//*[@id="l-select1"]/optgroup[3]/option[2]').click()
        elif tipo_imovel == "Casa Comercial":
            self.driver.find_element_by_xpath('//*[@id="l-select1"]/optgroup[3]/option[3]').click()
        elif tipo_imovel == "Terreno":
            terreno = self.driver.find_element_by_xpath('//*[@id="l-select1"]/optgroup[2]/option[10]')
            time.sleep(1)
            self.driver.execute_script("arguments[0].scrollIntoView();", terreno)
            terreno.click()


    def properties_url(self, search_str, tipo_imovel):

        self.driver.get('https://www.zapimoveis.com.br/')
        
        # Colocar string de pesquisa 
        search_box = self.driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/div/div/div/input')
        search_box.send_keys(search_str)

        # Esperar tempo para aparecer as sugestões
        time.sleep(3)

        # Selecionar a primeira sugestão 
        search_box.send_keys(Keys.RETURN)

        # Abrir Caixa de Seleção dos tipos de imóveis 
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="l-select1"]').click()
        self.seleciona_tipo(tipo_imovel)

        # Finaliza pesquisa
        self.driver.find_element_by_xpath('//*[@id="app"]/section/section[1]/div/section/form/div/div[2]/button').click()
        time.sleep(2)

        barra = str(r' / ')[1]

        time.sleep(4)
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
                    quarto = list(map(str, data[i]["listing"]["bedrooms"])) 
                    if len(quarto) > 0:
                        quartos.append("-".join(quarto))
                    elif len(quarto) == 0:
                        quartos.append('')
                    else:
                        quartos.append(quartos[0])

                    # Banheiros
                    try:
                        banheiros.append(str(data[i]["listing"]["bathrooms"][0]))
                    except:
                        banheiros.append('0')
                        
                    # Vagas
                    try:
                        vagas.append(str(data[i]["listing"]["parkingSpaces"][0]))
                    except:
                        vagas.append('0')
                    
                    # Preços
                    precos.append(data[i]["listing"]["pricingInfo"]["price"])

                    # Links
                    links.append('https://www.zapimoveis.com.br'+data[i]["listing"]["link"])

                end = self.next_page(dom)
                    
            pagina += 1

            if pagina > 6:
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
