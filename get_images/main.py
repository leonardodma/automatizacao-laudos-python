# Author - Leonardo Duarte Malta de Abreu 
# Github - leonardodma

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from lxml import etree
import pathlib
from pathlib import Path


ua = UserAgent()
barra = str(r' \ ')[1]
with open(str(pathlib.Path(__file__).parent.resolve())+str(r'\file.txt'), 'r') as f:
    dados = f.read().strip().split("\n")
    laudo_path = dados[0]
    amostra = dados[1]
    tentativas = int(dados[2])
    endereco = dados[3]
    bairro = dados[4]


def save_path():
    planilha = laudo_path.split('/')
    barra = str(r" \ ")[1]
    pyhon_file_path = str(Path(__file__).parent.resolve()).split(barra)
    user_path = barra.join(pyhon_file_path[:3])
    img_path = barra + barra.join(planilha[8:-1]) + barra + 'img'
    file_name = f'\\amostra{amostra}.png'

    if img_path == str(r'\\img'):
        save_path = barra.join(laudo_path.split(barra)[:-1]) + '\img' + file_name
        folder = barra.join(laudo_path.split(barra)[:-1]) + '\img'
    else:
        save_path = user_path + str(r'\Documents\Empírica Investimentos Gestão de Recursos Ltda\EMPIRICA-COBRANCAS-E-GARANTIAS - Documentos\Empirica Cobrancas e Garantia\5 - Avaliacoes de Imoveis') + img_path + file_name
        folder = user_path + str(r'\Documents\Empírica Investimentos Gestão de Recursos Ltda\EMPIRICA-COBRANCAS-E-GARANTIAS - Documentos\Empirica Cobrancas e Garantia\5 - Avaliacoes de Imoveis') + img_path

    return save_path, folder 


def get_address():
    search_string = f'{endereco} {bairro}'.strip()

    return search_string


def get_url(search_str):
    query = search_str.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"

    print(url)

    return url


def get_dom(url):
    session = requests.Session()
    page = session.get(url, headers={"User-Agent": str(ua.chrome)})
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))

    return dom


def download_image(src):
    path, folder = save_path()
    Path(folder).mkdir(parents=True, exist_ok=True)
    print('Imagem salva em:')
    print(path)
    f = open(path,'wb')
    f.write(requests.get(src).content)
    f.close()


def get_image(tentativas):
    url = get_url(get_address())
    dom = get_dom(url)
    xpath = ".//img[contains(@class, 'yWs4tf')]"
    src = dom.xpath(xpath)[tentativas].items()[2][1]
    download_image(src)


if __name__ == '__main__':
    get_image(tentativas)
