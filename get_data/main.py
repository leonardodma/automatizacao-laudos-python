# Author - Leonardo Duarte Malta de Abreu 
# Github - leonardodma

# Imports Bibliotecas Básicas
from re import search
from numpy.lib.function_base import append
import pandas as pd 
import numpy as np
import os, os.path
from pathlib import Path
import openpyxl
import pathlib


# Imports Selenium (Navegador Web) - Obter Links dos imóveis 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Importe de Módulos
from crawler_casa_mineira import *
from crawler_viva_real import *
from crawler_zap_imoveis import *


class Crawler_Full():
    def __init__(self):
        # Variável para guardar os dados coletados
        self.all_data = None


        # Chrome Driver
        chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver_win32\chromedriver.exe')
        options = Options()
        options.add_argument("--window-size=1920x1800")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)


        with open(str(pathlib.Path(__file__).parent.resolve())+str(r'\file.txt'), 'r') as f:
            informations = f.read().split('\n')
            self.file_path = informations[0]
            self.bairro = informations[1]
            self.municipio = informations[2]
            self.tipo = informations[3]
        
        # Planilha
        self.laudo = self.file_path
        print(f'LAUDO: {self.laudo}')


    def get_search_string(self):
        search_string = f'{self.bairro}, {self.municipio}'.strip()

        return search_string, self.tipo


    def merge_data(self, data_dict_list):
        frames = []

        for i in range(len(data_dict_list)):
            df = pd.DataFrame.from_dict(data_dict_list[i])
            frames.append(df)

        self.all_data = pd.concat(frames)


    def get_data(self):
        search_string, tipo_imovel = self.get_search_string()

        #crawler_casa_mineira = Crawler_CasaMineira(self.driver)
        crawler_viva_real = Crawler_VivaReal(self.driver)
        crawler_zap_imoveis = Crawler_ZapImoveis(self.driver)

        #casa_mineira = crawler_casa_mineira.get_data(search_string, tipo_imovel)
        viva_real = crawler_viva_real.get_data(search_string, tipo_imovel)
        zap_imoveis = crawler_zap_imoveis.get_data(search_string, tipo_imovel)

        self.merge_data([viva_real, zap_imoveis])


    def clean_dataframe(self):
        print('\n\n')
        self.all_data.replace('', np.nan, inplace=True)

        area_imovel = self.ws['U34'].value
        print(f'Área do imóvel analisado: {area_imovel}')

        print('LIMPANDO IMÓVEIS PELA ÁREA')
        self.all_data = self.all_data[(self.all_data['Área'] < area_imovel+20) & 
                                      (self.all_data['Área'] > area_imovel-20)]

        print('LIMPANDO ENDEREÇOS E PREÇOS VAZIOS')
        self.all_data[['Endereço', 'Preço']].replace('', np.nan, inplace=True)
        self.all_data.dropna(subset=['Endereço'], inplace=True)
        self.all_data.dropna(subset=['Preço'], inplace=True)

        print('LIMPANDO ITENS REPETIDOS')
        drop_idx = []
        cleaned_data = []

        bairro = list(self.all_data['Bairro'])
        endereco = list(self.all_data['Endereço'])
        area = list(self.all_data['Área'])
        preco = list(self.all_data['Preço'])

        for i in range(len(bairro)):
            row = [bairro[i], endereco[i], area[i], preco[i]]
            if row not in cleaned_data:
                cleaned_data.append(row)
            else:
                drop_idx.append(i)

        print(drop_idx)

        self.all_data.drop(self.all_data.index[drop_idx], inplace=True)


    def save_dataframe(self):
        file_path = self.laudo
        barra = str(r" \ ")[1]
        save_path = barra.join(file_path.split(barra)[0:-1])+barra+'dados_coletados.xlsx'
        print('\n')
        print(f'Dados coletados foram salvos em: {save_path}')
        
        self.all_data.reset_index(drop=True, inplace=True)
        self.all_data.to_excel(save_path, sheet_name='Sheet1')


if __name__ == '__main__':
    crawler = Crawler_Full()
    crawler.get_data()
    crawler.clean_dataframe()
    crawler.save_dataframe()
