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


def Le_VOBs_GCs(arquivo_entrada):
    # Abre o arquivo de entrada
    entrada = open(arquivo_entrada,mode='r',encoding='UTF-8')

    try:
        for linha in entrada:
            linha = linha.upper()
            VOB = linha.split(";")[0].strip()
            GC = linha.split(";")[1].strip()

            ComandoSQL = f"INSERT INTO VOB_GC_COMUNIDADE (VOB,GC) VALUES ('{VOB}','{GC}')"
            ExecutaComandoSQL(ComandoSQL)

    except Exception as erro:
        print(f"Erro na função 'Le_VOBs_GCs' - Erro: {erro}")

    entrada.close


def Le_Comunidade_VOBs(arquivo_entrada):
    # Abre o arquivo de entrada
    entrada = open(arquivo_entrada,mode='r',encoding='UTF-8')

    try:
        for linha in entrada:
            linha = linha.upper()
            VOB = linha.split(";")[0].strip()
            COMUNIDADE = linha.split(";")[1].strip()

            ComandoSQL = f"UPDATE VOB_GC_COMUNIDADE SET COMUNIDADE = '{COMUNIDADE}' WHERE VOB = '{VOB}'"
            ExecutaComandoSQL(ComandoSQL)

    except Exception as erro:
        print(f"Erro na função 'Le_VOBs_GCs' - Erro: {erro}")


ExecutaComandoSQL("DELETE FROM VOB_GC_COMUNIDADE")
Le_VOBs_GCs(sys.path[0] + '\GCs_Comunidade\GCs.txt')
Le_Comunidade_VOBs(sys.path[0] + '\GCs_Comunidade\VOBs_Comunidades.txt')
