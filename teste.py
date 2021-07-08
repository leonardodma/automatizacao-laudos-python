from pathlib import Path
from unidecode import unidecode

def concerta_str(string):
    string.to
    pass

def get_file():
        path = str(r'R:\Empírica Cobranças e Garantias\5 - Avaliações de Imóveis\Projeto estágio de férias\vba.txt')
        print(f'O arquivo contendo o path do laudo é: {path}')
        print('\n')

        file = str(r"R:\Empírica Cobranças e Garantias\5 - Avaliações de Imóveis")
    
        #txt = Path(path).read_text()
        with open(path, 'r') as f:
            txt = unidecode(f.read())

        print(txt)
        print(txt.split(' '))
        """
        a = []
        for i in range(0, len(txt.split(" "))):
            a.append(txt.split(" ")[i].encode('latin1').decode('utf-8'))

        print(a)
        """
        return None

import easygui
print(easygui.fileopenbox())
