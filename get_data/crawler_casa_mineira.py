# Author - Leonardo Duarte Malta de Abreu 
# Github - leonardodma

# Imports Bibliotecas Básicas
from numpy.lib.function_base import append
import pandas as pd 
import numpy as np
import time
import os, os.path
from pathlib import Path
from tqdm import tqdm
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


class Crawler_CasaMineira():
    def __init__(self, webdriver):
        # Variável para guardar os dados coletados
        self.data_casa_mineira = {}

        # Chrome Driver
        self.driver = webdriver

        # Dom Xpath
        warnings.simplefilter('ignore', InsecureRequestWarning)
        self.ua = UserAgent()

    def seleciona_tipo(self, tipo_imovel):
        time.sleep(3)
        # O que é imovel misto?
        if tipo_imovel == "Apartamento":
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//option[contains(@value, 'apartamento')]")))[0].click()
        elif tipo_imovel  == "Apartamento Cobertura":
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//option[contains(@value, 'cobertura')]")))[0].click()
        elif tipo_imovel == "Casa Condomínio": 
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//option[contains(@value, 'casa-em-condominio')]")))[0].click()
        elif tipo_imovel == "Casa Residencial":
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//option[contains(@value, 'casa')]")))[0].click()
        elif tipo_imovel == "Sala Comercial":
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//option[contains(@value, 'sala-andar')]")))[0].click()
        elif tipo_imovel == "Casa Comercial":
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//option[contains(@value, 'loja')]")))[0].click()
        elif tipo_imovel == "Terreno":
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//option[contains(@value, 'lote')]")))[0].click()
        
    def properties_url(self, search_str, tipo_imovel):

        self.driver.get('https://www.casamineira.com.br/venda')
        
        # Colocar string de pesquisa 
        search_box = WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//input[contains(@class, 'form-control')]")))[0]
        search_box.send_keys(search_str)

        # Esperar tempo para aparecer as sugestões
        time.sleep(3)

        # Selecionar a primeira sugestão 
        search_box.send_keys(Keys.ARROW_DOWN)
        search_box.send_keys(Keys.RETURN)

        # Abrir Caixa de Seleção dos tipos de imóveis 
        time.sleep(4)
        WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//select[contains(@class, 'form-control')]")))[0].click()
        self.seleciona_tipo(tipo_imovel)
        time.sleep(4)


        return self.driver.current_url
    

    def next_page(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(@class, 'page-link Paginacao_link__')]")))[0]
            return True
        except:
            return False


    def get_data(self, search_str, tipo_imovel):
        main_URL = self.properties_url(search_str, tipo_imovel)
        time.sleep(2)
        print('\n\n')

        cidades = []
        bairros = []
        enderecos = []
        areas = []
        quartos = []
        banheiros = [] 
        precos = []
        links = []

        end = False
        pagina = 1

        while not end:
            if pagina == 1:
                URL = main_URL
            else:
                URL = main_URL+f'?pagina={pagina}'

            print(URL)
            self.driver.get(URL)
            time.sleep(2)

            for my_elem in WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'Imovel_Imovel__')]"))):
                informacoes = my_elem.text.split('\n')

                # Endereço 
                endereco = informacoes[1]
                cidades.append(endereco.split('-')[0].split(',')[1].strip())
                bairros.append(endereco.split('-')[0].split(',')[0].strip())
                enderecos.append("")
                
                # Área
                if informacoes[3] == 'de área':
                    try:
                        areas.append(int(informacoes[2].split(" ")[0].strip()))
                    except:
                        areas.append(int(round(float(informacoes[2].split(" ")[0].strip()))))
                else:
                    areas.append(0)
                
                # Quartos
                if informacoes[5] == 'quartos':
                    quartos.append(informacoes[4].strip())
                else:
                    quartos.append("")
                
                # Banheiros
                if informacoes[7] == 'banheiro' or informacoes[7] == 'banheiros':
                    banheiros.append(informacoes[6].strip())
                else:
                    banheiros.append("")
                
                # Preço
                preco_encontrado = False
                for info in informacoes:
                    if info[0:2] == 'R$':
                        precos.append(info)
                        preco_encontrado = True
                
                if not preco_encontrado:
                    precos.append("")
                

                links.append(my_elem.find_element_by_xpath(".//a[contains(@class, 'Imovel_tituloLink')]").get_attribute('href'))
                    
            pagina += 1

            if pagina > 6 or not self.next_page():
                end = True

        self.data_casa_mineira['Cidade'] = cidades
        self.data_casa_mineira['Bairro'] = bairros
        self.data_casa_mineira['Endereço'] = enderecos
        self.data_casa_mineira['Área'] = areas
        self.data_casa_mineira['Quartos'] = quartos
        self.data_casa_mineira['Banheiros'] = banheiros
        self.data_casa_mineira['Preço'] = precos
        self.data_casa_mineira['Link'] = links

        return self.data_casa_mineira
