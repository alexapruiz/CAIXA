# Importando as bibliotecas
import os
import sys

sys.path.insert(0, 'c://Projetos//CAIXA//Funcoes')
from BancodeDados import SQLite


def CriaArquivoPolitica():

    with open(caminho + f"\\Arquivos\\ACL\\Policy_CAIXA.txt",mode="w",encoding="UTF-8") as arquivo_politica:
        arquivo_politica.write("[vob]\n")
        arquivo_politica.write("Role:Escrita Read\n")
        arquivo_politica.write("Role:Leitura Read\n")
        arquivo_politica.write("Role:ADM Full\n")
        arquivo_politica.write("[element]\n")
        arquivo_politica.write("Role:Leitura Read\n")
        arquivo_politica.write("Role:Escrita mod-label,Change\n")
        arquivo_politica.write("Role:ADM Full\n")
        arquivo_politica.write("[policy]\n")
        arquivo_politica.write("Role:Escrita Read\n")
        arquivo_politica.write("Role:ADM Full\n")
        arquivo_politica.write("Role:Leitura Read\n")
        arquivo_politica.write("[rolemap]\n")
        arquivo_politica.write("Role:Escrita Read\n")
        arquivo_politica.write("Role:ADM Full\n")
        arquivo_politica.write("Role:Leitura Read\n")


def CriaArquivoACLsemFabrica(COMUNIDADE,LISTA_GRUPOS_COMUNIDADE):
    
    try:
	    # Rolemap_leitura
        with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_leitura.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
            arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
            for GRUPO in LISTA_GRUPOS_COMUNIDADE:
                 arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO}" + "\n")

        # Rolemap_caixa
        with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_caixa.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
            arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
            for GRUPO in LISTA_GRUPOS_COMUNIDADE:
                 arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO}" + "\n")

        # Rolemap_desenvolvimento
        with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_desenvolvimento.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
            arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
            for GRUPO in LISTA_GRUPOS_COMUNIDADE:
                 arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO}" + "\n")

        # Rolemap_metrica
        with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_metrica.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
            arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
            for GRUPO in LISTA_GRUPOS_COMUNIDADE:
                 arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO}" + "\n")

        # Rolemap_certificacao
        with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_certificacao.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
            arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
            for GRUPO in LISTA_GRUPOS_COMUNIDADE:
                 arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO}" + "\n")

        # Rolemap_todos
        with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_todos.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
            arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
            for GRUPO in LISTA_GRUPOS_COMUNIDADE:
                 arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO}" + "\n")

    except Exception as erro:
        print(f"Ocorreu um erro durante a geracao dos arquivos ACL -  [' {erro}' ]")


def LeArquivosGruposACL():
	# Le os dados dos grupos de comunidades e fábricas e atualiza a tabela GRUPOS_ACL
    try:

        BancodeDados.ExecutaComandoSQL(f"delete from GRUPOS_ACL")

        arquivo_grupos_comunidades = open(caminho + f"\\Arquivos\\GRUPOS_COMUNIDADES.txt",mode="r",encoding="UTF-8")
    
        for linha in arquivo_grupos_comunidades:
            linha = linha.upper()
            COMUNIDADE = linha[13:linha.find("-DEV")]
            GRUPO_COMUNIDADE = linha[linha.find("G "):linha.find(",OU")]
            BancodeDados.ExecutaComandoSQL(f"Insert Into GRUPOS_ACL (COMUNIDADE,FABRICA,GRUPO,TIPO) Values ('{COMUNIDADE}','','{GRUPO_COMUNIDADE}','C')")

        arquivo_grupos_comunidades.close

        arquivo_grupos_fabricas = open(caminho + f"\\Arquivos\\GRUPOS_FABRICAS.txt",mode="r",encoding="UTF-8")
		
        for linha in arquivo_grupos_fabricas:
            linha = linha.upper()
            COMUNIDADE = linha[13:linha.find("-DEV")]
            FABRICA = linha[linha.find("-DEV") + 5 : linha.find(",OU")]
            FABRICA = FABRICA.upper()
            GRUPO_FABRICA = linha[linha.find("G "):linha.find(",OU")]
            BancodeDados.ExecutaComandoSQL(f"Insert Into GRUPOS_ACL (COMUNIDADE,FABRICA,GRUPO,TIPO) Values ('{COMUNIDADE}','{FABRICA}','{GRUPO_FABRICA}','F')")

        arquivo_grupos_fabricas.close

    except Exception as erro:
        print(f"Ocorreu um erro durante a leitura dos grupos -  [' {erro}' ]")


def Gera_Arquivos_ACL():
    # Le os dados das VOBs / grupos e gera os arquivos de cada Comunidade x Fabrica

    CriaArquivoPolitica()

    try:
        cursor_comunidades = BancodeDados.ConsultaSQL("SELECT DISTINCT(COMUNIDADE) FROM GRUPOS_ACL where tipo = 'C' ORDER BY COMUNIDADE")
        COMUNIDADES = cursor_comunidades.fetchone()
        while COMUNIDADES:
            # Para cada comunidade, pesquisar os grupos da comunidade e os grupos de cada fabrica
            COMUNIDADE = COMUNIDADES[0]
            LISTA_GRUPOS_COMUNIDADE = []
            
            cursor_grupos_comunidades = BancodeDados.ConsultaSQL(f"SELECT GRUPO FROM GRUPOS_ACL where COMUNIDADE = '{COMUNIDADE}' AND TIPO = 'C'")
            GRUPOS_COMUNIDADE = cursor_grupos_comunidades.fetchone()
            while GRUPOS_COMUNIDADE:

                LISTA_GRUPOS_COMUNIDADE.append(GRUPOS_COMUNIDADE[0])
                GRUPOS_COMUNIDADE = cursor_grupos_comunidades.fetchone()
            
            os.mkdir(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}")
            CriaArquivoACLsemFabrica(COMUNIDADE,LISTA_GRUPOS_COMUNIDADE)

            # Para cada comunidade, pesquisar as fabricas
            cursor_fabricas = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(FABRICA) FROM GRUPOS_ACL where COMUNIDADE = '{COMUNIDADE}' AND TIPO = 'F'")
            FABRICAS = cursor_fabricas.fetchone()
            while FABRICAS:
                LISTA_GRUPOS_FABRICAS=[]
                FABRICA = FABRICAS[0]

                # Para cada fabrica, pesquisar os grupos
                cursor_grupos_fabricas = BancodeDados.ConsultaSQL(f"SELECT GRUPO FROM GRUPOS_ACL WHERE COMUNIDADE = '{COMUNIDADE}' AND FABRICA = '{FABRICA}'")
                GRUPOS_FABRICAS = cursor_grupos_fabricas.fetchone()
                while GRUPOS_FABRICAS:
                    LISTA_GRUPOS_FABRICAS.append(GRUPOS_FABRICAS[0].strip())
                    GRUPOS_FABRICAS = cursor_grupos_fabricas.fetchone()

                # Criar as pastas da fabrica, dentro da comunidade
                os.mkdir(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}")

                # Rolemap_leitura
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_leitura.txt", mode="w",encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_caixa
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_caixa.txt", mode="w",encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_desenvolvimento
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_desenvolvimento.txt", mode="w",encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_metrica
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_metrica.txt", mode="w",encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_certificacao
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_certificacao.txt", mode="w",encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_todos
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_todos.txt", mode="w",encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                FABRICAS = cursor_fabricas.fetchone()

            COMUNIDADES = cursor_comunidades.fetchone()


    except Exception as erro:
        print(f"Ocorreu um erro durante a geracao dos arquivos ACL -  [' {erro}' ]")


caminho = sys.path[1]

# Abre a conexao do banco de dados
BancodeDados = SQLite(f"{caminho}\\Clearcase.db")

# Armazena os grupos
LeArquivosGruposACL()

# Gera os arquivos de configuracao do ACL
Gera_Arquivos_ACL()

print("Os arquivos de configuração do ACL foram gerados com sucesso!!!")