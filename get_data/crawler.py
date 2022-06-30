import requests
import json
import pandas as pd
from geopy import GoogleV3
import geog
import shapely.geometry
import numpy as np
from credentials import MAPS_API_TOKEN
from bs4 import BeautifulSoup
import requests
from lxml import etree
from fake_useragent import UserAgent
from pathlib import Path
from unidecode import unidecode

# Imports Bibliotecas Básicas
import re
import json
from googlesearch import search

ua = UserAgent()
geolocator = GoogleV3(api_key=MAPS_API_TOKEN)


class Crawler():
    def __init__(self, latitude, longitude, bairro, municipio, uf, area, tipo):
        self.latitude = latitude
        self.longitude = longitude
        self.bairro = bairro
        self.municipio = municipio
        self.uf = uf
        self.area = area
        self.tipo = tipo

        self.session = requests.Session()

    def get_address_from_lat_long(self, latitude, longitude):
        location = geolocator.reverse(f"{latitude}, {longitude}")
        return location.address

    def get_neighbors(self):
        p = shapely.geometry.Point([self.latitude, self.longitude])

        n_points = 20
        d = 1 * 1000  # meters
        angles = np.linspace(0, 360, n_points)
        polygon = geog.propagate(p, angles, d)
        locations_array = shapely.geometry.mapping(
            shapely.geometry.Polygon(polygon))["coordinates"][0]

        neighbors = []
        for location in locations_array:
            latitude = location[0]
            longitude = location[1]

            address = self.get_address_from_lat_long(latitude, longitude)
            print(address)
            try:
                neighborhood = address.split(",")[1].split("-")[1]
                x = " ".join(neighborhood.split())
                if not x.isnumeric():
                    if x not in neighbors:
                        neighbors.append(x)
            except:
                pass

        return neighbors

    def get_zap_imoveis_url(self, bairro):
        query = f"{self.tipo} a venda em {bairro}, {self.municipio}, {self.uf}, Zap Imóveis"
        print("\nPesquisando no Zap Imóveis: \n" + query)

        google_results = search(query, tld="co.in", num=10, stop=10)

        for link in google_results:
            URL = link
            break

        for link in google_results:
            link_splited = link.split('/')
            if link_splited[3] == "venda":
                if self.tipo == "Casa Residencial":
                    if link_splited[4] == "casas":
                        URL = link
                        break
                if self.tipo == "Terreno":
                    if link_splited[4] == "terrenos-lotes-condominios":
                        URL = link
                        break
              
        URL = "/".join(URL.split('/')[0:6])

        return URL
    
    def test_url_viva(self, test_url):
        page = self.session.get(test_url, headers={
                            "User-Agent": str(ua.chrome)})
        soup = str(BeautifulSoup(
            page.content, 'html.parser'))
        dom = etree.HTML(str(soup))

        try:
            dom.xpath('//*[@id="js-site-main"]/div/h3')[0].text
            return False
        except:
            return True

    def get_viva_real_url(self, bairro):
        query = f"{self.tipo} a venda em {bairro}, {self.municipio}, {self.uf}, Viva Real"
        print("\nPesquisando no Viva Real: \n" + query)

        google_results = search(query, tld="co.in", num=10, stop=10)

        for link in google_results:
            URL = link
            link_splited = link.split('/')
            if link_splited[3] == "venda":
                break

        try:
            for link in google_results:
                link_splited = link.split('/')

                if link_splited[3] == "venda" and link_splited[6] == "bairros":
                    link = "/".join(link_splited[0:7])
                    bairro_url = "-".join(unidecode(bairro.lower()).split(" "))
                    if self.tipo == "Casa Residencial" or self.tipo == "Casa":
                        test_url = f"{link}/{bairro_url}/casa_residencial/"
                        if self.test_url_viva(test_url):
                            URL = test_url
                            break
                    if self.tipo == "Terreno":
                        test_url = f"{link}/{bairro_url}/lote-terreno_comercial/"
                        if self.test_url_viva(test_url):
                            URL = test_url
                            break             
        except:
            pass

        return URL

    def get_df_imoveis_url(self, bairro):
        query = f"{self.tipo} {bairro}, DF imóveis"
        google_results = search(query, tld="co.in", num=10, stop=10)

        for result in google_results:
            return result

    def parse_zap_imoveis_data(self, soup):
        data_colected = []
        data = re.search(r'window.__INITIAL_STATE__=({.*})', soup).group(1)
        data = json.loads("".join(data.split(";")[0:-3]))['results']["listings"]

        for i in range(len(data)):
            imovel = {}
            try:
                rua = data[i]["listing"]["address"]["street"]
                numero = int(data[i]["listing"]["address"]["streetNumber"])
                bairro = data[i]["listing"]["address"]["neighborhood"]
                if numero > 0:
                    area = int(data[i]["listing"]["usableAreas"][0])
                    quartos = int(data[i]["listing"]["bedrooms"][0])
                    banheiros = int(data[i]["listing"]["bathrooms"][0])
                    vaga = int(data[i]["listing"]["parkingSpaces"][0])
                    link = 'https://www.zapimoveis.com.br' + \
                        data[i]["listing"]["link"]

                    string_real = data[i]["listing"]["pricingInfo"]["price"]
                    valor = int("".join(string_real.split(" ")[1].split(".")))

                    if len(string_real) > 0:
                        imovel["endereco"] = f'{rua}, {numero}'
                        imovel["bairro"] = bairro
                        imovel["area"] = area
                        imovel["quartos"] = quartos
                        imovel["banheiros"] = banheiros
                        imovel["vaga"] = vaga
                        imovel["valor"] = valor
                        imovel["link"] = link
                        data_colected.append(imovel)
            except:
                pass

        return data_colected

    def parse_viva_real_data(self, dom):
        qtd = 1
        final = False
        while not final:
            try:
                dom.xpath(
                    f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{qtd}]')[0]
                qtd += 1
            except:
                final = True

        data_colected = []
        for i in range(1, qtd):
            imovel = {}
            try:
                full_address = dom.xpath(
                    f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{i}]/div/article/a/div/h2/span[2]/span[1]')[0].text.strip()
                address = full_address.split('-')[0].strip()
                bairro = full_address.split('-')[1].split(',')[0].strip()

                if int(address.split(',')[1].replace(" ", "")) != 0:
                    area = int(dom.xpath(
                        f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{i}]/div/article/a/div/ul/li[1]/span[1]')[0].text.strip())

                    quartos = int(dom.xpath(
                        f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{i}]/div/article/a/div/ul[1]/li[2]/span[1]')[0].text.strip())

                    banheiros = int(dom.xpath(
                        f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{i}]/div/article/a/div/ul/li[3]/span[1]')[0].text.strip())

                    vaga = int(dom.xpath(
                        f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{i}]/div/article/a/div/ul[1]/li[4]/span[1]')[0].text.strip())

                    valor = dom.xpath(
                        f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{i}]/div/article/a/div/section/div/p')[0].text.strip()

                    valor = int("".join(valor.split(' ')[1].split('.')))

                    link = dom.xpath(
                        f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{i}]/div/article/a/@href')[0]

                    link = 'https://www.vivareal.com.br'+link
                    imovel["endereco"] = address
                    imovel["bairro"] = bairro
                    imovel["area"] = area
                    imovel["quartos"] = quartos
                    imovel["banheiros"] = banheiros
                    imovel["vaga"] = vaga
                    imovel["valor"] = valor
                    imovel["link"] = link
                    data_colected.append(imovel)

            except:
                pass

        return data_colected

    def parse_df_imoveis_data(self, dom, bairro):
        qtd = 1
        final = False
        while not final:
            try:
                dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{qtd}]')[0]
                qtd += 1
            except:
                final = True

        data_colected = []
        for i in range(1, qtd):
            imovel = {}

            try:
                full_address = dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{i}]/div/div[2]/div[2]/h3[1]/a/text()')[0].strip()

                area = dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{i}]/div/div[2]/div[2]/ul[2]/li[1]/text()')[0].strip()

                area = int(area.split(' ')[2])

                quartos = dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{i}]/div/div[2]/div[2]/ul[2]/li[2]')[0].text.strip()

                try:
                    quartos = int(quartos.split(' ')[0])
                except:
                    quartos = 0

                banheiros = dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{i}]/div/div[2]/div[2]/ul[2]/li[3]')[0].text.strip()

                try:
                    banheiros = int(banheiros.split(' ')[0])
                except:
                    banheiros = 0

                vaga = dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{i}]/div/div[2]/div[2]/ul[2]/li[3]')[0].text.strip()

                try:
                    vaga = int(vaga.split(' ')[0])
                except:
                    vaga = 0

                valor = dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{i}]/div/div[2]/div[2]/h4[1]/span[2]')[0].text.strip()

                valor = int("".join(valor.split('.')))

                link = dom.xpath(
                    f'/html/body/div[1]/section[3]/div[2]/ul/li[{i}]/div/div[2]/div[2]/h3[1]/a/@href')[0]

                link = 'https://www.dfimoveis.com.br'+link

                imovel["endereco"] = full_address
                imovel["bairro"] = bairro
                imovel["area"] = area
                imovel["quartos"] = quartos
                imovel["banheiros"] = banheiros
                imovel["vaga"] = vaga
                imovel["valor"] = valor
                imovel["link"] = link
                data_colected.append(imovel)

            except:
                pass

        return data_colected

    def get_samples(self):
        df_imoveis_regions = ["DF"]
        if self.uf not in df_imoveis_regions:
            print("OBTENDO AMOSTRAS NO VIVA REAL E ZAP IMÓVEIS")
            url_zap_imoveis = self.get_zap_imoveis_url(self.bairro)
            url_viva_real = self.get_viva_real_url(self.bairro)

            # Decidindo se vai ser uma pesquisa só no bairro ou também com os vizinhos
            page = self.session.get(url_viva_real, headers={
                                    "User-Agent": str(ua.chrome)})
            soup = BeautifulSoup(page.content, 'html.parser')
            dom = etree.HTML(str(soup))

            # Determina a quantidade de anuncios
            anuncios = dom.xpath(
                f'//*[@id="js-site-main"]/div[2]/div[1]/section/header/div/div/div[1]/div/h1/strong')[0].text.strip()
            qtd_anuncios = int("".join(anuncios.split(".")))

            # Começa a buscar as amostras
            data_colected = []
            if qtd_anuncios >= 300:
                qtd_paginas = round(qtd_anuncios/36)
                if qtd_paginas >= 15:
                    qtd_paginas = 15

                for i in range(qtd_paginas):
                    if i != 0:
                        search_url_zap = url_zap_imoveis+f"?pagina={i+1}"
                        search_url_viva = url_viva_real+f"?pagina={i+1}"
                    else:
                        search_url_zap = url_zap_imoveis
                        search_url_viva = url_viva_real

                    print(search_url_zap)
                    print(search_url_viva)

                    # Page of zap
                    page_zap = self.session.get(search_url_zap, headers={
                                                "User-Agent": str(ua.chrome)})
                    soup_zap = str(BeautifulSoup(
                        page_zap.content, 'html.parser'))

                    # Page of vivareal
                    page_viva = self.session.get(search_url_viva, headers={
                        "User-Agent": str(ua.chrome)})
                    soup_viva = str(BeautifulSoup(
                        page_viva.content, 'html.parser'))
                    dom = etree.HTML(str(soup_viva))

                    # Colect data
                    data_colected += self.parse_zap_imoveis_data(soup_zap)
                    data_colected += self.parse_viva_real_data(dom)

            else:
                neighbors = self.get_neighbors()
                print("\n\nPESQUISANDO NOS BAIRROS:")
                print(neighbors)

                if self.bairro not in neighbors:
                    neighbors.insert(0, self.bairro)

                for neighbor in neighbors:
                    url_zap_imoveis = self.get_zap_imoveis_url(neighbor)
                    url_viva_real = self.get_viva_real_url(neighbor)

                    for i in range(3):
                        if i != 0:
                            search_url_zap = url_zap_imoveis+f"?pagina={i+1}"
                            search_url_viva = url_viva_real+f"?pagina={i+1}"
                        else:
                            search_url_zap = url_zap_imoveis
                            search_url_viva = url_viva_real

                        print(search_url_zap)
                        print(search_url_viva)

                        # Page of zap
                        page_zap = self.session.get(search_url_zap, headers={
                                                    "User-Agent": str(ua.chrome)})
                        soup_zap = str(BeautifulSoup(
                            page_zap.content, 'html.parser'))

                        # Page of vivareal
                        page_viva = self.session.get(search_url_viva, headers={
                            "User-Agent": str(ua.chrome)})
                        soup_viva = str(BeautifulSoup(
                            page_viva.content, 'html.parser'))
                        dom = etree.HTML(str(soup_viva))

                        # Colect data
                        data_colected += self.parse_zap_imoveis_data(soup_zap)
                        data_colected += self.parse_viva_real_data(dom)
        else:
            print("OBTENDO AMOSTRAS NO DF IMÓVEIS")
            url_df_imoveis = self.get_df_imoveis_url(self.bairro)

            data_colected = []
            for i in range(15):
                if i != 0:
                    search_url_df_imoveis = url_df_imoveis+f"?pagina={i+1}"
                else:
                    search_url_df_imoveis = url_df_imoveis

                print(search_url_df_imoveis)

                page = self.session.get(search_url_df_imoveis, headers={
                    "User-Agent": str(ua.chrome)})
                soup = BeautifulSoup(page.content, 'html.parser')
                dom = etree.HTML(str(soup))
                data_colected += self.parse_df_imoveis_data(dom, self.bairro)

        return data_colected

    def export_data(self, report_path):
        df = pd.json_normalize(self.get_samples())

        # Remove linhas com links repetidos
        df = df.drop_duplicates(subset=['link'])
        print("Removendo duplicados")

        print(df)

        # Filtra um range de 15 m2 de diferença para a área do imóvel analisado
        df = df[df['area'] < self.area + 20]
        df = df[df['area'] > self.area - 20]
        print("Filtrando as áreas")
        

        # Deixa o mesmo endereço somente 3 vezes
        df = df.groupby(["endereco"]).head(3)
        print("Tirando endereços repetidos se houver mais de 3 ocorrências")

        ############### Organizando as amostras ###############
        # Organiza as amostras pela proximidade da média de preços
        mean_prices = df["valor"].mean()
        df = df.iloc[(df['valor'] - mean_prices).abs().argsort()]
        print("Organizando Amostras\n\n")

        # Reset Index
        df = df.reset_index(drop=True)
        print("Amostras encontradas:")
        print(df)

        ############### Exporta as amostras###############
        planilha = report_path.split('/')
        barra = str(r" \ ")[1]
        pyhon_file_path = str(Path(__file__).parent.resolve()).split(barra)
        user_path = barra.join(pyhon_file_path[:3])
        planilha_path = barra + barra.join(planilha[7:-1])
        file_name = r'\dados_coletados.xlsx'

        if planilha_path == barra:
            save_path = barra.join(self.laudo.split(barra)[:-1]) + file_name
        else:
            save_path = user_path + \
                str(r'\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis') + \
                planilha_path + file_name

        df.to_excel(save_path, sheet_name='Sheet1')
        print(f'Dados coletados foram salvos em: {save_path}')
