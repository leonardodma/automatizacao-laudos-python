from os import name
import os
import requests
import json

from win32com import client
from credentials import MAPS_TOKEN, EMPIRICA_USER
import wikipedia
from datetime import date
wikipedia.set_lang("pt")


def get_bairro_correios(cep):
    url = f'https://viacep.com.br/ws/{cep}/json/'
    result = requests.get(url).json()
    return result['bairro']


def get_bairro(cep):
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?parameters'

    params = {
        'key': MAPS_TOKEN,
        'input': f'CEP: {cep}, Brasil',
        'inputtype': 'textquery',
        'fields': 'place_id,formatted_address',
    }

    try:
        return get_bairro_correios(cep)
    except:
        try:
            result = requests.post(url, params=params).json()['candidates'][0]
            infos = result['formatted_address'].split(',')

            if len(infos) == 4:
                return infos[0]
            elif len(infos) == 5:
                return infos[1]
            else:
                return ""
        except:
            return ""


def get_obs(bairro, cidade):
    if len(bairro) > 0:
        try:
            obs = wikipedia.summary(f"{bairro} - Bairro de {cidade}").split("\n")

            if len(obs) > 1:
                if len(obs[0].split('.')) > 2:
                    return obs[0]
                else:
                    return obs[0] + ' ' + obs[1]
            else:
                return obs[0]
        except:
            return 'Não foi encontrado nada sobre esse bairro no Wikpedia'
    else:
        return ""


def get_path():
    today = str(date.today()).split('-')
    year = today[0][2:]
    month = str(int(today[1]))
    time_folder = '.'.join([month, year])
    time_folder = f'\\{time_folder}'
    path = r'C:\Users' + f'\\{EMPIRICA_USER}' + r'\Documents\Empírica Investimentos Gestão de Recursos Ltda\EMPIRICA-COBRANCAS-E-GARANTIAS - Documentos\Empirica Cobrancas e Garantia\5 - Avaliacoes de Imoveis\Laudos Creditas' + time_folder    

    return path


def listdirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def create_client_path(cliente):
    path = get_path()
    dirs = listdirs(path)
    current_number = 0
    for i in range(len(dirs)):
        dir_name = str(dirs[i])
        try:
            n = int(dir_name.split('-')[0].strip())
            if n > current_number:
                current_number = n
        except:
            pass
    
    client_path = path + f'\{str(current_number + 1)} - {cliente}'
    # Cria pasta se ela não
    os.makedirs(client_path, exist_ok=True)

    return client_path