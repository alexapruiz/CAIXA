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
        print(erro)


def ConsultaSQLite(ComandoSQL):
    # Executa a consulta SQL recebida e retorna um cursor, com o resultado
    try:
        conexao = sqlite3.connect(sys.path[0] + '\Clearcase.db')
        cursor = conexao.cursor()
        cursor.execute(ComandoSQL)
        return cursor
    
    except Exception as erro:
        print(erro)


def Le_Dados_DESC_VOB(arquivo):
    # Limpa a tabela temporária
    ExecutaComandoSQL(f"DELETE FROM DADOS_VOB")

    # Abre o arquivo com resultado do DESC
    entrada = open(arquivo,mode='r',encoding='UTF-8')

    # Inicia as variaveis
    VOB=''
    SITE=''
    SERVIDOR=''
    DATA_CRIACAO=''
    DB_SCHEMA=''
    ACL_HABILITADO=''
    FEATURE_LEVEL=''
    POSSUI_GRUPO_DOMAIN_USERS='NAO'
    MODELO_SEGURANCA='VELHO'
    GRUPOS_LEITURA_ESCRITA = 'CAIXA_ESCRITA;TODOS_ESCRITA;METRICA;TRANSVERSAL;CERTIFICACAO'
    GRUPOS_FABRICAS = 'PEOPLEWARE;BRY;BENNER;SONDAS;RJE;ESEC;BRQ;ATOS;MURAH;VERT_SAS;DBA;MAGNA;INDRA;SENIOR;CAST;FOTON;STEFANINI;FIRST;UNISYS;RESOURCE;TIVIT;SPREAD;DATAINFO;GLOBALWEB;TTY;LATIN;QINTESS;MAPS;CPQD;RJY;TREE'

    for linha in entrada:
        linha = linha.upper()
        if linha.find("VERSIONED") != -1:
            VOB=linha[24:-2]

            SITE=''
            SERVIDOR=''
            DATA_CRIACAO=''
            DB_SCHEMA=''
            ACL_HABILITADO=''
            FEATURE_LEVEL=''
            POSSUI_GRUPO_DOMAIN_USERS='NAO'
            MODELO_SEGURANCA='VELHO'
            COMUNIDADE=''

        # Procura pelas comunidades
        if linha.find('CORPCAIXA\G DF5222 CC_') != -1:
            GRUPO_COMUNIDADE=linha[linha.find('CORPCAIXA\G DF5222 CC_') + 22: -1]
            if GRUPOS_LEITURA_ESCRITA.find(GRUPO_COMUNIDADE) == -1 and GRUPOS_FABRICAS.find(GRUPO_COMUNIDADE) == -1:
                COMUNIDADE += GRUPO_COMUNIDADE + '-'

        # Separa por servidor
        if linha.find("CADSVAPRNT002") != -1:
            SERVIDOR="CADSVAPRNT002"
            SITE = "SP"

        elif linha.find("CBRSVAPRNT005") != -1:
            SERVIDOR = "CBRSVAPRNT005"
            SITE = "BR"

        elif linha.find("CADSVAPRNT009") != -1:
            SERVIDOR = "CADSVAPRNT009"
            SITE = "RJ"

        elif linha.find("CBRSVAPRNT010") != -1:
            SERVIDOR = "CBRSVAPRNT010"
            SITE = "CEPEM"

        elif linha.find("CBRSVAPRNT013") != -1:
            SERVIDOR = "CBRSVAPRNT013"
            SITE = "LOTERIAS"

        # DATA DE CRIAÇÃO
        elif linha.find("CREATED") != -1:
            DATA_CRIACAO = datetime.strptime(linha[10:20], '%Y-%m-%d')

        # DATABASE SCHEMA
        elif linha.find("DATABASE SCHEMA VERSION") != -1:
            DB_SCHEMA = linha[27:-1]

        # ACL HABILITADO ?
        elif linha.find("ACLS ENABLED") != -1:
            ACL_HABILITADO = linha[16:-1]
            if ACL_HABILITADO == 'NO':
                ACL_HABILITADO = 'NAO'

        # ACL HABILITADO? - Sim
        elif linha.find("ACLS FEATURE LEVEL:") != -1:
            ACL_HABILITADO = 'SIM'
        
        # USUARIO SERVICO
        elif linha.find("OWNER ") != -1:
            USER_OWNER = linha[20:-1]

        # POSSUI GRUPO CORPCAIXA\DOMAIN USERS
        elif linha.find("CORPCAIXA\DOMAIN USERS") != -1:
            POSSUI_GRUPO_DOMAIN_USERS = 'SIM'

        # VERIFICA O MODELO DE SEGURANCA
        elif linha.find("DF5222") != -1:
            # Descarta se for o grupo CERTIFICACAO
            if linha.find("CC_CERTIFICACAO") == -1:
                MODELO_SEGURANCA = 'COMUNIDADES - (GRUPOS DF5222)'

        elif linha.find("CS7266") != -1:
            MODELO_SEGURANCA = 'SEGMENTO NEGOCIO SP - (GRUPOS CS7266)'

        elif (linha.find("CR7265") != -1) or (linha.find("RJ7265") != -1):
            MODELO_SEGURANCA = 'SEGMENTO NEGOCIO RJ - (GRUPOS CR7265 ou RJ7265)'

        elif (linha.find("DF7390") != -1):
            MODELO_SEGURANCA = 'SEGMENTO NEGOCIO BR - (GRUPOS DF7390)'

        elif (linha.find("DF5229") != -1):
            MODELO_SEGURANCA = 'GRUPO(S) DF5229)'

        # FEATURE LEVEL - ULTIMA INFORMAÇÃO DA VOB -> GRAVAR OS DADOS
        elif linha.find("FEATURELEVEL") != -1:
            FEATURE_LEVEL = linha[19:-1]
            try:
                ExecutaComandoSQL(f"INSERT INTO DADOS_VOB (VOB,SITE,SERVIDOR,COMUNIDADE,DATA_CRIACAO,DB_SCHEMA,ACL_HABILITADO,FEATURE_LEVEL,USER_OWNER,POSSUI_GRUPO_DOMAIN_USERS,MODELO_SEGURANCA) VALUES ('{VOB}','{SITE}','{SERVIDOR}','{COMUNIDADE[:-1]}','{DATA_CRIACAO}','{DB_SCHEMA}','{ACL_HABILITADO}','{FEATURE_LEVEL}','{USER_OWNER}','{POSSUI_GRUPO_DOMAIN_USERS}','{MODELO_SEGURANCA}')")
            except Exception as erro:
                print(f"Erro ao gravar os dados da VOB {VOB} - Erro: {erro}")

    entrada.close


def Le_Tamanho_VOBs_SPRJ(arquivo):
    try:
        # Abre o arquivo com os dados do tamanho das VOBs - comando 'cleartool space -update'
        entrada = open(arquivo,mode='r',encoding='UTF-8')

        VOB = ''
        TAMANHO = 0

        for linha in entrada:
            try:
                linha = linha.upper()
                if linha.find("TOTAL USAGE") != -1:
                    VOB = linha[linha.find("FOR VOB") + 10:linha.find("IS ")-2].strip()
                    TAMANHO = linha[linha.find("IS ") + 2:-3].strip()
                    TAMANHO = TAMANHO.replace(",",".")

                    ExecutaComandoSQL(f"UPDATE DADOS_VOB SET TAMANHO = {TAMANHO} WHERE VOB = '{VOB}'")

                    VOB = ''
                    TAMANHO = 0
            except Exception as erro:
                print(erro)

        entrada.close

    except Exception as erro:
        print(f"Erro na funcao 'Le_Tamanho_VOBs_SPRJ' - Erro: {erro}")


def Le_Tamanho_VOBs_BR(arquivo):
    # Abre o arquivo com os dados do tamanho das VOBs - comando 'cleartool space -directory'
    entrada = open(arquivo,mode='r',encoding='UTF-8')

    VOB = ''
    TAMANHO = 0

    for linha in entrada:
        try:
            linha = linha.upper()
            if linha.find(".VBS") != -1:
                VOB = linha[linha.find("\\") +1 : -5].strip()
                TAMANHO = linha[0:linha.find(",")+3].strip()
                TAMANHO = TAMANHO.replace(",",".")

                ExecutaComandoSQL(f"UPDATE DADOS_VOB SET TAMANHO = {TAMANHO} WHERE VOB = '{VOB}'")

                VOB = ''
                TAMANHO = 0
        except Exception as erro:
            print(erro)

    entrada.close


def Le_DIR_Pasta_Principal(arquivo):
    # Abre o arquivo com o resultado do comando DIR
    entrada = open(arquivo,mode='r',encoding='UTF-8')

    VOB = ''
    POSSUI_PASTA_MODELAGEM = 'NAO'
    MODELAGEM = 'NAO'
    REQUISITOS = 'NAO'
    ANALISE_DESIGN = 'NAO'
    IMPLEMENTACAO = 'NAO'
    TESTES = 'NAO'
    IMPLANTACAO = 'NAO'
    AMBIENTE = 'NAO'
    GARANTIA_QUALIDADE = 'NAO'
    GER_CONFIG_MUDANCA = 'NAO'
    GER_PROJETOS = 'NAO'
    GER_SUBCONTRATACAO = 'NAO'

    for linha in entrada:
        linha = linha.upper()
        if (linha.find('BYTES FREE') != -1) and (VOB != ''):
            # Verifica os flags e grava as informações
            if MODELAGEM == 'SIM':
                POSSUI_PASTA_MODELAGEM = 'SIM'

            # Se todas as pastas de disciplina (1-10) existirem, está no padrão
            if (REQUISITOS == 'SIM' and ANALISE_DESIGN == 'SIM' and IMPLEMENTACAO == 'SIM' and TESTES == 'SIM' and IMPLANTACAO == 'SIM' and AMBIENTE == 'SIM' and GARANTIA_QUALIDADE == 'SIM' and GER_CONFIG_MUDANCA == 'SIM' and GER_PROJETOS == 'SIM' and GER_SUBCONTRATACAO == 'SIM'):
                PADRAO_PASTAS = 'SIM'
            else:
                PADRAO_PASTAS = 'NAO'

            try:
                ExecutaComandoSQL(f"UPDATE DADOS_VOB SET PADRAO_PASTAS = '{PADRAO_PASTAS}' , POSSUI_PASTA_MODELAGEM = '{POSSUI_PASTA_MODELAGEM}' WHERE VOB = '{VOB}'")

                POSSUI_PASTA_MODELAGEM = 'NAO'
                MODELAGEM = 'NAO'
                REQUISITOS = 'NAO'
                ANALISE_DESIGN = 'NAO'
                IMPLEMENTACAO = 'NAO'
                TESTES = 'NAO'
                IMPLANTACAO = 'NAO'
                AMBIENTE = 'NAO'
                GARANTIA_QUALIDADE = 'NAO'
                GER_CONFIG_MUDANCA = 'NAO'
                GER_PROJETOS = 'NAO'
                GER_SUBCONTRATACAO = 'NAO'
            
            except Exception as erro:
                print(erro)

        try:
            # Verifica se é a quebra da VOB ou uma pasta
            if linha.find("DIRECTORY OF") != -1:
                VOB = linha.split("\\")[-1].strip()
            else:
                if linha.find("00-MODELAGEM_NEGOCIO") != -1:
                    MODELAGEM = 'SIM'
                if linha.find("01-REQUISITOS") != -1:
                    REQUISITOS = 'SIM'
                if linha.find("02-ANALISE_DESIGN") != -1:
                    ANALISE_DESIGN = 'SIM'
                if linha.find("03-IMPLEMENTACAO") != -1:
                    IMPLEMENTACAO = 'SIM'
                if linha.find("04-TESTES") != -1:
                    TESTES = 'SIM'
                if linha.find("05-IMPLANTACAO") != -1:
                    IMPLANTACAO = 'SIM'
                if linha.find("06-AMBIENTE") != -1:
                    AMBIENTE = 'SIM'
                if linha.find("07-GARANTIA_QUALIDADE") != -1:
                    GARANTIA_QUALIDADE = 'SIM'
                if linha.find("08-GER_CONFIG_MUDANCA") != -1:
                    GER_CONFIG_MUDANCA = 'SIM'
                if linha.find("09-GER_PROJETOS") != -1:
                    GER_PROJETOS = 'SIM'
                if linha.find("10-GER_SUBCONTRATACAO") != -1:
                    GER_SUBCONTRATACAO = 'SIM'
        except Exception as erro:
            print(erro)

    entrada.close


def Le_Dados_DESC_Pasta(arquivo):
    # Lê o arquivo com o DESC nas pastas FONTES e BUILD

    if 'FONTES' in arquivo:
        PASTA = 'FONTES'
    elif 'BUILD' in arquivo:
        PASTA = 'BUILD'

    # Abre o arquivo com resultado do DESC
    entrada = open(arquivo,mode='r',encoding='UTF-8')

    # Inicializa as variaveis
    VOB = ''
    USER = ''
    GRUPO = ''
    OUTROS = ''

    for linha in entrada:
        linha = linha.upper()
        if linha.find("DIRECTORY VERSION") != -1:
            if VOB == '':
                # Primeira linha, coleta o nome da VOB
                VOB=linha[19:-1].split("\\")[0]
            else:
                # Grava os dados coletados
                if PASTA == 'FONTES':
                    try:
                        ExecutaComandoSQL(f"UPDATE DADOS_VOB SET DESC_PASTA_FONTES = '{USER} - {GRUPO} - {OUTROS}' WHERE VOB = '{VOB}'")

                    except Exception as erro:
                        print(erro)

                elif PASTA == 'BUILD':
                    try:
                        ExecutaComandoSQL(f"UPDATE DADOS_VOB SET DESC_PASTA_BUILD = '{USER} - {GRUPO} - {OUTROS}' WHERE VOB = '{VOB}'")
                    
                    except Exception as erro:
                        print(erro)

                VOB = linha[19:-1].split("\\")[0]
                USER = ''
                GRUPO = ''
                OUTROS = ''

        try:
            # Pesquisa User Owner da pasta
            if linha.find("USER :") != -1:
                USER = linha.split(":")[1].strip() + " ( " + linha.split(":")[2][:-1].strip() + " ) "
                USER = USER.replace("CORPCAIXA\\", "")

            # Pesquisa Group Owner da pasta
            if linha.find("GROUP:") != -1:
                GRUPO = linha.split(":")[1].strip() + " ( " + linha.split(":")[2][:-1].strip() + " ) "
                GRUPO = GRUPO.replace("CORPCAIXA\\", "")

            # Pesquisa Other Groups da pasta
            if linha.find("OTHER:") != -1:
                OUTROS = "OUTROS: ( " + linha.split(":")[2][:-1].strip() + " )"
        
        except Exception as erro:
            print(erro)

    entrada.close


def Le_Dados_LOCK_Pasta(arquivo):
    # Lê arquivo com o resultado do comando CLEARTOOL LSLOCK, executado nas pastas FONTES e BUILD

    # Abre o arquivo com resultado do DESC
    entrada = open(arquivo,mode='r',encoding='UTF-8')

    if 'FONTES' in arquivo:
        PASTA = 'FONTES'
    elif 'BUILD' in arquivo:
        PASTA = 'BUILD'

    # Inicializa as variaveis
    VOB = ''

    for linha in entrada:
        linha = linha.upper()
        if linha.find("LOCK DIRECTORY ELEMENT") != -1:
            if VOB == '':
                # Primeira linha, coleta o nome da VOB
                VOB = linha[linha.find("ELEMENT") + 9:-1].split("\\")[0].strip()
            else:
                # Grava os dados coletados
                if PASTA == 'FONTES':
                    try:
                        ExecutaComandoSQL(f"UPDATE DADOS_VOB SET LOCK_PASTA_FONTES = 'SIM' WHERE VOB = '{VOB}'")

                    except Exception as erro:
                        print(erro)

                elif PASTA == 'BUILD':
                    try:
                        ExecutaComandoSQL(f"UPDATE DADOS_VOB SET LOCK_PASTA_BUILD = 'SIM' WHERE VOB = '{VOB}'")
                    
                    except Exception as erro:
                        print(erro)

                VOB = linha[linha.find("ELEMENT") + 9:-1].split("\\")[0].strip()

    entrada.close


def Le_DIR(arquivo):
    # Lê o arquivo com o resultado do DIR e identifica as atualizações mais recentes da VOB, da pasta FONTES e da pasta BUILD
    
    # Abre o arquivo
    entrada = open(arquivo,mode='r',encoding='UTF-8')

    # Inicializa as variaveis
    VOB = ''
    DATA = ''
    DIA = 0
    MES = 0
    ANO = 0
    DATA_ULTIMA_ALTERACAO_VOB = 0
    DATA_ULTIMA_ALTERACAO_FONTES = 0
    DATA_ULTIMA_ALTERACAO_BUILD = 0
    CAMPO_DATA_ULTIMA_ALTERACAO_VOB = ''
    CAMPO_DATA_ULTIMA_ALTERACAO_FONTES = ''
    CAMPO_DATA_ULTIMA_ALTERACAO_BUILD = ''
    LINHA_FONTES = False
    LINHA_BUILD = False

    for linha in entrada:
        linha = linha.upper()
        if linha.find("DIRECTORY OF") != -1:
            if VOB == '':
                # Primeira linha, coleta o nome da VOB
                VOB = linha.split("\\")[2].strip()
            else:
                if VOB != linha.split("\\")[2].strip():
                    try:
                        if CAMPO_DATA_ULTIMA_ALTERACAO_VOB != 0:
                            CAMPO_DATA_ULTIMA_ALTERACAO_VOB = DATA_ULTIMA_ALTERACAO_VOB[-2:] + '/' + DATA_ULTIMA_ALTERACAO_VOB[-4:-2] + '/' + DATA_ULTIMA_ALTERACAO_VOB[0:4]

                        if DATA_ULTIMA_ALTERACAO_FONTES != 0:
                            CAMPO_DATA_ULTIMA_ALTERACAO_FONTES = DATA_ULTIMA_ALTERACAO_FONTES[-2:] + '/' + DATA_ULTIMA_ALTERACAO_FONTES[-4:-2] + '/' + DATA_ULTIMA_ALTERACAO_FONTES[0:4]

                        if DATA_ULTIMA_ALTERACAO_BUILD != 0:
                            CAMPO_DATA_ULTIMA_ALTERACAO_BUILD = DATA_ULTIMA_ALTERACAO_BUILD[-2:] + '/' + DATA_ULTIMA_ALTERACAO_BUILD[-4:-2] + '/' + DATA_ULTIMA_ALTERACAO_BUILD[0:4]

                        ExecutaComandoSQL(f"UPDATE DADOS_VOB SET DATA_ULTIMA_ALTERACAO_VOB = '{CAMPO_DATA_ULTIMA_ALTERACAO_VOB}' , DATA_ULTIMA_ALTERACAO_FONTES = '{CAMPO_DATA_ULTIMA_ALTERACAO_FONTES}' , DATA_ULTIMA_ALTERACAO_BUILD = '{CAMPO_DATA_ULTIMA_ALTERACAO_BUILD}' WHERE VOB = '{VOB}'")
                        CAMPO_DATA_ULTIMA_ALTERACAO_VOB = ''
                        CAMPO_DATA_ULTIMA_ALTERACAO_FONTES = ''
                        CAMPO_DATA_ULTIMA_ALTERACAO_BUILD = ''
                        DATA_ULTIMA_ALTERACAO_VOB = 0
                        DATA_ULTIMA_ALTERACAO_FONTES = 0
                        DATA_ULTIMA_ALTERACAO_BUILD = 0
                        LINHA_FONTES = False
                        LINHA_BUILD = False
                        VOB = linha.split("\\")[2].strip()

                    except Exception as erro:
                        print(erro)
                else:
                    if linha.find("03-IMPLEMENTACAO\FONTES") != -1:
                        LINHA_FONTES = True
                        LINHA_BUILD = False
                    elif linha.find("05-IMPLANTACAO\BUILD") != -1:
                        LINHA_FONTES = False
                        LINHA_BUILD = True
                    else:
                        LINHA_FONTES = False
                        LINHA_BUILD = False
        else:
            if linha.find("/") != -1 and linha.find("LOST+FOUND") == -1 and linha.find("<DIR>") == -1:
                # Se os primeiros 10 caracteres corresponderem à uma data válida, considerar a linha
                DATA = linha[0:10]
                DATA = DATA.split("/")
                DIA = int(DATA[0])
                MES = int(DATA[1])
                ANO = int(DATA[2])

                if (DIA >= 1 and DIA <= 31) and (MES >= 1 and MES <= 12) and (ANO >= 1999 and ANO <= 2022):
                    # É uma data válida -> Verificar se a data é mais recente que a atualmente armazenada
                    if int(DATA[2] + DATA[1] + DATA[0]) > int(DATA_ULTIMA_ALTERACAO_VOB):
                        DATA_ULTIMA_ALTERACAO_VOB = DATA[2] + DATA[1] + DATA[0]

                    if LINHA_FONTES:
                        if int(DATA[2] + DATA[1] + DATA[0]) > int(DATA_ULTIMA_ALTERACAO_FONTES):
                            DATA_ULTIMA_ALTERACAO_FONTES = DATA[2] + DATA[1] + DATA[0]

                    if LINHA_BUILD:
                        if int(DATA[2] + DATA[1] + DATA[0]) > int(DATA_ULTIMA_ALTERACAO_BUILD):
                            DATA_ULTIMA_ALTERACAO_BUILD = DATA[2] + DATA[1] + DATA[0]

    entrada.close

def Grava_Dados_em_Arquivo():
    # Le os dados da tabela DADOS_VOB e grava em arquivo CSV
    try:
        saida = open(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\DADOS_VOB.csv',mode='w',encoding='UTF-8')

        # Escreve a linha do cabeçalho
        saida.write("VOB;SITE;SERVIDOR;DATA_CRIACAO;DB_SCHEMA;ACL_HABILITADO;FEATURE_LEVEL;USER_OWNER;COMUNIDADE;POSSUI_GRUPO_DOMAIN_USERS;MODELO_SEGURANCA;TAMANHO;PADRAO_PASTAS;POSSUI_PASTA_MODELAGEM;LOCK_PASTA_FONTES;DESC_PASTA_FONTES;LOCK_PASTA_BUILD;DESC_PASTA_BUILD;DATA_ULTIMA_ALTERACAO_VOB;DATA_ULTIMA_ALTERACAO_FONTES;DATA_ULTIMA_ALTERACAO_BUILD\n")

        cursor_VOBs = ConsultaSQLite("SELECT VOB,SITE,SERVIDOR,DATA_CRIACAO,DB_SCHEMA,ACL_HABILITADO,FEATURE_LEVEL,USER_OWNER,COMUNIDADE,POSSUI_GRUPO_DOMAIN_USERS,MODELO_SEGURANCA,TAMANHO,PADRAO_PASTAS,POSSUI_PASTA_MODELAGEM,LOCK_PASTA_FONTES,DESC_PASTA_FONTES,LOCK_PASTA_BUILD,DESC_PASTA_BUILD,DATA_ULTIMA_ALTERACAO_VOB,DATA_ULTIMA_ALTERACAO_FONTES,DATA_ULTIMA_ALTERACAO_BUILD FROM DADOS_VOB")

        VOBs = cursor_VOBs.fetchone()
        while VOBs:
            # Gravar a linha no arquivo de saida
            saida.write(f"{VOBs[0]};{VOBs[1]};{VOBs[2]};{VOBs[3]};{VOBs[4]};{VOBs[5]};{VOBs[6]};{VOBs[7]};{VOBs[8]};{VOBs[9]};{VOBs[10]};{VOBs[11]};{VOBs[12]};{VOBs[13]};{VOBs[14]};{VOBs[15]};{VOBs[16]};{VOBs[17]};{VOBs[18]};{VOBs[19]};{VOBs[20]}\n")
            
            VOBs = cursor_VOBs.fetchone()

    except Exception as erro:
        print(erro)


print('Le_Dados_DESC_VOB : ' + str(datetime.now().strftime("%H:%M:%S")))
Le_Dados_DESC_VOB(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\DESC.txt')

#print('Le_Tamanho_VOBs_SPRJ - SP : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Tamanho_VOBs_SPRJ(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\SP_update_space.txt')

#print('Le_Tamanho_VOBs_SPRJ - RJ : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Tamanho_VOBs_SPRJ(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\RJ_update_space.txt')

#print('Le_Tamanho_VOBs_SPRJ - BR : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Tamanho_VOBs_BR(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\BR_update_space.txt')

#print('Le_Tamanho_VOBs_BR - CEPEM : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Tamanho_VOBs_BR(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\CEPEM_update_space.txt')

#print('Le_DIR_Pasta_Principal : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_DIR_Pasta_Principal(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\SAIDA_DIR.txt')

#print('Le_Dados_DESC_Pasta - Fontes : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Dados_DESC_Pasta(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\DESC_PASTA_FONTES.txt')

#print('Le_Dados_DESC_Pasta - Build : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Dados_DESC_Pasta(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\DESC_PASTA_BUILD.txt')

#print('Le_Dados_LOCK_Pasta - Fontes : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Dados_LOCK_Pasta(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\LSLOCK_PASTA_FONTES.txt')

#print('Le_Dados_LOCK_Pasta - Build : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_Dados_LOCK_Pasta(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\LSLOCK_PASTA_BUILD.txt')

#print('Le_DIR : ' + str(datetime.now().strftime("%H:%M:%S")))
#Le_DIR(sys.path[0] + '\DESC_Verifica_Dados_Arquivos\DIR_VOBS.txt')

print('Grava_Dados_em_Arquivo : ' + str(datetime.now().strftime("%H:%M:%S")))
Grava_Dados_em_Arquivo()

print('Fim do Processo : ' + str(datetime.now().strftime("%H:%M:%S")))