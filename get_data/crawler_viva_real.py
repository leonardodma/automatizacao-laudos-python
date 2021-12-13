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

# Imports Selenium (Navegador Web) - Obter Links dos imóveis 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# Imports Web Scraper - Obter Base de dados 
from bs4 import BeautifulSoup
from lxml import etree
import requests
import warnings
from fake_useragent import UserAgent
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Importe de Módulos
from parseadores.parseador_VivaReal import *


class Crawler_VivaReal():
    def __init__(self, webdriver):
        # Variável para guardar os dados coletados
        self.data_viva_real = {}

        # Chrome Driver
        self.driver = webdriver

        # Dom Xpath
        warnings.simplefilter('ignore', InsecureRequestWarning)
        self.ua = UserAgent()

    def obtem_elemento(self, xpath):
        return wait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def seleciona_tipo(self, tipo_imovel):
        # O que é imovel misto?
        if tipo_imovel == "Apartamento" or tipo_imovel == "Apartamento Cobertura":
            self.obtem_elemento('//*[@id="unit-type-APARTMENT|UnitSubType_NONE,DUPLEX,LOFT,STUDIO,TRIPLEX|RESIDENTIAL|APARTMENT"]').click()
        elif tipo_imovel == "Casa Condomínio" or tipo_imovel == "Casa Residencial":
            self.obtem_elemento('//*[@id="unit-type-HOME|UnitSubType_NONE,SINGLE_STOREY_HOUSE,VILLAGE_HOUSE,KITNET|RESIDENTIAL|HOME"]').click()
        elif tipo_imovel == "Sala Comercial":
            self.obtem_elemento('//*[@id="unit-type-OFFICE|UnitSubType_NONE,OFFICE,FLOOR|COMMERCIAL|OFFICE"]').click()
        elif tipo_imovel == "Casa Comercial":
            self.obtem_elemento('//*[@id="unit-type-HOME|UnitSubType_NONE|COMMERCIAL|COMMERCIAL_PROPERTY"]').click()
        elif tipo_imovel == "Terreno":
            self.obtem_elemento('//*[@id="unit-type-ALLOTMENT_LAND|UnitSubType_NONE,CONDOMINIUM,VILLAGE_HOUSE|RESIDENTIAL|RESIDENTIAL_ALLOTMENT_LAND"]').click()

    def properties_url(self, search_str, tipo_imovel):

        self.driver.get('https://www.vivareal.com.br/venda/')
        edit_filters = self.obtem_elemento('//*[@id="js-site-main"]/div[2]/div[1]/section/header/div/div/div[3]/div/button')
        edit_filters.click()

        # Aceitar os cookies da página 
        try:
            accept_cookies = self.obtem_elemento('//*[@id="cookie-notifier-cta"]')
            accept_cookies.click()
        except:
            pass

        # Colocar string de pesquisa 
        search_box = self.obtem_elemento('//*[@id="filter-location-search-input"]')
        search_box.send_keys(search_str)
        time.sleep(3)
        
        # Selecionar a primeira sugestão 
        search_box.send_keys(Keys.RETURN)

        # Filtrar tipo de imóvel (Apartamento, Casa, Sala, Loja, Loteamento)
        # 1) Clicar em "mostrar todos"
        mostrar_todos = self.obtem_elemento('//*[@id="js-site-main"]/div[2]/div[1]/nav/div/div/form/fieldset[1]/div[3]/div')
        mostrar_todos.click()

        # 2) Ajuste à janela de seleção do tipo de imóvel
        janela_selecao = self.obtem_elemento('//*[@id="js-site-main"]/div[2]/div[1]/nav/div/div/form/fieldset[1]/div[3]/div/div/div')
        self.driver.execute_script("arguments[0].scrollIntoView();", janela_selecao)

        # 3) Selecionar Tipo de Imóvel
        self.seleciona_tipo(tipo_imovel)

        # 4) Reajustar à "mostrar todos" novamente
        self.driver.execute_script("arguments[0].scrollIntoView();", mostrar_todos)
        mostrar_todos.click()
        
        # Terminar a edição 
        finish_edit = self.obtem_elemento('//*[@id="js-site-main"]/div[2]/div[1]/nav/div/div/form/div/a')
        finish_edit.click()

        # Retornar o URL com os imóveis 
        time.sleep(3)


        return self.driver.current_url
    

    def qtd_anuncios(self, dom):
        qtd = 1
        idx_li = 1
        final = False

        while not final:
            try:
                dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{idx_li}]')[0]
                qtd += 1
                idx_li += 1
            except:
                final = True
        
        return qtd


    def get_data(self, search_str, tipo_imovel):
        main_URL = self.properties_url(search_str, tipo_imovel)
        time.sleep(2)
        #self.driver.quit()
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
                URL = main_URL+f'?pagina={pagina}'

            print(URL)
            session = requests.Session()
            page = session.get(URL, headers={"User-Agent": str(self.ua.chrome)})

            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                dom = etree.HTML(str(soup))
                qtd_anuncios = self.qtd_anuncios(dom)

                for i in range(1, qtd_anuncios):
                    # Extrações 
                    estado, cidade, bairro, endereco = get_adress(dom, i)
                    area = get_area(dom, i)
                    quarto = get_quartos(dom, i)
                    banheiro = get_banheiros(dom, i)
                    vaga = get_vagas(dom, i)
                    preco = get_preco(dom, i)
                    link = 'https://www.vivareal.com.br' + get_link(dom, i)

                    # Adicionando extrações à lista
                    if len(preco) > 0:
                        estados.append(estado)
                        cidades.append(cidade)
                        bairros.append(bairro)
                        enderecos.append(endereco)
                        areas.append(area)
                        quartos.append(quarto)
                        banheiros.append(banheiro)
                        vagas.append(vaga)
                        precos.append(preco)
                        links.append(link)

                #next_page = get_next_page(dom, tipo_imovel)
                #print(next_page)
                if pagina > 7:
                    end = True
                    
            pagina += 1

        self.data_viva_real['Estado'] = estados
        self.data_viva_real['Cidade'] = cidades
        self.data_viva_real['Bairro'] = bairros
        self.data_viva_real['Endereço'] = enderecos
        self.data_viva_real['Área'] = areas
        self.data_viva_real['Quarto'] = quartos
        self.data_viva_real['Banheiro'] = banheiros
        self.data_viva_real['Vaga'] = vagas
        self.data_viva_real['Preço'] = precos
        self.data_viva_real['Link'] = links

        return self.data_viva_real
