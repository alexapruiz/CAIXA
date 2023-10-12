import sys

# Abrindo o arquivo de entrada
arquivo_entrada = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\Todos_Grupos_Compart.txt',mode='r',encoding='UTF-8')
arquivo_saida = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\Saida_Todos_Grupos_Compart.txt',mode='w',encoding='UTF-8')

GRUPO = ''
GRUPOS = ''
for linha in arquivo_entrada:
    linha = linha.upper()
    if GRUPOS.find(linha) == -1:
        GRUPOS += linha

arquivo_saida.write(GRUPOS)

arquivo_entrada.close()
arquivo_saida.close()
