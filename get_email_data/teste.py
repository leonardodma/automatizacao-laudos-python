import win32com.client
import os
from datetime import datetime, timedelta
import pandas as pd
from utils import *

outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI")
solicitacoes = outlook.Folders['Avaliações'].Folders['Caixa de Entrada']
messages = solicitacoes.Items

solicitacao1 = 'Creditas - Solicitação de Laudo'
solicitacao2 = 'Creditas - Solicitação de Laudo Remoto'

fim = False
pedidos = 0
bodys = []
for msg in messages:
    subject_splited = msg.Subject.split(':')

    if len(subject_splited) > 1:
        if subject_splited[1].strip() == solicitacao1 or subject_splited[1].strip() == solicitacao2:
            bodys.append(msg.body)
            pedidos += 1
    
    if pedidos >= 5:
        break
