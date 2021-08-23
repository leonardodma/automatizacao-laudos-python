from ast import ExtSlice
import win32com.client
import os
import time
from datetime import datetime, timedelta
import pandas as pd
from win32com.client.selecttlb import TypelibSpec
from utils import *
from tqdm import tqdm

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path

# Chrome Driver 
chromedriver_path = Path(str(Path(__file__).parent.resolve()) + '\software\chromedriver_win32\chromedriver.exe')
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


import pythoncom           # These 2 lines are here because COM library
pythoncom.CoInitialize()   # is not initialized in the new thread
from credentials import EMPIRICA_USER, EMPIRICA_EMAIL, SENHA_JIRA


def transform_string(string, keep=False):
    if not keep:
        a = string.strip().split(" ")
        words = []

        complementos = ['DOS', 'DA', 'DE', 'DAS']
        for word in a:
            if word not in complementos:
                words.append(word[0]+word[1:].lower())
            else:
                words.append(word.lower())
        
        return " ".join(words)
    else:
        return string.strip()


def get_bodys():
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI")
    solicitacoes = outlook.Folders['Avaliações'].Folders['Caixa de Entrada']
    messages = solicitacoes.Items
    messages.Sort("[ReceivedTime]", True)

    solicitacao1 = 'Creditas - Solicitação de Laudo'
    solicitacao2 = 'Creditas - Solicitação de Laudo Remoto'
    tipos_solicitacoes = [solicitacao1, solicitacao2]

    pedidos = 0
    bodys = []
    solicitacoes = []

    pedidos = 0
    print('Colhendo Mensagens...')
    fim = False
    for msg in messages:
        if not fim:
            data = msg.SentOn.strftime("%d/%m/%y")
            subject_splited = msg.Subject.split(':')
            
            not_solicitaoes = ['ENC', 'RES', 'Re']
            try:
                if subject_splited[0] not in not_solicitaoes:
                    if subject_splited[0].strip() in tipos_solicitacoes:
                        print(f'Deseja colher os dados do email com descrição "{msg.Subject}"", enviado {data}? [S/N]')
                        awsr = input('Digite sua resposta: ')
                        if awsr == 'S':
                            bodys.append(msg.body.strip())
                            pedidos += 1
                        else: 
                            fim = True 
            except:
                pass
        
        else:
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

        for i in  range(len(rua_numero)):
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


def download_documents(link, folder):
    prefs = {"download.default_directory" : folder}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
    driver.get(link)
    time.sleep(4)

    # Colocar email
    driver.find_element_by_xpath('//*[@id="user-email"]').send_keys(EMPIRICA_EMAIL)
    time.sleep(2)

    # Seleciona próximo
    driver.find_element_by_xpath('//*[@id="login-button"]').click()
    time.sleep(4)

    # Seleciona Entrar com login Único
    driver.find_element_by_xpath('//*[@id="login-button"]').click()
    time.sleep(2)

    # Seleciona Continuar 
    driver.find_element_by_xpath('//*[@id="login-submit"]').click()
    time.sleep(1)

    # Digita a senha 
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(SENHA_JIRA)
    time.sleep(1)

    # Seleciona Continuar 
    driver.find_element_by_xpath('//*[@id="login-submit"]').click()
    time.sleep(10)

    # Recolhe para a div documentos
    div_documentos = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div[2]/main/div/div[2]/div[1]/div[2]')
    driver.execute_script("arguments[0].scrollIntoView();", div_documentos)
    time.sleep(1)

    # Clica no primeiro documento 
    driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div[2]/main/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div/div/div[2]').click()
    time.sleep(2)

    # Clica no botão de download
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/button').click()
    time.sleep(3)

    # Fecha o primeiro documento 
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/button').click()
    time.sleep(2)

    # Clica no segundo documento 
    driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div/div[2]/main/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/div/div/div[2]').click()
    time.sleep(2)

    # Clica no botão de download
    driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/button').click()
    time.sleep(3)


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
    descricoes = []

    if len(bodys_list) > 0:
        print('COLHENDO DADOS DO EMAIL...')
        for j in tqdm(range(len(bodys_list))):
            body = bodys_list[j]
            splited_text = body.split('\n')

            for i in range(len(splited_text)):
                if splited_text[i].strip() == 'Lead ID:':
                    lead.append(transform_string(splited_text[i+1], keep=True))

                    nome_cliente = transform_string(splited_text[i+3])
                    nome.append(nome_cliente)
                    
                    # Cria pasta com nome do cliente:
                    client_path = create_client_path(nome_cliente)

                    # Continua colhendo as informações
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
                    descricoes.append(get_obs(b, transform_string(splited_text[i+9])))


                # Colhe o link do Jira
                if splited_text[i].strip() == 'Observações:':
                    try:
                        link = splited_text[i+1].strip().split('Jira:')[1].strip()
                    except:
                        link = splited_text[i+1]

                    # Faz o download dos documentos com o link do Jira
                    download_documents(link, client_path)

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
    dados['Descrições'] = descricoes
    dados['Endereço Completo'] = endereco_completo

    df = pd.DataFrame.from_dict(dados)
    path = str(r'C:\Users' f'\\{EMPIRICA_USER}' r'\Empírica Investimentos Gestão de Recursos Ltda\Dados - Documentos\Empirica Cobrancas e Garantias\5 - Avaliacoes de Imoveis\Laudos Creditas\novos_laudos.xlsx')
    df.to_excel(path, sheet_name='Sheet1')


if __name__ == '__main__':
    bodys = get_bodys()
    parse_informations(bodys)
    

#print(str(messages.GetLast().body).strip())