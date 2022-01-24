from credentials import EMPIRICA_USER, EMPIRICA_EMAIL, SENHA_JIRA
import pythoncom           # These 2 lines are here because COM library
from ast import ExtSlice
import win32com.client
import os
import time
from datetime import datetime, timedelta
import pandas as pd
from win32com.client.selecttlb import TypelibSpec
from utils import *
from tqdm import tqdm
from tkinter import *
from tkinter import ttk

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

# Chrome Driver
chromedriver_path = Path(str(Path(__file__).parent.resolve(
)) + '\software\chromedriver_win32\chromedriver.exe')
options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

pythoncom.CoInitialize()   # is not initialized in the new thread


class Selector():
    def __init__(self, options_list, title):
        # Creating root of object
        self.root = Tk()
        self.root.title(title)
        self.root.geometry("+50+300")

        # Creating frame to displace the options
        frame = ttk.Frame(self.root, padding=(3, 3, 12, 12))
        frame.grid(column=0, row=0, sticky=(N, S, E, W))

        # Creating option list from python list recieved
        var = StringVar(value=options_list)
        self.lstbox = Listbox(frame, listvariable=var,
                              selectmode=MULTIPLE, width=200, height=15)
        self.lstbox.grid(column=0, row=0, columnspan=2)

        btn = ttk.Button(frame, text="OK", command=self.select)
        btn.grid(column=1, row=1)
        self.root.mainloop()

    def select(self):
        reslist = list()
        seleccion = self.lstbox.curselection()
        self.selected_items = []
        for i in seleccion:
            entrada = self.lstbox.get(i)
            reslist.append(entrada)
        for val in reslist:
            self.selected_items.append(val)

        self.root.destroy()

    def get_select(self):
        return self.selected_items


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


def get_last_emails(solicitacoes, qtd=5):
    solicitacao1 = 'Creditas - Solicitação de Laudo'
    solicitacao2 = 'Creditas - Solicitação de Laudo Remoto'
    tipos_solicitacoes = [solicitacao1, solicitacao2]

    not_solicitaoes = ['ENC', 'RES', 'Re']
    pedidos = 0
    leads = []
    bodys = []
    
    messages = solicitacoes.Items
    messages.Sort("[ReceivedTime]", True)

    fim = False
    for msg in messages:
        if not fim:
            try:
                data = msg.SentOn.strftime("%d/%m/%y")
                subject_splited = msg.Subject.split(':')

                try:
                    if subject_splited[0] not in not_solicitaoes:
                        if subject_splited[0].strip() in tipos_solicitacoes:

                            email = f'{msg.Subject}, enviado {data}.'

                            if pedidos <= qtd:
                                leads.append(email)
                                bodys.append(msg.body.strip())
                                pedidos += 1
                            else:
                                fim = True
                except:
                    pass
            except:
                pass
        else:
            break
    
    return leads, bodys


def get_bodys():
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI")
    solicitacoes_caixa_solicitacoes = outlook.Folders['Avaliações'].Folders['Solicitações']
    solicitacoes_caixa_entrada = outlook.GetDefaultFolder(6)
    
    leads_caixa_solicitacoes, bodys_caixa_solicitacoes = get_last_emails(solicitacoes_caixa_solicitacoes, qtd=10)
    leads_caixa_entrada, bodys_caixa_entrada = get_last_emails(solicitacoes_caixa_entrada)
    leads = leads_caixa_solicitacoes + leads_caixa_entrada
    bodys = bodys_caixa_solicitacoes + bodys_caixa_entrada

    #leads = leads_caixa_solicitacoes
    #bodys = bodys_caixa_solicitacoes
    
    bodys_selected = []
    list_box = Selector(leads, "Caixa de Solicitações")
    chosen_options = list_box.get_select()

    for i in range(len(leads)):
        if leads[i] in chosen_options:
            bodys_selected.append(bodys[i])

    return bodys_selected


def split_addresses(endereco_completo, UF):
    if UF != 'DF':
        endereco_completo = endereco_completo.split(',')
        endereco = endereco_completo[0]
        numero = ""
        complemento = ""

        if len(endereco_completo) == 2:
            numero_complemento = endereco_completo[1].split('-')

            if len(numero_complemento) == 1:
                if numero_complemento[0].count('(') > 0:
                    numero = numero_complemento[0].split('(')[0]
                    complemento = numero_complemento[0].split(
                        '(')[1].split(')')[0]
                else:
                    numero = numero_complemento[0]
                    complemento = ""
            else:
                numero = numero_complemento[0].strip()
                complemento = numero_complemento[1]

        else:
            numero = endereco_completo[1]
            complemento = endereco_completo[2]

    else:
        endereco = ""
        numero = ""
        complemento = ""

    return endereco, numero.strip(), complemento.strip()


def obtem_elemento(driver, xpath):
    return wait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))


def download_documents(link, folder):
    prefs = {"download.default_directory": folder}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        executable_path=chromedriver_path, options=options)

    driver.get(link)
    time.sleep(4)

    # Colocar email
    obtem_elemento(driver, '//*[@id="user-email"]').send_keys(EMPIRICA_EMAIL)

    # Seleciona próximo
    obtem_elemento(driver, '//*[@id="login-button"]').click()
    time.sleep(2)

    # Seleciona Entrar com login Único
    obtem_elemento(driver, '//*[@id="login-button"]').click()
    time.sleep(2)

    # Seleciona Continuar
    obtem_elemento(driver, '//*[@id="login-submit"]').click()
    time.sleep(2)

    # Digita a senha
    obtem_elemento(driver, '//*[@id="password"]').send_keys(SENHA_JIRA)

    # Seleciona Continuar
    obtem_elemento(driver, '//*[@id="login-submit"]').click()
    time.sleep(2)

    try:
        mostrar_mais = obtem_elemento(
            driver, '//*[@id="root"]/div[1]/div/div/div[2]/main/div[2]/div[2]/div[1]/div[2]/div[1]/button/span')
        driver.execute_script("arguments[0].scrollIntoView();", mostrar_mais)
        mostrar_mais.click()
        #print("Clicou mostrar mais")
        div_documentos = obtem_elemento(
            driver, '//*[@id="root"]/div[1]/div/div/div[2]/main/div[2]/div[2]/div[1]/div[2]/div[2]')
        driver.execute_script("arguments[0].scrollIntoView();", div_documentos)

        i = 1
        falhou = False
        while not falhou:
            try:
                # Clica no documento
                obtem_elemento(
                    driver, f'//*[@id="root"]/div[1]/div/div/div[2]/main/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div[{i}]/div/div/div/div/div[2]').click()
                time.sleep(2)

                # Clica no botão de download
                obtem_elemento(
                    driver, '/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/button').click()
                time.sleep(2)

                # Fecha o primeiro documento
                obtem_elemento(
                    driver, '/html/body/div[4]/div/div/div[1]/button').click()
                time.sleep(2)

                i += 1
            except:
                falhou = True

    except:
        # Recolhe para a div documentos
        div_documentos = obtem_elemento(
            driver, '//*[@id="root"]/div[1]/div/div/div[2]/main/div/div[2]/div[1]/div[2]')
        driver.execute_script("arguments[0].scrollIntoView();", div_documentos)
        time.sleep(2)
        #print("Documetos visíveis")
        i = 1
        falhou = False
        while not falhou:
            try:
                # Clica no documento
                obtem_elemento(
                    driver, f'//*[@id="root"]/div[1]/div/div/div[2]/main/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div[2]/div/div[{i}]/div/div/div/div/div[2]').click()
                time.sleep(2)

                # Clica no botão de download
                obtem_elemento(
                    driver, '/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/button').click()
                time.sleep(2)

                # Fecha o primeiro documento
                obtem_elemento(
                    driver, '/html/body/div[4]/div/div/div[1]/button').click()
                time.sleep(2)

                i += 1
            except:
                falhou = True


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
                    descricoes.append(
                        get_obs(b, transform_string(splited_text[i+9])))

                # Colhe o link do Jira
                if splited_text[i].strip() == "Observações":
                    try:
                        link = splited_text[i +
                                            1].strip().split('Jira:')[1].strip()
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
    path = str(
        r'C:\Users' f'\\{EMPIRICA_USER}' r'\Empírica Investimentos Gestão de Recursos Ltda\ESCO - Documentos\5 - Avaliacoes de Imoveis\Laudos Creditas\novos_laudos.xlsx')
    df.to_excel(path, sheet_name='Sheet1')


if __name__ == '__main__':
    bodys = get_bodys()
    parse_informations(bodys)
