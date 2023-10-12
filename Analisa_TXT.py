import os
import sys

#Importando os arquivos das funções comuns
sys.path.append('c:\\Projetos\\CAIXA\\Funcoes')
from MessageBox import MessageBox


class Analisa_TXT():

    def Le_DESC(arq_entrada, arq_saida):
        # Separando os tipos de grupos
        grupos_padrao = ['CORPCAIXA\g7259csp', 'CORPCAIXA\g cs7266 cc_regiao_qualidade_sp', 'CORPCAIXA\g cs7266 cc_metricas',
                         'CORPCAIXA\g cs7266 cc_regiao_ti_metricas', 'CORPCAIXA\g cs7266 cc_caixa_escrita',
                         'CORPCAIXA\g cs7266 cc_todos_escrita']

        grupos_caixa = ['CORPCAIXA\g cs7266 cc_regiao_back_office', 'CORPCAIXA\g cs7266 cc_regiao_infraestrutura',
                        'CORPCAIXA\g cs7266 cc_regiao_captar', 'CORPCAIXA\g cs7266 cc_regiao_servicos_bancarios',
                        'CORPCAIXA\g cs7266 cc_regiao_canais', 'CORPCAIXA\G CS7266 CC_REGIAO_FINANCEIRO',
                        'CORPCAIXA\G CS7266 CC_REGIAO_MOBILIDADE', 'CORPCAIXA\g cs7266 cc_regiao_cartoes',
                        'CORPCAIXA\G DF5222 CC_ARRECADACAO','CORPCAIXA\G DF5222 CC_CAMBIO','CORPCAIXA\G DF5222 CC_CANAIS_CLIENTES','CORPCAIXA\G DF5222 CC_CANAIS_INTERNO','CORPCAIXA\G DF5222 CC_CONTRATACOES','CORPCAIXA\G DF5222 CC_CONTROLADORIA','CORPCAIXA\G DF5222 CC_CREDITO','CORPCAIXA\G DF5222 CC_CRM_CADASTRO','CORPCAIXA\G DF5222 CC_DADOS','CORPCAIXA\G DF5222 CC_DEPOSITO','CORPCAIXA\G DF5222 CC_ESTEIRAS','CORPCAIXA\G DF5222 CC_ESTRUTURANTES_TI','CORPCAIXA\G DF5222 CC_FINANCEIRO','CORPCAIXA\G DF5222 CC_FOMENTO_DJ','CORPCAIXA\G DF5222 CC_FUNDOS_GOVERNO','CORPCAIXA\G DF5222 CC_HABITACAO','CORPCAIXA\G DF5222 CC_INSTITUCIONAL','CORPCAIXA\G DF5222 CC_LOTERIAS','CORPCAIXA\G DF5222 CC_MEIOS_PAGAMENTO','CORPCAIXA\G DF5222 CC_OPEN_BANKING','CORPCAIXA\G DF5222 CC_OPERACOES_BANCARIAS','CORPCAIXA\G DF5222 CC_PESSOAS','CORPCAIXA\G DF5222 CC_PROGRAMAS_SOCIAIS','CORPCAIXA\G DF5222 CC_RISCO','CORPCAIXA\G DF5222 CC_SEGURANCA']

        grupos_fabrica = ['CORPCAIXA\G CS7266 CC_REGIAO_RESOURCE', 'CORPCAIXA\G CS7266 CC_REGIAO_FIRST_DECISION',
                          'CORPCAIXA\G CS7266 CC_REGIAO_SPREAD', 'CORPCAIXA\g cs7266 cc_regiao_stefanini',
                          'CORPCAIXA\g cs7266 cc_regiao_msa_tty', 'CORPCAIXA\g cs7266 cc_regiao_global_web',
                          'CORPCAIXA\g cs7266 cc_regiao_foton', 'CORPCAIXA\G CS7266 CC_REGIAO_CAST',
                          'CORPCAIXA\G CS7266 CC_REGIAO_INDRA', 'CORPCAIXA\g cs7266 cc_regiao_cpm',
                          'CORPCAIXA\G CS7266 CC_REGIAO_TREE', 'CORPCAIXA\G CS7266 CC_REGIAO_TTY_SP',
                          'CORPCAIXA\G CS7266 CC_REGIAO_MAGNA', 'CORPCAIXA\g cs7266 cc_regiao_dba',
                          'CORPCAIXA\G CS7266 CC_REGIAO_MAPS',
                          'CORPCAIXA\G DF5222 CC_ATOS','CORPCAIXA\G DF5222 CC_B3','CORPCAIXA\G DF5222 CC_BRQ','CORPCAIXA\G DF5222 CC_BRY','CORPCAIXA\G DF5222 CC_BRQEWAVE','CORPCAIXA\G DF5222 CC_CAST','CORPCAIXA\G DF5222 CC_CMA','CORPCAIXA\G DF5222 CC_CPQD','CORPCAIXA\G DF5222 CC_DATAINFO','CORPCAIXA\G DF5222 CC_DBA','CORPCAIXA\G DF5222 CC_ESEC','CORPCAIXA\G DF5222 CC_FIRST','CORPCAIXA\G DF5222 CC_FOTON','CORPCAIXA\G DF5222 CC_GLOBALWEB','CORPCAIXA\G DF5222 CC_INDRA','CORPCAIXA\G DF5222 CC_HITSS','CORPCAIXA\G DF5222 CC_MAGNA','CORPCAIXA\G DF5222 CC_MAPS','CORPCAIXA\G DF5222 CC_MEMORA','CORPCAIXA\G DF5222 CC_MURAH','CORPCAIXA\G DF5222 CC_PEOPLEWARE','CORPCAIXA\G DF5222 CC_QUINTES','CORPCAIXA\G DF5222 CC_RESOURCE','CORPCAIXA\G DF5222 CC_RJE','CORPCAIXA\G DF5222 CC_SENIOR','CORPCAIXA\G DF5222 CC_SONDAS','CORPCAIXA\G DF5222 CC_SPREAD','CORPCAIXA\G DF5222 CC_STEFANINI','CORPCAIXA\G DF5222 CC_TELEDATA','CORPCAIXA\G DF5222 CC_TIVIT','CORPCAIXA\G DF5222 CC_TREE','CORPCAIXA\G DF5222 CC_TTY','CORPCAIXA\G DF5222 CC_UNISYS','CORPCAIXA\G DF5222 CC_VERT_SAS']

        outros_grupos = ['CORPCAIXA\g cs7266 pedep sp', 'CORPCAIXA\G DF7390 PRESTAR_SERVICO2',
                         'CORPCAIXA\G DF7390 FINANCIAMENTO_IMOBILIARIO', 'CORPCAIXA\G DF7390 NOVAS_TECNOLOGIAS',
                         'CORPCAIXA\g cs7266 sisag', 'CORPCAIXA\g cs7266 sisag_restrito', 'CORPCAIXA\g cr7265 suporte_caixa',
                         'CORPCAIXA\g cr7265 suporte_caixa', 'CORPCAIXA\g cs7266 sisag_restrito',
                         'CORPCAIXA\G DF7390 GESTAO_SUPORTE', 'CORPCAIXA\G CS7266 SISAG_RESTRITO_DIEBOLD',
                         'CORPCAIXA\G DF7390 CPM_BRAXIS']

        # Abrindo os arquivos de entrada e saida
        arquivo_entrada = open(arq_entrada, mode='r', encoding='UTF-8')
        arquivo_saida = open(arq_saida, mode='w', encoding='UTF-8')

        saida = ''
        GRUPO_CAIXA = ''
        GRUPO_FABRICA = ''
        OUTROS_GRUPOS = ''

        # Escrevendo as colunas do cabeçalho do arquivo de saida
        arquivo_saida.write('VOB;Grupo CAIXA;Grupo Fabrica;Outros Grupos;Outros Grupos;Outros Grupos')
        arquivo_saida.write('\n')

        #tamanho_arquivo_entrada = os.path.getsize(arq_entrada)
        #ercentual_progresso = 0

        for linha in arquivo_entrada:
            if linha.find('versioned') != -1:
                # Encontrou a primeira linha da VOB
                VOB = str(linha[24:-2])
            elif linha.find('FeatureLevel') != -1:
                # Encontrou a última linha da VOB, então precisa organizar a gravar a saída
                saida = VOB + ';' + GRUPO_CAIXA + ';' + GRUPO_FABRICA + ';' + OUTROS_GRUPOS
                arquivo_saida.write(saida)
                arquivo_saida.write('\n')
                GRUPO_CAIXA = ''
                GRUPO_FABRICA = ''
                OUTROS_GRUPOS = ''
            else:
                # Linhas do conteúdo da VOB
                if (linha.find('group') != -1) and (linha.find('Additional') != 2):
                    GRUPO = str(linha[10:-1])
                    if (GRUPO in grupos_caixa):
                        GRUPO_CAIXA = GRUPO
                    elif (GRUPO in grupos_fabrica):
                        GRUPO_FABRICA = GRUPO
                    elif (GRUPO in outros_grupos):
                        OUTROS_GRUPOS = OUTROS_GRUPOS + ';' + GRUPO

        # Fecha os arquivos
        arquivo_entrada.close()
        arquivo_saida.close()


    def Le_NETSHARE(arq_entrada, arq_saida):
        # Separando os tipos de grupos
        grupos_padrao = ['CORPCAIXA\g7259csp', 'CORPCAIXA\g cs7266 cc_regiao_qualidade_sp', 'CORPCAIXA\g cs7266 cc_metricas',
                         'CORPCAIXA\g cs7266 cc_regiao_ti_metricas', 'CORPCAIXA\g cs7266 cc_caixa_escrita',
                         'CORPCAIXA\g cs7266 cc_todos_escrita']

        grupos_caixa = ['CORPCAIXA\g cs7266 cc_regiao_back_office', 'CORPCAIXA\g cs7266 cc_regiao_infraestrutura',
                        'CORPCAIXA\g cs7266 cc_regiao_captar', 'CORPCAIXA\g cs7266 cc_regiao_servicos_bancarios',
                        'CORPCAIXA\g cs7266 cc_regiao_canais', 'CORPCAIXA\G CS7266 CC_REGIAO_FINANCEIRO',
                        'CORPCAIXA\G CS7266 CC_REGIAO_MOBILIDADE', 'CORPCAIXA\g cs7266 cc_regiao_cartoes',
                        'CORPCAIXA\G DF5222 CC_ARRECADACAO','CORPCAIXA\G DF5222 CC_CAMBIO','CORPCAIXA\G DF5222 CC_CANAIS_CLIENTES','CORPCAIXA\G DF5222 CC_CANAIS_INTERNO','CORPCAIXA\G DF5222 CC_CONTRATACOES','CORPCAIXA\G DF5222 CC_CONTROLADORIA','CORPCAIXA\G DF5222 CC_CREDITO','CORPCAIXA\G DF5222 CC_CRM_CADASTRO','CORPCAIXA\G DF5222 CC_DADOS','CORPCAIXA\G DF5222 CC_DEPOSITO','CORPCAIXA\G DF5222 CC_ESTEIRAS','CORPCAIXA\G DF5222 CC_ESTRUTURANTES_TI','CORPCAIXA\G DF5222 CC_FINANCEIRO','CORPCAIXA\G DF5222 CC_FOMENTO_DJ','CORPCAIXA\G DF5222 CC_FUNDOS_GOVERNO','CORPCAIXA\G DF5222 CC_HABITACAO','CORPCAIXA\G DF5222 CC_INSTITUCIONAL','CORPCAIXA\G DF5222 CC_LOTERIAS','CORPCAIXA\G DF5222 CC_MEIOS_PAGAMENTO','CORPCAIXA\G DF5222 CC_OPEN_BANKING','CORPCAIXA\G DF5222 CC_OPERACOES_BANCARIAS','CORPCAIXA\G DF5222 CC_PESSOAS','CORPCAIXA\G DF5222 CC_PROGRAMAS_SOCIAIS','CORPCAIXA\G DF5222 CC_RISCO','CORPCAIXA\G DF5222 CC_SEGURANCA']

        grupos_fabrica = ['CORPCAIXA\G CS7266 CC_REGIAO_RESOURCE', 'CORPCAIXA\G CS7266 CC_REGIAO_FIRST_DECISION',
                          'CORPCAIXA\G CS7266 CC_REGIAO_SPREAD', 'CORPCAIXA\g cs7266 cc_regiao_stefanini',
                          'CORPCAIXA\g cs7266 cc_regiao_msa_tty', 'CORPCAIXA\g cs7266 cc_regiao_global_web',
                          'CORPCAIXA\g cs7266 cc_regiao_foton', 'CORPCAIXA\G CS7266 CC_REGIAO_CAST',
                          'CORPCAIXA\G CS7266 CC_REGIAO_INDRA', 'CORPCAIXA\g cs7266 cc_regiao_cpm',
                          'CORPCAIXA\G CS7266 CC_REGIAO_TREE', 'CORPCAIXA\G CS7266 CC_REGIAO_TTY_SP',
                          'CORPCAIXA\G CS7266 CC_REGIAO_MAGNA', 'CORPCAIXA\g cs7266 cc_regiao_dba',
                          'CORPCAIXA\G CS7266 CC_REGIAO_MAPS',
                          'CORPCAIXA\G DF5222 CC_ATOS','CORPCAIXA\G DF5222 CC_B3','CORPCAIXA\G DF5222 CC_BRQ','CORPCAIXA\G DF5222 CC_BRY','CORPCAIXA\G DF5222 CC_BRQEWAVE','CORPCAIXA\G DF5222 CC_CAST','CORPCAIXA\G DF5222 CC_CMA','CORPCAIXA\G DF5222 CC_CPQD','CORPCAIXA\G DF5222 CC_DATAINFO','CORPCAIXA\G DF5222 CC_DBA','CORPCAIXA\G DF5222 CC_ESEC','CORPCAIXA\G DF5222 CC_FIRST','CORPCAIXA\G DF5222 CC_FOTON','CORPCAIXA\G DF5222 CC_GLOBALWEB','CORPCAIXA\G DF5222 CC_INDRA','CORPCAIXA\G DF5222 CC_HITSS','CORPCAIXA\G DF5222 CC_MAGNA','CORPCAIXA\G DF5222 CC_MAPS','CORPCAIXA\G DF5222 CC_MEMORA','CORPCAIXA\G DF5222 CC_MURAH','CORPCAIXA\G DF5222 CC_PEOPLEWARE','CORPCAIXA\G DF5222 CC_QUINTES','CORPCAIXA\G DF5222 CC_RESOURCE','CORPCAIXA\G DF5222 CC_RJE','CORPCAIXA\G DF5222 CC_SENIOR','CORPCAIXA\G DF5222 CC_SONDAS','CORPCAIXA\G DF5222 CC_SPREAD','CORPCAIXA\G DF5222 CC_STEFANINI','CORPCAIXA\G DF5222 CC_TELEDATA','CORPCAIXA\G DF5222 CC_TIVIT','CORPCAIXA\G DF5222 CC_TREE','CORPCAIXA\G DF5222 CC_TTY','CORPCAIXA\G DF5222 CC_UNISYS','CORPCAIXA\G DF5222 CC_VERT_SAS',
                          'CORPCAIXA\G DF7390 ARRECADACAO-dev-foton','CORPCAIXA\G DF7390 ARRECADACAO-dev-globalweb','CORPCAIXA\G DF7390 ARRECADACAO-dev-quintes','CORPCAIXA\G DF7390 ARRECADACAO-dev-spread','CORPCAIXA\G DF7390 ARRECADACAO-dev-stefanini','CORPCAIXA\G DF7390 CANAIS_CLIENTES-dev-first','CORPCAIXA\G DF7390 CANAIS_CLIENTES-dev-foton','CORPCAIXA\G DF7390 CANAIS_CLIENTES-dev-spread','CORPCAIXA\G DF7390 CANAIS_CLIENTES-dev-stefanini','CORPCAIXA\G DF7390 DADOS-dev-first','CORPCAIXA\G RJ7265 CRM_CADASTRO-dev-cast','CORPCAIXA\G RJ7265 CRM_CADASTRO-dev-stefanini','CORPCAIXA\G SP7266 ARRECADACAO-dev-foton','CORPCAIXA\G SP7266 ARRECADACAO-dev-globalweb','CORPCAIXA\G SP7266 ARRECADACAO-dev-quintes','CORPCAIXA\G SP7266 ARRECADACAO-dev-spread','CORPCAIXA\G SP7266 ARRECADACAO-dev-stefanini','CORPCAIXA\G SP7266 CAMBIO-dev-cast','CORPCAIXA\G SP7266 CAMBIO-dev-first','CORPCAIXA\G SP7266 CAMBIO-dev-foton','CORPCAIXA\G SP7266 CAMBIO-dev-maps','CORPCAIXA\G SP7266 CAMBIO-dev-resource','CORPCAIXA\G SP7266 CAMBIO-dev-tree','CORPCAIXA\G SP7266 CAMBIO-dev-tty','CORPCAIXA\G SP7266 CANAIS_CLIENTES-dev-first','CORPCAIXA\G SP7266 CANAIS_CLIENTES-dev-foton','CORPCAIXA\G SP7266 CANAIS_CLIENTES-dev-spread','CORPCAIXA\G SP7266 CANAIS_CLIENTES-dev-stefanini','CORPCAIXA\G SP7266 CANAIS_INTERNO-dev-cast','CORPCAIXA\G SP7266 CANAIS_INTERNO-dev-foton','CORPCAIXA\G SP7266 CANAIS_INTERNO-dev-indra','CORPCAIXA\G SP7266 CANAIS_INTERNO-dev-spread']

        outros_grupos = ['CORPCAIXA\g cs7266 pedep sp', 'CORPCAIXA\G DF7390 PRESTAR_SERVICO2',
                         'CORPCAIXA\G DF7390 FINANCIAMENTO_IMOBILIARIO', 'CORPCAIXA\G DF7390 NOVAS_TECNOLOGIAS',
                         'CORPCAIXA\g cs7266 sisag', 'CORPCAIXA\g cs7266 sisag_restrito', 'CORPCAIXA\g cr7265 suporte_caixa',
                         'CORPCAIXA\g cr7265 suporte_caixa', 'CORPCAIXA\g cs7266 sisag_restrito',
                         'CORPCAIXA\G DF7390 GESTAO_SUPORTE', 'CORPCAIXA\G CS7266 SISAG_RESTRITO_DIEBOLD',
                         'CORPCAIXA\G DF7390 CPM_BRAXIS']

        # Abrindo os arquivos de entrada e saida
        arquivo_entrada = open(arq_entrada)
        arquivo_saida = open(arq_saida, "w")

        saida = ''
        GRUPO_CAIXA = ''
        GRUPO_FABRICA = ''
        OUTROS_GRUPOS = ''

        # Escrevendo as colunas do cabeçalho do arquivo de saida
        arquivo_saida.write('VOB;Grupo CAIXA;Grupo Fabrica;Outros Grupos;Outros Grupos;Outros Grupos')
        arquivo_saida.write('\n')

        GRUPO=''
        GRUPO_COMUNIDADE=''
        OUTROS_GRUPOS=''
        for linha in arquivo_entrada:
            if linha.find('Share name') != -1:
                # Encontrou a primeira linha da VOB
                VOB = str(linha[18:-2])
            elif linha.find('The command completed successfully.') != -1:
                # Encontrou a última linha da VOB, então precisa organizar a gravar a saída
                saida = VOB + ';' + GRUPO_COMUNIDADE + ';' + GRUPO_FABRICA + ';' + OUTROS_GRUPOS
                arquivo_saida.write(saida)
                arquivo_saida.write('\n')
                GRUPO_COMUNIDADE = ''
                GRUPO_FABRICA = ''
                OUTROS_GRUPOS = ''
            else:
                GRUPO = str(linha[10:-9])
                GRUPO = GRUPO.lstrip().rstrip()
                if (GRUPO in grupos_caixa):
                    GRUPO_COMUNIDADE += GRUPO + ';'
                elif (GRUPO in grupos_fabrica):
                    GRUPO_FABRICA += GRUPO + ';'
                elif (GRUPO in outros_grupos):
                    OUTROS_GRUPOS = OUTROS_GRUPOS + ';' + GRUPO


        # Fecha os arquivos
        arquivo_entrada.close()
        arquivo_saida.close()

        MessageBox.Mensagem(f"Arquivo '{arq_saida}' gerado com sucesso!!!!","Informação",QMessageBox.Information,QMessageBox.Ok)


    def Extrai_Areas_Report(entrada):
        # Abrindo o arquivo de entrada
        arquivo_entrada = open(entrada,encoding='UTF-8')

        AREAS_RTC = []
        AREAS_RDNG = []
        AREAS_RQM = []
        for linha in arquivo_entrada:
            if linha.find('Projeto CCM') != -1:
                # Encontrou uma área de projeto do RTC
                AREAS_RTC.append(linha[1:-15])
                
            elif linha.find('Projeto RM') != -1:
                # Encontrou uma área de projeto do RDNG
                AREAS_RDNG.append(linha[1:-14])

            elif linha.find('Projeto QM') != -1:
                # Encontrou uma área de projeto do RQM
                AREAS_RQM.append(linha[1:-14])

        #Gravar as áreas encontradas no arquivo de saida
        arquivo_saida_RTC = open(entrada[2:-4] + "_saida_RTC.csv", "w")
        arquivo_saida_RDNG = open(entrada[2:-4] + "_saida_RDNG.csv", "w")
        arquivo_saida_RQM = open(entrada[2:-4] + "_saida_RQM.csv", "w")

        # Escrevendo as colunas do cabeçalho nos arquivos de saida
        arquivo_saida_RTC.write('Area_RTC')
        arquivo_saida_RTC.write('\n')
        arquivo_saida_RDNG.write('Area_RDNG')
        arquivo_saida_RDNG.write('\n')
        arquivo_saida_RQM.write('Area_RQM')
        arquivo_saida_RQM.write('\n')

        for AREA in AREAS_RTC:
            arquivo_saida_RTC.write(AREA)
            arquivo_saida_RTC.write('\n')

        for AREA in AREAS_RDNG:
            arquivo_saida_RDNG.write(AREA)
            arquivo_saida_RDNG.write('\n')

        for AREA in AREAS_RQM:
            arquivo_saida_RQM.write(AREA)
            arquivo_saida_RQM.write('\n')

        # Fecha os arquivos
        arquivo_entrada.close()
        arquivo_saida_RTC.close()
        arquivo_saida_RDNG.close()
        arquivo_saida_RQM.close()


    def Relaciona_Areas_e_Master(entrada):
        # Abrindo o arquivo de entrada
        arquivo_entrada = open(entrada,encoding='UTF-8')

        for linha in arquivo_entrada:
            if linha.find('</com.ibm.team.process.ProjectArea>') != -1:
                print(area + ' - ' + master)

            if linha.find('<com.ibm.team.process.ProjectArea>') != -1:
                tipo = 'area'

            if linha.find('internalProcessProvider') != -1:
                tipo = 'master'

            if linha.find('<name>') != -1:
                if tipo == 'area':
                    area = ''
                elif tipo == 'master':
                    master = ''


    def Le_dir_gera_comando(entrada):
        # Abrindo o arquivo de entrada
        arquivo_entrada = open(entrada,"r",encoding='UTF-8')
        arquivo_saida = open(entrada[2:-4] + "_saida.txt","w",encoding='UTF-8')

        DIRETORIO = ''
        ARQUIVO = ''

        for linha in arquivo_entrada:
            #Verifica se a linha contem o diretório
            if linha.find('Directory') != -1:
                DIRETORIO = linha[14:-1]

            #Verifica se a linha contem o nome do arquivo
            if linha.find('.doc') != -1:
                ARQUIVO = linha[linha.find('SIFES'):-1]

            #Verifica se finalizou as linhas do arquivo pesquisado
            if linha.find('Total Files Listed') != -1:
                if (len(DIRETORIO) == 0 or len(ARQUIVO) == 0):
                    arquivo_saida.write("Erro!! DIR:" + DIRETORIO + " - ARQUIVO: " + ARQUIVO)
                    DIRETORIO = ""
                    ARQUIVO = ""
                else:
                    comando = "cleartool protect -chmod 755 '" + DIRETORIO + "\\" + ARQUIVO + "'"
                    arquivo_saida.write(comando)
                    arquivo_saida.write('\n')

                    DIRETORIO = ""
                    ARQUIVO = ""

        arquivo_entrada.close
        arquivo_saida.close

        return(entrada[2:-4] + "_saida.txt")
    
    
    def Le_DESC_Flevel_schemadb(arq_entrada):
        # Abrindo os arquivos de entrada e saida
        arquivo_entrada = open(arq_entrada,mode='r',encoding='UTF-8')
        arquivo_saida = open(arq_entrada[:-4] + '_saida.csv',mode='w',encoding='UTF-8')

        saida = ''

        for linha in arquivo_entrada:
            if linha.find('versioned') != -1:
                # Encontrou a primeira linha da VOB
                VOB = str(linha[24:-2])
            elif linha.find('FeatureLevel') != -1:
                # Encontrou a última linha da VOB, então precisa organizar a gravar a saída
                FLevel = linha[19:20]

                if ( (FLevel != '9') and (DBSchema != '80') ):
                    arquivo_saida.write('VOB: ' + VOB + ' - Feature Level: ' + FLevel + ' - DB Schema : ' + DBSchema + '\n')

                VOB = ''
                FLevel=''
                DBSchema = ''
            elif linha.find('schema') != -1:
                # Encontrou O Database Schema
                DBSchema = linha[27:29]

        # Fecha os arquivos
        arquivo_entrada.close()
        arquivo_saida.close()


    def Le_SaidaDir_Caso_Desenv(arquivo_entrada):
        try:
            # Abrindo os arquivos de entrada e saida
            dir_txt = open(arquivo_entrada,mode='r',encoding='UTF-8')
            arquivo_saida = open(arquivo_entrada[:-4] + '_saida.csv',mode='w',encoding='UTF-8')
        except:
            return 'Erro ao abrir os arquivos'

        try:
            saida = ''
            VOB=''
            for linha in dir_txt:
                if linha.find("Directory of M:\\f541364_view5") != -1:
                    # Encontrou a primeira linha da VOB, se não for a primeira, gravar os dados
                    if ( VOB != ''):
                        arquivo_saida.write(f"{VOB} ; {Local} ; {Data_Alteracao}\n")

                    # Ler a proxima VOB
                    VOB = linha.split("\\")[2]

                elif linha.find('Nao encontrou o Caso de Desenvolvimento') != -1:
                    # VOB não tem o arquivo -> Gravar os dados da VOB anterior
                    if ( VOB != ''):
                        arquivo_saida.write(f"{VOB} ; {Local} ; {Data_Alteracao}\n")

                    VOB = linha[:int(linha.find('Nao encontrou o Caso de Desenvolvimento')-3)]
                    Local = "Nao localizado na pasta '06 - Ambiente'"
                    Data_Alteracao = "Nao se aplica"
                    arquivo_saida.write(f"{VOB} ; {Local} ; {Data_Alteracao}\n")

                    VOB = ''
                    Local = ''
                    Data_Alteracao = ''
                elif ( (linha.find('Caso') != -1) or (linha.find('Desenv') != -1) or (linha.find('.doc') != -1) ):
                    Data_Alteracao = linha[:17]
                    Local = linha[36:-1]
        except:
            return 'Erro ao gerar a analise do TXT'

        else:
            return 'Arquivo analisado com sucesso'
        finally:
            # Independente de ter ocorrido algum erro, o programa deve fechar os arquivos
            dir_txt.close
            arquivo_saida.close


    def Gera_Arquivo_Tamanho_VOBs(arquivo_entrada):

        # Abrindo os arquivos de entrada e saida
        entrada = open(arquivo_entrada,mode='r',encoding='UTF-8')
        saida = open(arquivo_entrada[:-4] + '_saida.csv',mode='w',encoding='UTF-8')
        saida.write('VOB;TAMANHO_VOB\n')

        VOB=''
        for linha in entrada:
            if linha.find('Total usage') != -1:
                # Encontrou a linha que possui a informação do tamanho da VOB
                posicao1 = linha.find('vob') + 6
                posicao2 = linha.find('is') - 2
                posicao3 = linha.find('is') + 3
                posicao4 = linha.find('Mb') - 1
                VOB = linha[posicao1:posicao2]
                TAMANHO_VOB = linha[posicao3:posicao4]
                saida.write(VOB + ';' + TAMANHO_VOB + "\n")

        entrada.close
        saida.close
        return arquivo_entrada[:-4] + '_saida.csv'


    def Gera_Arquivo_VOBs_Servidor(arquivo_entrada):

        # Abrindo os arquivos de entrada e saida
        entrada = open(arquivo_entrada,mode='r',encoding='UTF-8')
        saida = open(arquivo_entrada[:-4] + '_saida.csv',mode='w',encoding='UTF-8')
        saida.write('VOB;SERVIDOR\n')

        VOB=''
        for linha in entrada:
            VOB = linha[3:linha.find('\\\\')].rstrip()
            linha = linha.upper()

            #INICIO_SERVIDOR = linha.find("\\\\") +2
            #FIM_SERVIDOR = linha.find(VOB + "$") -1
            #NOME_SERVIDOR = linha[INICIO_SERVIDOR:FIM_SERVIDOR]
            
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
            else:
                SERVIDOR = "Não encontrado"

            saida.write(VOB + ";" + SERVIDOR + "\n")

        entrada.close()
        saida.close()
        return arquivo_entrada[:-4] + '_saida.csv'