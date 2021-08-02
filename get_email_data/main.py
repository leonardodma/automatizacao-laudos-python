import win32com.client
import os
from datetime import datetime, timedelta
import pandas as pd
from win32com.client.selecttlb import TypelibSpec
from utils import *


def transform_string(string, keep=False, remoto=True):
    if remoto:
        if not keep:
            a = string.split(" ")
            words = []

            for word in a:
                words.append(word[0]+word[1:].lower())
            
            return " ".join(words)[:-1]
        else:
            return string[:-1]
    else:
        if not keep:
            a = string.split(" ")
            words = []

            for word in a:
                words.append(word[0]+word[1:].lower())
            
            return " ".join(words)[2:-1]
        else:
            return string[2:-1]


def get_bodys():
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI")
    solicitacoes = outlook.Folders['Avaliações'].Folders['Caixa de Entrada']
    messages = solicitacoes.Items

    solicitacao1 = 'Creditas - Solicitação de Laudo'
    solicitacao2 = 'Creditas - Solicitação de Laudo Remoto'

    pedidos = 0
    bodys = []
    tipos = []
    solicitacoes = []

    for msg in messages:
        subject_splited = msg.Subject.split(':')

        if len(subject_splited) > 1:
            if subject_splited[1].strip() == solicitacao1:
                bodys.append(msg.body.strip())
                tipos.append(solicitacao1)
                pedidos += 1
            if subject_splited[1].strip() == solicitacao2:
                bodys.append(msg.body.strip())
                tipos.append(solicitacao2)
                pedidos += 1
        
        if pedidos >= 5:
            break

    return bodys, tipos


def parse_informations(bodys_list, tipos):
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
        for j in  range(len(bodys_list)):
            body = bodys_list[j]
            tipo = tipos[j]
            print(tipo)
            splited_text = body.split('\n')

            #print(splited_text)
            #print('\n\n')

            if tipo == 'Creditas - Solicitação de Laudo':
                for i in range(len(splited_text)):
                    if splited_text[i][:-1] == 'Lead ID:':

                        lead.append(transform_string(splited_text[i+1], keep=True))
                        nome.append(transform_string(splited_text[i+3]))
                        tipologia.append(transform_string(splited_text[i+5]))

                        endereco_completo = transform_string(splited_text[i+7])

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
                        uf.append(transform_string(splited_text[i+11], keep=True))
                        cep.append(splited_text[i+13])

                        x = get_bairro(splited_text[i+13])
                        bairro.append(x) # cep
                        observacoes.append(get_obs(x, transform_string(splited_text[i+9])))
            
            else:
                splited_text[i][2:-1]

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
    path = str(r'.\novos_laudos.xlsx')
    df.to_excel(path, sheet_name='Sheet1')


if __name__ == '__main__':
    bodys, tipos = get_bodys()
    parse_informations(bodys, tipos)

#print(str(messages.GetLast().body).strip())