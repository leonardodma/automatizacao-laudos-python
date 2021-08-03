import win32com.client
import os
from datetime import datetime, timedelta
import pandas as pd
from win32com.client.selecttlb import TypelibSpec
from utils import *
import tqdm


def transform_string(string, keep=False):
    if not keep:
        a = string.strip().split(" ")
        words = []

        for word in a:
            words.append(word[0]+word[1:].lower())
        
        return " ".join(words)
    else:
        return string.strip()



def get_bodys():
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI")
    solicitacoes = outlook.Folders['Avaliações'].Folders['Caixa de Entrada']
    messages = solicitacoes.Items

    solicitacao1 = 'Creditas - Solicitação de Laudo'
    solicitacao2 = 'Creditas - Solicitação de Laudo Remoto'

    pedidos = 0
    bodys = []
    solicitacoes = []

    pedidos = 0
    for msg in messages:
        subject_splited = msg.Subject.split(':')

        if subject_splited[1].strip() == solicitacao1 or subject_splited[1].strip() == solicitacao2:
            bodys.append(msg.body.strip())
            pedidos += 1

        if pedidos >= 5:
            break

    return bodys


def split_addresses(endereco_completo, UF):
    if UF != 'DF':
        endereco_completo = endereco_completo.split('-')
        rua_numero = endereco_completo[0].split(" ")
        complemento = endereco_completo[1]

        for i in range(len(rua_numero)):
            try:
                int(rua_numero[i])
                numero = rua_numero[i]
                rua_numero.pop(i)
            except:
                pass

        endereco = " ".join(rua_numero)

    else:
        endereco_completo = endereco_completo.split('-')
        rua_numero = endereco_completo[0].split(" ")
        complemento = endereco_completo[1]
        
        endereco = ""
        numero = ""
        inicio_complemento = False
        fim = False

        for i in range(len(rua_numero)):
            if not inicio_complemento:
                endereco += ' '+rua_numero[i]
            else:
                numero += ' '+rua_numero[i]

            if not fim:
                if rua_numero[i] == 'Lote':
                    endereco = " ".join(endereco.strip().split(' ')[:-1])
                    inicio_complemento = True
                    fim = True
    
    return endereco, numero.strip(), complemento.strip()


def parse_informations(bodys_list):
    lead = []
    nome = []
    tipologia = []
    endereco_completo = []
    endereco = []
    complemento = []
    numero = []
    bairro = []
    municipio = []
    uf = []
    cep = []
    observacoes = []

    if len(bodys_list) > 0:
        print('COLHENDO DADOS DO EMAIL')
        for j in range(len(bodys_list)):
            body = bodys_list[j]
            splited_text = body.split('\n')

            for i in range(len(splited_text)):
                if splited_text[i].strip() == 'Lead ID:':
                    lead.append(transform_string(splited_text[i+1], keep=True))
                    nome.append(transform_string(splited_text[i+3]))
                    tipologia.append(transform_string(splited_text[i+5]))
                    end_completo = transform_string(splited_text[i+7])
                    endereco_completo.append(end_completo)

                    u = transform_string(splited_text[i+11], keep=True)
                    uf.append(u)

                    end, num, comp = split_addresses(end_completo, u)
                    endereco.append(end)
                    numero.append(num)
                    complemento.append(comp)

                    municipio.append(transform_string(splited_text[i+9]))

                    c = transform_string(splited_text[i+13], keep=True)
                    cep.append(c)
                    b = get_bairro(c)
                    bairro.append(b)
                    observacoes.append(get_obs(b, transform_string(splited_text[i+9])))

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
    dados['Endereço Completo'] = endereco_completo

    df = pd.DataFrame.from_dict(dados)
    path = str(r'.\novos_laudos.xlsx')
    df.to_excel(path, sheet_name='Sheet1')


if __name__ == '__main__':
    bodys = get_bodys()
    parse_informations(bodys)

#print(str(messages.GetLast().body).strip())