# Author - Leonardo Duarte Malta de Abreu 
# Github - leonardodma

# Imports Bibliotecas Básicas
from re import search
from numpy.lib.function_base import append, copy
import pandas as pd 
import numpy as np
import os, os.path
from pathlib import Path
import openpyxl
import pathlib
from scipy import stats


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
            self.laudo = informations[0]
            self.bairro = informations[1]
            self.municipio = informations[2]
            self.tipo = informations[3]

            try:
                self.area = int(informations[4])
            except:
                self.area = int(float(".".join(informations[4].split(","))))
            
            self.quartos = int(informations[5])
        
        # Planilha
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
        #self.all_data.to_excel(str(pathlib.Path(__file__).parent.resolve())+str(r'\all_data.xlsx'))



    def get_data(self):
        search_string, tipo_imovel = self.get_search_string()

        #crawler_casa_mineira = Crawler_CasaMineira(self.driver)
        crawler_viva_real = Crawler_VivaReal(self.driver)
        crawler_zap_imoveis = Crawler_ZapImoveis(self.driver)

        #casa_mineira = crawler_casa_mineira.get_data(search_string, tipo_imovel)
        viva_real = crawler_viva_real.get_data(search_string, tipo_imovel)
        zap_imoveis = crawler_zap_imoveis.get_data(search_string, tipo_imovel)

        self.merge_data([viva_real, zap_imoveis])


    def valor_unitario(self):
        precos = list(self.all_data['Preço'])
        areas = list(self.all_data['Área'])
        
        valor_unitario = []
        for i in range(len(precos)):
            try:
                num = int("".join(precos[i].strip()[2:].split('.')))
            except:
                num = 0.0
            value = float(f'{num/areas[i]:.2f}')
            valor_unitario.append(value)
        
        return valor_unitario
    

    def remove_outliers(self):
        z_scores = stats.zscore(self.all_data['Valor unitário (R$/m²)'])
        abs_z_scores = np.abs(z_scores)
        filtered_entries = abs_z_scores < 2.0
        self.all_data = self.all_data[filtered_entries]

    
    def clean_dataframe(self):
        print('\n\n')
        self.all_data.replace('', np.nan, inplace=True)

        area_imovel = self.area
        print(f'Área do imóvel analisado: {area_imovel}')

        print('LIMPANDO IMÓVEIS PELA ÁREA')
        self.all_data = self.all_data[self.all_data['Área'] < area_imovel + area_imovel*0.2]
        self.all_data = self.all_data[self.all_data['Área'] > area_imovel - area_imovel*0.2]

        print('LIMPANDO ITEMS PELO NÚMERO DE QUARTOS')
        self.all_data = self.all_data[self.all_data['Quarto'] == self.quartos]

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

        cleaned_df = pd.DataFrame.copy(self.all_data)
        cleaned_df.dropna(subset=['Endereço'], inplace=True)
        cleaned_df.dropna(subset=['Preço'], inplace=True)
        
        if len(cleaned_df.index) > 8:
            print('LIMPANDO ENDEREÇOS E PREÇOS VAZIOS')
            self.all_data = cleaned_df
        else:
            print('Tem menos de oito itens. Salvando itens sem endereço também!' )
        

        print('REMOVENDO OUTLIERS DO VALOR UNITÁRIO')
        self.all_data['Valor unitário (R$/m²)'] =  self.valor_unitario()
        self.remove_outliers()
        self.all_data = self.all_data.sort_values(by=['Valor unitário (R$/m²)'])


    def save_dataframe(self):
        planilha = self.laudo.split('/')
        barra = str(r" \ ")[1]
        pyhon_file_path = str(Path(__file__).parent.resolve()).split(barra)
        user_path = barra.join(pyhon_file_path[:3])
        planilha_path = barra + barra.join(planilha[8:-1])
        file_name = r'\dados_coletados.xlsx'

        if planilha_path == barra:
            save_path = barra.join(self.laudo.split(barra)[:-1]) + file_name
        else:
            save_path = user_path + str(r'\Documents\Empírica Investimentos Gestão de Recursos Ltda\EMPIRICA-COBRANCAS-E-GARANTIAS - Documentos\Empirica Cobrancas e Garantia\5 - Avaliacoes de Imoveis') + planilha_path + file_name

        print('\n')
        print(f'Dados coletados foram salvos em: {save_path}')
        self.all_data.reset_index(drop=True, inplace=True)
        self.all_data.to_excel(save_path, sheet_name='Sheet1')


if __name__ == '__main__':
    crawler = Crawler_Full()
    crawler.get_data()
    crawler.clean_dataframe()
    crawler.save_dataframe()
