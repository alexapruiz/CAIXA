import sys
import os
import shutil

sys.path.insert(0, 'c://projetos//CAIXA//Funcoes')
from BancodeDados import SQLite

def LimpaTabelas():
    # Grava os dados da VOB
    try:
        BancodeDados.ExecutaComandoSQL(f"DELETE FROM DADOS_ACL_VOBS")
        BancodeDados.ExecutaComandoSQL(f"DELETE FROM DADOS_ACL_GRUPOS")

    except Exception as erro:
        print(f"Ocorreu um erro durante a limpeza das tabelas -  [' {erro}' ]")


def GravaDadosVOB(VOB,ACL_ATIVADO,COMUNIDADE,FABRICA):
    # Grava os dados da VOB
    try:
        BancodeDados.ExecutaComandoSQL(f"INSERT INTO DADOS_ACL_VOBs (VOB,COMUNIDADE,FABRICA,ACL_ATIVADO) VALUES ('{VOB}','{COMUNIDADE}','{FABRICA}','{ACL_ATIVADO}')")

    except Exception as erro:
        print(f"Ocorreu um erro durante a gravacao dos dados das VOBs -  [' {erro}' ]")


def GravaDadosGrupos(VOB,GRUPO,COMUNIDADE,FABRICA,TIPO):
    # Grava os grupos encontrados na VOB
    try:
        BancodeDados.ExecutaComandoSQL(f"INSERT INTO DADOS_ACL_GRUPOS (VOB,GRUPO,COMUNIDADE,FABRICA,TIPO) VALUES ('{VOB}','{GRUPO}','{COMUNIDADE}','{FABRICA}','{TIPO}')")

    except Exception as erro:
        print(f"Ocorreu um erro durante a gravacao dos grupos das VOBs -  [' {erro}' ]")


def CriaArquivoACLsemFabrica(COMUNIDADE,LISTA_GRUPOS_COMUNIDADE):
    # Rolemap_leitura
    with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_leitura.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
        arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
        for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

    # Rolemap_caixa
    with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_caixa.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
        arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
        for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

    # Rolemap_desenvolvimento
    with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_desenvolvimento.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
        arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
        for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

    # Rolemap_metrica
    with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_metrica.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
        arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")
        for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

    # Rolemap_certificacao
    with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_certificacao.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
        arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
        for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
            arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

    # Rolemap_todos
    with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_todos.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
        arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
        for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
            arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")


def LeDESC():
    # Abre o arquivo com o DESC de todas as VOBs e para aquelas que estáo no ACL, armazena as informações dos grupos em uma base de dados

    VOB = ""
    ACL_ATIVADO = False
    COMUNIDADE = ""
    FABRICA = ""
    ENCONTROU_FABRICA = False
    GRUPOS_COMUNIDADES = "SEM_COMUNIDADE_FABRICA;ARRECADACAO;CAMBIO;CANAIS_DIGITAIS;CANAIS_FISICOS;CLIENTES;CONTRATACOES;CREDITO;DADOS;DEPOSITO;ESTRUTURANTES_TI;FINANCEIRO_CONTROLADORIA;FOMENTO_DJ;FUNDOS_GOVERNO;HABITACAO;INSTITUCIONAL;LOTERIAS;MEIOS_PAGAMENTO;PESSOAS;PROGRAMAS_SOCIAIS;RISCO;SEGURANCA"
    LISTA_COMUNIDADES = GRUPOS_COMUNIDADES.split(";")
    GRUPOS_FABRICAS = "ATOS;BENNER;BRQ;BRY;CAST;CPQD;DATAINFO;DBA;ESEC;FIRST;FOTON;GLOBALWEB;INDRA;LATIN;MAGNA;MAPS;MURAH;PEOPLEWARE;RESOURCE;RJE;SENIOR;SONDA;SPREAD;STEFANINI;TIVIT;TREE;TTY;UNISYS;VERT_SAS;WIPRO"
    LISTA_FABRICAS = GRUPOS_FABRICAS.split(";")

    try:
        with open("C:\\projetos\\CAIXA\\Scripts\\Clearcase\\Arquivos\\DESC.txt", mode='r', encoding='UTF-8') as arquivo:
            for linha in arquivo:
                linha2 = linha.upper()

                if linha2.find("VERSIONED OBJECT BASE") > -1:
                    if VOB == "":
                        # Apenas na primeira VOB
                        VOB = linha2.split("\\")[1].split('"')[0]
                    else:
                        GravaDadosVOB(VOB,ACL_ATIVADO,COMUNIDADE,FABRICA)

                        VOB = linha2.split("\\")[1].split('"')[0]
                        ACL_ATIVADO = False
                        COMUNIDADE = ""
                        FABRICA = ""
                        ENCONTROU_FABRICA = False

                if linha2.find("ACLS FEATURE LEVEL") > -1:
                    ACL_ATIVADO = True

                if linha2.find("ACLS ENABLED: NO") > -1:
                    ACL_ATIVADO = False

                if linha2.find("GROUP:CORPCAIXA") > -1:
                    for item_comunidade in LISTA_COMUNIDADES:
                        ENCONTROU_FABRICA = False
                        if linha2.find(item_comunidade) > -1:
                            COMUNIDADE = item_comunidade
                            for item_fabrica in LISTA_FABRICAS:
                                if linha2.find(item_fabrica) > -1:
                                    FABRICA = item_fabrica
                                    ENCONTROU_FABRICA = True
                                    GravaDadosGrupos(VOB, linha2.split("\\")[1].split("READ\n")[0].strip(), COMUNIDADE,FABRICA, 'F')
                                    break

                            if ENCONTROU_FABRICA == False:
                                GravaDadosGrupos(VOB, linha2.split("\\")[1].split("READ")[0].strip(), COMUNIDADE, FABRICA, 'C')



    except Exception as erro:
        print(f"Ocorreu um erro durante a analise do arquivo DESC.txt - ACL_Le_DESC_Grupos - [' {erro}' ]")


def Gera_Arquivos_ACL():
    # Le os dados das VOBs e gera os arquivos de cada Comunidade x Fabrica
    try:
        cursor_comunidades = BancodeDados.ConsultaSQL("SELECT DISTINCT(COMUNIDADE) FROM DADOS_ACL_VOBS where COMUNIDADE IS NOT NULL AND COMUNIDADE <> '' ORDER BY COMUNIDADE")
        COMUNIDADES = cursor_comunidades.fetchone()
        while COMUNIDADES:
            # Para cada comunidade, pesquisar os grupos da comunidade e os grupos de cada fabrica
            COMUNIDADE = COMUNIDADES[0].strip()

            cursor_grupos_comunidades = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(GRUPO) FROM DADOS_ACL_GRUPOS WHERE COMUNIDADE = '{COMUNIDADE}' and TIPO = 'C'")
            GRUPOS_COMUNIDADE = cursor_grupos_comunidades.fetchone()
            LISTA_GRUPOS_COMUNIDADE=[]
            LISTA_GRUPOS_FABRICAS = []
            while GRUPOS_COMUNIDADE:
                LISTA_GRUPOS_COMUNIDADE.append(GRUPOS_COMUNIDADE[0])

                GRUPOS_COMUNIDADE = cursor_grupos_comunidades.fetchone()

            os.mkdir(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}")

            CriaArquivoACLsemFabrica(COMUNIDADE,LISTA_GRUPOS_COMUNIDADE)

            # Para cada comunidade, pesquisar as fabricas
            cursor_fabricas = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(FABRICA) FROM DADOS_ACL_VOBS where COMUNIDADE = '{COMUNIDADE}' AND FABRICA <> ''")
            FABRICAS = cursor_fabricas.fetchone()
            while FABRICAS:
                LISTA_GRUPOS_FABRICAS=[]
                FABRICA = FABRICAS[0]

                # Para cada fabrica, pesquisar os grupos
                cursor_grupos_fabricas = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(GRUPO) FROM DADOS_ACL_GRUPOS WHERE COMUNIDADE = '{COMUNIDADE}' AND FABRICA = '{FABRICA}' AND TIPO = 'F'")
                GRUPOS_FABRICAS = cursor_grupos_fabricas.fetchone()
                while GRUPOS_FABRICAS:
                    LISTA_GRUPOS_FABRICAS.append(GRUPOS_FABRICAS[0].strip())
                    GRUPOS_FABRICAS = cursor_grupos_fabricas.fetchone()

                # Criar as pastas da fabrica, dentro da comunidade
                os.mkdir(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}")

                # Rolemap_leitura
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_leitura.txt", mode="w",
                          encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_caixa
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_caixa.txt", mode="w",
                          encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_desenvolvimento
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_desenvolvimento.txt", mode="w",
                          encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_metrica
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_metrica.txt", mode="w",
                          encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_certificacao
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_certificacao.txt", mode="w",
                          encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                # Rolemap_todos
                with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_todos.txt", mode="w",
                          encoding="UTF-8") as arquivo_rolemap:
                    arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
                    arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
                    arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
                    for GRUPO_COMUNIDADE in LISTA_GRUPOS_COMUNIDADE:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_COMUNIDADE}" + "\n")

                    for GRUPO_FABRICA in LISTA_GRUPOS_FABRICAS:
                        arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{GRUPO_FABRICA}" + "\n")

                FABRICAS = cursor_fabricas.fetchone()

            COMUNIDADES = cursor_comunidades.fetchone()


    except Exception as erro:
        print(f"Ocorreu um erro durante a geracao dos arquivos ACL -  [' {erro}' ]")


# Verifica se esta sendo chamado por um interpretador python ou executavel
if __name__ == "__main__":
    caminho = sys.path[1]

    # Abre a conexao do banco de dados
    BancodeDados = SQLite(f"{caminho}\\Clearcase.db")

    if os.path.isdir(caminho + "\\Arquivos\\ACL"):
        shutil.rmtree(caminho + "\\Arquivos\\ACL")

    os.mkdir(caminho + f"\\Arquivos\\ACL")

    LimpaTabelas()

    LeDESC()

    Gera_Arquivos_ACL()