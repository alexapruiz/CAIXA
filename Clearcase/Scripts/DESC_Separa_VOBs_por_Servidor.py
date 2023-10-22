# Abrindo os arquivos de entrada e saida
entrada = open('C:\Projetos\CAIXA\scripts\Clearcase\Arquivos\DESC.txt',mode='r',encoding='UTF-8')
saida = open('C:\Projetos\CAIXA\scripts\Clearcase\Arquivos\VOBs_por_Servidor.csv',mode='w',encoding='UTF-8')
saida.write('VOB;SERVIDOR\n')

VOB=''
SERVIDOR=''
for linha in entrada:
    linha = linha.upper()
    if linha.find("VERSIONED") != -1:
        if (VOB == ''):
            VOB=linha[24:-2]
        else:
            saida.write(VOB + ";" + SERVIDOR + "\n")
            VOB=linha[24:-2]
            SERVIDOR=''

    if linha.find("CADSVAPRNT002") != -1:
        SERVIDOR = "SP"

    elif linha.find("CBRSVAPRNT005") != -1:
        SERVIDOR = "BR"

    elif linha.find("CADSVAPRNT009") != -1:
        SERVIDOR = "RJ"

    elif linha.find("CBRSVAPRNT010") != -1:
        SERVIDOR = "CEPEM"

    elif linha.find("CBRSVAPRNT013") != -1:
        SERVIDOR = "LOTERIAS"

entrada.close()
saida.close()