from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import re
import json
from statistics import mean

ua = UserAgent()

URL = 'https://www.zapimoveis.com.br/venda/apartamentos/sp+sao-paulo+zona-sul+sto-amaro/'
session = requests.Session()
page = session.get(URL, headers={"User-Agent": str(ua.chrome)})
soup = str(BeautifulSoup(page.content, 'html.parser'))


data = re.search(r'window.__INITIAL_STATE__=({.*})', soup).group(1)
a = "".join(data.split(";")[0:-3])
data = json.loads(a)['results']["listings"]
#print(json.dumps(data, indent=4))


for i in range(len(data)):
    cidade = data[i]["link"]["data"]["city"]
    print(cidade)

    bairro = data[i]["link"]["data"]["neighborhood"]
    print(bairro)

    endereco = data[i]["link"]["data"]["street"]+', '+data[i]["link"]["data"]["streetNumber"]
    print(endereco)

    area = mean(list(map(int, data[i]["listing"]["usableAreas"])))
    print(area)

    banheiros = data[i]["listing"]["bathrooms"][0]
    print(banheiros)

    quartos = data[i]["listing"]["bedrooms"][0]
    print(quartos)

    preco = data[i]["listing"]["pricingInfo"]["price"]
    print(preco)
    
    link = 'https://www.zapimoveis.com.br'+data[i]["listing"]["link"]
    print(link)
    