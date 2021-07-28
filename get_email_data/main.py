import win32com.client
import os
from datetime import datetime, timedelta
import pandas as pd
from utils import *


def transform_string(string, keep=False):
    if not keep:
        a = string.split(" ")
        words = []

        for word in a:
            words.append(word[0]+word[1:].lower())
        
        return " ".join(words)[:-1]
    else:
        return string[:-1]


def get_bodys():
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI")
    root_folder = outlook.Folders.Item(1)
    solicitacoes = root_folder.Folders['Solicitações de Laudo']
    messages = solicitacoes.Items

    bodys = []

    for msg in list(messages):
        bodys.append(str(msg.body).strip())

    return bodys


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

            splited_text = body.split('\n')

            for i in range(len(splited_text)):
                #print(splited_text[i][:-1])
                if splited_text[i][:-1] == 'Lead ID:':

                    lead.append(transform_string(splited_text[i+1], keep=True))
                    nome.append(transform_string(splited_text[i+3]))
                    tipologia.append(transform_string(splited_text[i+5]))

                    endereco_completo = transform_string(splited_text[i+7])
                    print(endereco_completo)

                    try:
                        endereco.append(endereco_completo.split(',')[0])
                        numero.append(endereco_completo.split(',')[1].split('-')[0])
                        complemento.append(endereco_completo.split(',')[1].split('-')[1])
                    except:
                        endereco.pop(-1)
                        endereco.append(endereco_completo.split(' ')[0] +' '+ endereco_completo.split(' ')[1])
                        numero.append(endereco_completo.split(' ')[2][:-1])
                        complemento.append("")

                    municipio.append(transform_string(splited_text[i+9]))
                    uf.append(splited_text[i+11])
                    cep.append(splited_text[i+13])

                    x = get_bairro(splited_text[i+13])
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

    print(dados)

    df = pd.DataFrame.from_dict(dados)
    print(df)
    path = str(r'.\novos_laudos.xlsx')
    df.to_excel(path, sheet_name='Sheet1')


if __name__ == '__main__':
    bodys = get_bodys()
    parse_informations(bodys)

#print(str(messages.GetLast().body).strip())