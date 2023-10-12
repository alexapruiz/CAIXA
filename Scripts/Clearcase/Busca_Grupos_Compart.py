import sys

# Abrindo o arquivo de entrada
arquivo_entrada = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\NET_SHARE_CEPEM.txt',mode='r',encoding='UTF-8')
arquivo_saida = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\Grupos_Compart_CEPEM.txt',mode='w',encoding='UTF-8')

GRUPO = ''
GRUPOS = ''
for linha in arquivo_entrada:
    linha = linha.upper()
    if linha.find("CORPCAIXA\\") > -1:
        GRUPO = linha[linha.find("CORPCAIXA"):linha.find(",")]
        if GRUPOS.find(GRUPO) == -1:
            GRUPOS += GRUPO + "\n"


arquivo_saida.write(GRUPOS)

arquivo_entrada.close()
arquivo_saida.close()
