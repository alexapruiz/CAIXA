# Abrindo os arquivos de entrada e saida
entrada = open('C:\Projetos\CAIXA\scripts\Clearcase\Arquivos\DESC.txt',mode='r',encoding='UTF-8')
saida = open('C:\Projetos\CAIXA\scripts\Clearcase\Arquivos\VOBs_ACL.txt',mode='w',encoding='UTF-8')

VOB=''
ACL = False
for linha in entrada:
    linha = linha.upper()
    if linha.find("VERSIONED") != -1:
        if (VOB == ''):
            VOB=linha[24:-2]
        else:
            if ACL == True:
                saida.write(VOB + "\n")
                ACL = False

            VOB=linha[24:-2]

    if linha.find("ACLS FEATURE LEVEL") > -1:
        ACL = True


entrada.close()
saida.close()