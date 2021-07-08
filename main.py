# Author - Leonardo Duarte Malta de Abreu 
# Github - leonardodma

# Imports Bibliotecas Básicas
from re import search
from numpy.lib.function_base import append
import pandas as pd 
import numpy as np
import time
import os, os.path
from pathlib import Path
import openpyxl
import easygui
from tqdm import tqdm

# Imports Selenium (Navegador Web) - Obter Links dos imóveis 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Importe de Módulos
from crawler_viva_real import *


class Crawler_Full():
    def __init__(self):
        # Variável para guardar os dados coletados
        self.all_data = {}

        # Planilha selecionada 
        print('SELECIONE A PLANILHA COM O LAUDO QUE VOCÊ ESTÁ COLHENDO OS DADOS')
        self.laudo = str(self.get_file_path())
        print(f'VOCÊ SELECIONOU O LAUDO: {self.laudo}')
        
        # Iniciando Softwares Necessários
        # 1) Chrome Driver
        chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver_win32\chromedriver.exe')
        options = Options()
        options.add_argument("--window-size=1920x1800")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)

    
    def get_file_path(self):
        #path = str(r'R:\Empírica Cobranças e Garantias\5 - Avaliações de Imóveis\Projeto estágio de férias\vba.txt')
        #print(f'O arquivo contendo o path do laudo é: {path}')

        #file = open(path, encoding="ascii").read()

        #return str(r'R:\Empírica Cobranças e Garantias\5 - Avaliações de Imóveis\Laudos Creditas\7.21\TESTE - ESTAGIO DE FÉRIAS - AUTOMATIZAÇÃO LAUDOS\07.21 - Maria José Pereira Dias.xlsm')

        return easygui.fileopenbox()


    def get_search_string(self):
        # Give the location of the file
        path = self.laudo
        wb_obj = openpyxl.load_workbook(path, data_only=True)
        self.ws = wb_obj['Modelo de Laudo']

        bairro = self.ws['E23'].value.strip()
        municipio = self.ws['E24'].value.strip()
        tipo = self.ws['E27'].value.strip()

        search_string = f'{bairro} - {municipio}'

        return search_string, tipo


    def get_data(self):
        search_string, tipo_imovel = self.get_search_string()
        crawler_viva_real = Crawler_VivaReal(self.driver)
        self.all_data = crawler_viva_real.get_data(search_string, tipo_imovel)


    def remove_by_idx(self, idxs):
        self.all_data['Estado'] = [i for n, i in enumerate(self.all_data['Estado']) if n not in idxs]
        self.all_data['Cidade'] = [i for n, i in enumerate(self.all_data['Cidade']) if n not in idxs]
        self.all_data['Bairro'] = [i for n, i in enumerate(self.all_data['Bairro']) if n not in idxs]
        self.all_data['Endereço'] = [i for n, i in enumerate(self.all_data['Endereço']) if n not in idxs]
        self.all_data['Área'] = [i for n, i in enumerate(self.all_data['Área']) if n not in idxs]
        self.all_data['Quartos'] = [i for n, i in enumerate(self.all_data['Quartos']) if n not in idxs]
        self.all_data['Banheiros'] = [i for n, i in enumerate(self.all_data['Banheiros']) if n not in idxs]
        self.all_data['Preço'] = [i for n, i in enumerate(self.all_data['Preço']) if n not in idxs]
        self.all_data['Link'] = [i for n, i in enumerate(self.all_data['Link']) if n not in idxs]


    def filter_by_area(self):
        area_imovel = self.ws['U34'].value
        print(f'Área do imóvel analisado: {area_imovel}')

        areas = self.all_data['Área']
        array_areas = []
        for area in areas:
            try:
                array_areas.append(int(area))
            except:
                x = int(area.split('-')[0].strip())
                y = int(area.split('-')[0].strip())
                array_areas.append((x+y)/2)

        idx_remove = []

        print('LIMPANDO IMÓVEIS PELA ÁREA')
        for i in tqdm(range(len(array_areas))):
            if array_areas[i] < area_imovel-20 or array_areas[i] > area_imovel+20:
                idx_remove.append(i)
        
        return idx_remove


    def clean_dataframe(self):
        # Filtra Área
        self.remove_by_idx(self.filter_by_area())
    

    def save_dataframe(self):
        file_path = self.laudo
        barra = str(r" \ ")[1]
        save_path = barra.join(file_path.split(barra)[0:-1])+barra+'dados_coletados.xlsx'
        print('\n')
        print(f'Dados coletados foram salvos em: {save_path}')
        
        pd.DataFrame.from_dict(self.all_data).to_excel(save_path, sheet_name='Sheet1')


if __name__ == '__main__':
    crawler = Crawler_Full()
    crawler.get_data()
    crawler.clean_dataframe()
    crawler.save_dataframe()
