import pandas as pd 
from bs4 import BeautifulSoup
from nylas import APIClient
from requests.api import patch
from credentials import CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN
from utils import *

nylas = APIClient(
    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN
)


def emails_laudos_bodys():
    bodys = []
    
    messages = nylas.messages.all(limit=50)
    for i in range(len(messages)):
        pasta = str(messages[i]['_folder']['display_name']).strip()
        if pasta == "Solicitações de Laudo":
            email = messages[i]['from'][0]['email']
            name = messages[i]['from'][0]['name']

            q = ""
            respostas = ['S', 'N']
            while q not in respostas:
                q = input(f"""Deseja extrair as informações enviadas por {name} ({email}) para fazer um Laudo? [S/N]: """)

                if q not in respostas:    
                    print('Resposta inválida. Digite (N) para NÃO ou (S) para SIM.')

            if q == 'S':
                bodys.append(messages[i]['body'])

    return bodys


def get_text(soup):
    """
    https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
    """

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def transform_string(string):
    a = string.split(" ")
    words = []

    for word in a:
        words.append(word[0]+word[1:].lower())
    
    return " ".join(words)


def parse_informations(bodys_list):
    lead = []
    nome = []
    tipologia = []
    endereco = []
    complemento = []
    numero = []
    bairro = []
    municipio = []
    uf = []
    cep = []
    observacoes = []

    if len(bodys_list) > 0:
        for body in bodys_list:
            soup = BeautifulSoup(body, features="html.parser")
            text = get_text(soup)
            # keep main information
            splited_text = text.split('\n')

            for i in range(len(splited_text)):
                if splited_text[i] == 'Lead ID:':
                    lead.append(splited_text[i+1])
                    nome.append(transform_string(splited_text[i+3]))
                    tipologia.append(transform_string(splited_text[i+5]))

                    endereco_completo = splited_text[i+7]
                    print(endereco_completo)
                    try:
                        endereco.append(transform_string(endereco_completo.split(',')[0]))
                        numero.append(endereco_completo.split(',')[1].split('-')[0])
                        complemento.append(transform_string(endereco_completo[i+7].split(',')[1].split('-')[1]))
                    except:
                        endereco.pop(-1)
                        endereco.append(transform_string(endereco_completo.split(' ')[0] +' '+ endereco_completo.split(' ')[1]))
                        numero.append(endereco_completo.split(' ')[2][:-1])
                        complemento.append("")

                    municipio.append(transform_string(splited_text[i+9]))
                    uf.append(splited_text[i+11])
                    cep.append(splited_text[i+13])

                    x = transform_string(get_bairro(splited_text[i+13]))
                    bairro.append(x) # cep


                    observacoes.append(get_obs(x, transform_string(splited_text[i+9])))
                    
                    #observacoes.append(splited_text[i+15])
    else:
        print('Não há novos email para serem extraidos')


    dados = {}
    dados['Nome Cliente'] = nome
    dados['Endereço'] = endereco
    dados['Numero'] = numero
    dados['Complemento'] = complemento
    dados['Bairro'] = bairro
    dados['CEP'] = cep
    dados['Município'] = municipio
    dados['UF'] = uf
    dados['Tipo'] = tipologia
    dados['Lead ID'] = lead
    dados['Observações'] = observacoes

    df = pd.DataFrame.from_dict(dados)
    path = str(r'R:\Empirica Cobrancas e Garantias\5 - Avaliacoes de Imoveis\Laudos Creditas') + str(r'\novos_laudos.xlsx')
    df.to_excel(path, sheet_name='Sheet1')


if __name__ == '__main__':
    bodys = emails_laudos_bodys()
    parse_informations(bodys)