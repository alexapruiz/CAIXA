from asyncio.windows_events import NULL
from datetime import datetime
import sqlite3
import sys


def ExecutaComandoSQL(ComandoSQL):
    # Executa o comando SQL recebido
    try:
        conexao = sqlite3.connect(sys.path[0] + '\Clearcase.db')
        conexao.execute(ComandoSQL)
        conexao.commit()
        conexao.close()

    except Exception as erro:
        print(f"Erro ao executar comando na base de dados - Erro: {erro}")


def ConsultaSQLite(ComandoSQL):
    # Executa a consulta SQL recebida e retorna um cursor, com o resultado
    try:
        conexao = sqlite3.connect(sys.path[0] + '\Clearcase.db')
        cursor = conexao.cursor()
        cursor.execute(ComandoSQL)
        return cursor
    
    except Exception as erro:
        print(f"Erro ao consultar a base de dados - Erro: {erro}")


def Le_Caso_Desenv_Inclui_Comunidade(arquivo_entrada,arquivo_saida):
    # Abre os arquivos de entrada e saida
    entrada = open(arquivo_entrada,mode='r',encoding='ANSI')
    saida = open(arquivo_saida,mode='w',encoding='UTF-8')
    saida.write("COMUNIDADE;VOB;CAMINHO_CASO_DESENV;VERSAO;DATA_ULTIMA_ALTERACAO\n")

    try:
        for linha in entrada:
            linha = linha.upper()
            if linha.find("LOST+") == -1:
                linha_quebrada = linha.split(";")
                SISTEMA = linha_quebrada[0].strip()

                ComandoSQL = f"SELECT * FROM SISTEMAS_COMUNIDADES WHERE SISTEMA = '{SISTEMA}'"
                cursor_COMUNIDADE = ConsultaSQLite(ComandoSQL)
                COMUNIDADE = cursor_COMUNIDADE.fetchone()
                if COMUNIDADE:
                    linha_saida = f"{COMUNIDADE[1][0:-1]};{linha}"
                else:
                    linha_saida = f"COMUNIDADE_NAO_ENCONTRADA;{linha}"

                saida.write(linha_saida)


    except Exception as erro:
        print(f"Erro na função 'Le_Dados_DESC_VOB' - Erro: {erro}")

    entrada.close


def Carrega_Arquivo_VOBs_Comunidades(arquivo):
    try:
        # Abre o arquivo com as informações das comunidades x VOBs
        entrada = open(arquivo,mode='r',encoding='ANSI')

        SISTEMA = ''
        COMUNIDADE = 0

        for linha in entrada:
            linha = linha.upper()
            linha = linha.split(";")
            SISTEMA = linha[0]
            COMUNIDADE = linha[1]

            ExecutaComandoSQL(f"INSERT INTO SISTEMAS_COMUNIDADES (SISTEMA , COMUNIDADE) VALUES ('{SISTEMA}','{COMUNIDADE}')")

        entrada.close

    except Exception as erro:
        print(f"Erro ao incluir relacao de sistemas x comunidades - Erro: {erro}")


def Inclui_Sistemas_Sem_CasoDesenv(arquivo):
    entrada = open(arquivo,mode='r',encoding='ANSI')
    saida = open(sys.path[0] + '\Caso_Desenv\VOBs_Sem_Caso_Desenv.csv',mode='w',encoding='UTF-8')
    saida.write("COMUNIDADE;VOB;CAMINHO_CASO_DESENV;VERSAO;DATA_ULTIMA_ALTERACAO\n")

    linha_saida=""
    for linha in entrada:
        SISTEMA = linha[0:-1]
        ComandoSQL = f"SELECT * FROM SISTEMAS_COMUNIDADES WHERE SISTEMA = '{SISTEMA}'"
        cursor_COMUNIDADE = ConsultaSQLite(ComandoSQL)
        COMUNIDADE = cursor_COMUNIDADE.fetchone()
        if not COMUNIDADE:
            saida.write(f"N/A;{SISTEMA};N/A;N/A;N/A\n")
            saida.write(linha_saida)


#Carrega_Arquivo_VOBs_Comunidades(sys.path[0] + '\Caso_Desenv\Relacao_Sistemas_Comunidades.txt')

#Le_Caso_Desenv_Inclui_Comunidade(sys.path[0] + '\Caso_Desenv\saida_20221019.csv',sys.path[0] + '\Caso_Desenv\saida_20221019_final.csv' )

Inclui_Sistemas_Sem_CasoDesenv(sys.path[0] + '\Caso_Desenv\Todos_sistemas.txt')
