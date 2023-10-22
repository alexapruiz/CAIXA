usuarios = open('users.txt','r')
arquivo_saida = open('creds.txt','w')

for linha in usuarios:
  posicao = linha.find('@mail')
  if posicao > 0:
    #encontrou o usuario
    user_atual = linha[posicao-8:-14]
    saida = 'creds -c ' + user_atual + '\n'
    print(saida)
    arquivo_saida.write(saida)

print('Comandos gerados com sucesso!!!')