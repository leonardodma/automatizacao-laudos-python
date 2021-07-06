full_adress = 'Jardim Aeroporto, São Paulo - SP'
endereco = ""
bairro = full_adress.split('-')[0].split(',')[0]
cidade = full_adress.split('-')[0].split(',')[1][1:-1]
estado = full_adress.split('-')[1][1:]

print('---------'+endereco+'-----------')
print('---------'+bairro+'-----------')
print('---------'+estado+'-----------')
print('---------'+cidade+'-----------')