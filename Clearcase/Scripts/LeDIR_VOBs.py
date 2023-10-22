import sys

# Abrindo o arquivo de entrada
arquivo_dir = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\saida_dir2.txt',mode='r',encoding='UTF-8')
arquivo_saida = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\Valida_pastas.csv',mode='w',encoding='UTF-8')

arquivo_saida.write(f"VOB;CERTIFICACAO;CERTIFICACAO_MASSA;CERTIFICACAO_MASSA_ALTA;CERTIFICACAO_MASSA_ALTA_BATCH;CERTIFICACAO_MASSA_ALTA_ONLINE;CERTIFICACAO_MASSA_BAIXA;CERTIFICACAO_MASSA_BAIXA_BATCH;CERTIFICACAO_MASSA_BAIXA_ONLINE;CERTIFICACAO_EXECUCAO;CERTIFICACAO_PLANEJAMENTO;HOMOLOGACAO;HOMOLOGACAO_MASSA;HOMOLOGACAO_MASSA_ALTA;HOMOLOGACAO_MASSA_ALTA_BATCH;HOMOLOGACAO_MASSA_ALTA_ONLINE;HOMOLOGACAO_MASSA_BAIXA;HOMOLOGACAO_MASSA_BAIXA_BATCH;HOMOLOGACAO_MASSA_BAIXA_ONLINE;HOMOLOGACAO_EXECUCAO;HOMOLOGACAO_PLANEJAMENTO;NAO_FUNCIONAL;NAO_FUNCIONAL_MASSA;NAO_FUNCIONAL_EXECUCAO;NAO_FUNCIONAL_PLANEJAMENTO;\n")
# Ler as linhas do arquivo e verificar se todas as pastas foram devidamente criadas

VOB = False
CERTIFICACAO = False
CERTIFICACAO_MASSA = False
CERTIFICACAO_MASSA_ALTA = False
CERTIFICACAO_MASSA_ALTA_BATCH = False
CERTIFICACAO_MASSA_ALTA_ONLINE = False
CERTIFICACAO_MASSA_BAIXA = False
CERTIFICACAO_MASSA_BAIXA_BATCH = False
CERTIFICACAO_MASSA_BAIXA_ONLINE = False
CERTIFICACAO_EXECUCAO = False
CERTIFICACAO_PLANEJAMENTO = False

HOMOLOGACAO = False
HOMOLOGACAO_MASSA = False
HOMOLOGACAO_MASSA_ALTA = False
HOMOLOGACAO_MASSA_ALTA_BATCH = False
HOMOLOGACAO_MASSA_ALTA_ONLINE = False
HOMOLOGACAO_MASSA_BAIXA = False
HOMOLOGACAO_MASSA_BAIXA_BATCH = False
HOMOLOGACAO_MASSA_BAIXA_ONLINE = False
HOMOLOGACAO_EXECUCAO = False
HOMOLOGACAO_PLANEJAMENTO = False

NAO_FUNCIONAL = False
NAO_FUNCIONAL_MASSA = False
NAO_FUNCIONAL_EXECUCAO = False
NAO_FUNCIONAL_PLANEJAMENTO = False

for linha in arquivo_dir:
    linha = linha.upper()
    if linha.find("DIRECTORY OF M:\F541364_VIEW_BR") > -1:
        if VOB == "":
            VOB = linha[33:linha.find('04-TESTES')-1]
        else:
            if VOB == linha[33:linha.find('04-TESTES')-1]:
                # Continua na mesma VOB

                # CERTIFICACAO
                if linha.find('04-TESTES\CERTIFICACAO') > -1:
                    CERTIFICACAO = True
                if linha.find('04-TESTES\CERTIFICACAO\MASSA') > -1:
                    CERTIFICACAO_MASSA = True
                if linha.find('04-TESTES\CERTIFICACAO\MASSA\ALTA') > -1:
                    CERTIFICACAO_MASSA_ALTA = True
                if linha.find('04-TESTES\CERTIFICACAO\MASSA\ALTA\BATCH') > -1:
                    CERTIFICACAO_MASSA_ALTA_BATCH = True
                if linha.find('04-TESTES\CERTIFICACAO\MASSA\ALTA\ONLINE') > -1:
                    CERTIFICACAO_MASSA_ALTA_ONLINE = True
                if linha.find('04-TESTES\CERTIFICACAO\MASSA\BAIXA') > -1:
                    CERTIFICACAO_MASSA_BAIXA = True
                if linha.find('04-TESTES\CERTIFICACAO\MASSA\BAIXA\BATCH') > -1:
                    CERTIFICACAO_MASSA_BAIXA_BATCH = True
                if linha.find('04-TESTES\CERTIFICACAO\MASSA\BAIXA\ONLINE') > -1:
                    CERTIFICACAO_MASSA_BAIXA_ONLINE = True
                if linha.find('04-TESTES\CERTIFICACAO\EXECUCAO') > -1:
                    CERTIFICACAO_EXECUCAO = True
                if linha.find('04-TESTES\CERTIFICACAO\PLANEJAMENTO') > -1:
                    CERTIFICACAO_PLANEJAMENTO = True

                # HOMOLOGACAO
                if linha.find('04-TESTES\HOMOLOGACAO') > -1:
                    HOMOLOGACAO = True
                if linha.find('04-TESTES\HOMOLOGACAO\MASSA') > -1:
                    HOMOLOGACAO_MASSA = True
                if linha.find('04-TESTES\HOMOLOGACAO\MASSA\ALTA') > -1:
                    HOMOLOGACAO_MASSA_ALTA = True
                if linha.find('04-TESTES\HOMOLOGACAO\MASSA\ALTA\BATCH') > -1:
                    HOMOLOGACAO_MASSA_ALTA_BATCH = True
                if linha.find('04-TESTES\HOMOLOGACAO\MASSA\ALTA\ONLINE') > -1:
                    HOMOLOGACAO_MASSA_ALTA_ONLINE = True
                if linha.find('04-TESTES\HOMOLOGACAO\MASSA\BAIXA') > -1:
                    HOMOLOGACAO_MASSA_BAIXA = True
                if linha.find('04-TESTES\HOMOLOGACAO\MASSA\BAIXA\BATCH') > -1:
                    HOMOLOGACAO_MASSA_BAIXA_BATCH = True
                if linha.find('04-TESTES\HOMOLOGACAO\MASSA\BAIXA\ONLINE') > -1:
                    HOMOLOGACAO_MASSA_BAIXA_ONLINE = True
                if linha.find('04-TESTES\HOMOLOGACAO\EXECUCAO') > -1:
                    HOMOLOGACAO_EXECUCAO = True
                if linha.find('04-TESTES\HOMOLOGACAO\PLANEJAMENTO') > -1:
                    HOMOLOGACAO_PLANEJAMENTO = True

                # NAO_FUNCIONAL
                if linha.find('04-TESTES\\NAO_FUNCIONAL') > -1:
                    NAO_FUNCIONAL = True
                if linha.find('04-TESTES\\NAO_FUNCIONAL\\MASSA') > -1:
                    NAO_FUNCIONAL_MASSA = True
                if linha.find('04-TESTES\\NAO_FUNCIONAL\\EXECUCAO') > -1:
                    NAO_FUNCIONAL_EXECUCAO = True
                if linha.find('04-TESTES\\NAO_FUNCIONAL\\PLANEJAMENTO') > -1:
                    NAO_FUNCIONAL_PLANEJAMENTO = True

            else:
                # Mudou a VOB -> Salvar as informações encontradas
                # Só gravar no arquivo de saida se alguma coluna for falsa
                if CERTIFICACAO == False or CERTIFICACAO_MASSA == False or CERTIFICACAO_MASSA_ALTA == False or CERTIFICACAO_MASSA_ALTA_BATCH == False or CERTIFICACAO_MASSA_ALTA_ONLINE == False or CERTIFICACAO_MASSA_BAIXA == False or CERTIFICACAO_MASSA_BAIXA_BATCH == False or CERTIFICACAO_MASSA_BAIXA_ONLINE == False or CERTIFICACAO_EXECUCAO == False or CERTIFICACAO_PLANEJAMENTO == False or HOMOLOGACAO == False or HOMOLOGACAO_MASSA == False or HOMOLOGACAO_MASSA_ALTA == False or HOMOLOGACAO_MASSA_ALTA_BATCH == False or HOMOLOGACAO_MASSA_ALTA_ONLINE == False or HOMOLOGACAO_MASSA_BAIXA == False or HOMOLOGACAO_MASSA_BAIXA_BATCH == False or HOMOLOGACAO_MASSA_BAIXA_ONLINE == False or HOMOLOGACAO_EXECUCAO == False or HOMOLOGACAO_PLANEJAMENTO == False or NAO_FUNCIONAL == False or NAO_FUNCIONAL_MASSA == False or NAO_FUNCIONAL_EXECUCAO == False or NAO_FUNCIONAL_PLANEJAMENTO == False:
                    arquivo_saida.write(f"{VOB};{CERTIFICACAO};{CERTIFICACAO_MASSA};{CERTIFICACAO_MASSA_ALTA};{CERTIFICACAO_MASSA_ALTA_BATCH};{CERTIFICACAO_MASSA_ALTA_ONLINE};{CERTIFICACAO_MASSA_BAIXA};{CERTIFICACAO_MASSA_BAIXA_BATCH};{CERTIFICACAO_MASSA_BAIXA_ONLINE};{CERTIFICACAO_EXECUCAO};{CERTIFICACAO_PLANEJAMENTO};{HOMOLOGACAO};{HOMOLOGACAO_MASSA};{HOMOLOGACAO_MASSA_ALTA};{HOMOLOGACAO_MASSA_ALTA_BATCH};{HOMOLOGACAO_MASSA_ALTA_ONLINE};{HOMOLOGACAO_MASSA_BAIXA};{HOMOLOGACAO_MASSA_BAIXA_BATCH};{HOMOLOGACAO_MASSA_BAIXA_ONLINE};{HOMOLOGACAO_EXECUCAO};{HOMOLOGACAO_PLANEJAMENTO};{NAO_FUNCIONAL};{NAO_FUNCIONAL_MASSA};{NAO_FUNCIONAL_EXECUCAO};{NAO_FUNCIONAL_PLANEJAMENTO};\n")

                CERTIFICACAO = False
                CERTIFICACAO_MASSA = False
                CERTIFICACAO_MASSA_ALTA = False
                CERTIFICACAO_MASSA_ALTA_BATCH = False
                CERTIFICACAO_MASSA_ALTA_ONLINE = False
                CERTIFICACAO_MASSA_BAIXA = False
                CERTIFICACAO_MASSA_BAIXA_BATCH = False
                CERTIFICACAO_MASSA_BAIXA_ONLINE = False
                CERTIFICACAO_EXECUCAO = False
                CERTIFICACAO_PLANEJAMENTO = False

                HOMOLOGACAO = False
                HOMOLOGACAO_MASSA = False
                HOMOLOGACAO_MASSA_ALTA = False
                HOMOLOGACAO_MASSA_ALTA_BATCH = False
                HOMOLOGACAO_MASSA_ALTA_ONLINE = False
                HOMOLOGACAO_MASSA_BAIXA = False
                HOMOLOGACAO_MASSA_BAIXA_BATCH = False
                HOMOLOGACAO_MASSA_BAIXA_ONLINE = False
                HOMOLOGACAO_EXECUCAO = False
                HOMOLOGACAO_PLANEJAMENTO = False

                NAO_FUNCIONAL = False
                NAO_FUNCIONAL_MASSA = False
                NAO_FUNCIONAL_EXECUCAO = False
                NAO_FUNCIONAL_PLANEJAMENTO = False

                VOB = linha[33:linha.find('04-TESTES')-1]

   
arquivo_dir.close()
arquivo_saida.close()