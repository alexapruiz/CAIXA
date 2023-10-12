import sys
import sqlite3


def ExecutaComandoSQL(ComandoSQL):
    # Executa o comando SQL recebido
    try:
        conexao = sqlite3.connect(sys.path[0] + '\Clearcase.db')
        conexao.execute(ComandoSQL)
        conexao.commit()
        conexao.close()
        return 0

    except Exception as erro:
        print(erro)

try:
    # Abrindo o arquivo de entrada
    with open(sys.path[0] + '\\Arquivos\\Pesquisa_Usuarios_Mod_1.csv',mode='r',encoding='UTF-8') as entrada:
        for linha in entrada:
            if len(linha) > 1:
                linha = linha.upper()
                linha = linha.replace("'","")
                linha = linha.replace(",",".")
                linha = linha.split(";")

                # Insere a linha na tabela
                retorno = ExecutaComandoSQL(f"INSERT INTO PESQUISA_USUARIOS_REQ (VOB,CAMINHO,USUARIO,DATA_MODIF) VALUES ('{linha[0]}','{linha[1]}','{linha[2]}','{linha[3]}')")
                if retorno != 0:
                    print("Erro")
except Exception as erro:
    print(erro)

print("Dados Usuarios REQ importados com sucesso!!!")