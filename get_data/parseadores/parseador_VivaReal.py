import math

def get_adress(dom, idx):
    try:
        full_adress = dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{str(idx)}]/div/article/a/div/h2/span[2]/span[1]')[0].text.strip()
        
        if len(full_adress.split('-')) < 3:
            endereco = ""
            bairro = full_adress.split('-')[0].split(',')[0]
            cidade = full_adress.split('-')[0].split(',')[1][1:-1]
            estado = full_adress.split('-')[1][1:]
        else:
            endereco = full_adress.split('-')[0][0:-1]
            bairro = full_adress.split('-')[1].split(',')[0][1:]
            cidade = full_adress.split('-')[1].split(',')[1][1:-1]
            estado = full_adress.split('-')[2][1:]
        
        return estado, cidade, bairro, endereco
        

    except:
        return "", "", "", ""


def get_area(dom, idx):
    try:
        area = dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{str(idx)}]/div/article/a/div/ul/li[1]/span[1]')[0].text.strip()
        try:
            return int(area)
        except:
            x = int(area.split('-')[0].strip())
            y = int(area.split('-')[1].strip())
            return int((x+y)/2)
    except:
        return 0


def get_quartos(dom, idx):
    try: 
        quartos = dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{str(idx)}]/div/article/a/div/ul[1]/li[2]/span[1]')[0].text.strip()
        try:
            quartos = int(quartos)
        except:
            quartos = math.ceil(float((quartos.split('-')[0] + quartos.split('-')[1])/2))

    except:
        quartos = 0
    
    return quartos


def get_banheiros(dom, idx):
    try:
        
        banheiros = dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{str(idx)}]/div/article/a/div/ul/li[3]/span[1]')[0].text.strip()
    except:
        banheiros = ""
    
    return banheiros


def get_vagas(dom, idx):
    try:
        vagas = dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{str(idx)}]/div/article/a/div/ul[1]/li[4]/span[1]')[0].text.strip()
    except:
        vagas = ""
    
    return vagas


def get_preco(dom, idx):
    try:
        preco = dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{str(idx)}]/div/article/a/div/section/div/p')[0].text.strip()
    except:
        preco = ""
    
    return preco


def get_link(dom, idx):
    try:
        link = dom.xpath(f'/html/body/main/div[2]/div[1]/section/div[2]/div[1]/div[{str(idx)}]/div/article/a/@href')[0]
    except:
        link = ""
    
    return link


def get_next_page(dom, tipo):
    try:
        if tipo == 'Casa':
            next_page = dom.xpath(f'//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[8]/a/@href')[0]
        elif tipo == 'Loteamento':
            next_page = dom.xpath(f'//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[4]/a/@href')[0]
        else:
            next_page = dom.xpath(f'//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a/@href')[0]

    except:
        correto = False
        n = 1
        while not correto:
            try:
                next_page = dom.xpath(f'//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[{n}]/a/@href')[0]
                correto = True
            except:
                n += 1
    
    return next_page