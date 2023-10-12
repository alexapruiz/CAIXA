# Abrindo os arquivos de entrada e saida
entrada = open("saida_dir.txt", mode='r', encoding='UTF-8')
saida = open("resultado_analise_dir.csv", mode='w', encoding='UTF-8')

VOB=''
PLANEJAMENTO=''
EXECUCAO=''
MASSA=''

# Gravando a primeira linha, com o cabeçalho
saida.write('VOB;PLANEJAMENTO;EXECUCAO;MASSA')
saida.write('\n')

for linha in entrada:
    if linha.find('Directory of M') != -1:
        # Encontrou a linha inicial
        posicao1 = 31
        posicao2 = linha.find('04-Testes\Certificacao') -1
        VOB = linha[posicao1:posicao2]

    elif linha.find('<DIR>          Planejamento')!= -1:
        PLANEJAMENTO = 'OK'

    elif linha.find('<DIR>          Execucao')!= -1:
        EXECUCAO = 'OK'

    elif linha.find('<DIR>          Massa')!= -1:
        MASSA = 'OK'

    elif linha.find('Volume in drive M is CCase')!= -1:
        saida.write(VOB + ';' + PLANEJAMENTO + ';' + EXECUCAO + ';' + MASSA + '\n')

        VOB=''
        PLANEJAMENTO=''
        EXECUCAO=''
        MASSA=''

entrada.close
saida.close