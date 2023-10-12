import sys

# Abrindo o arquivo de entrada
arquivo_dir = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\saida_desc_pastas.txt',mode='r',encoding='UTF-8')
arquivo_saida = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\Valida_protecao_pastas.csv',mode='w',encoding='UTF-8')

arquivo_saida.write(f"VOB;CERTIFICACAO;CERTIFICACAO_MASSA;CERTIFICACAO_MASSA_ALTA;CERTIFICACAO_MASSA_ALTA_BATCH;CERTIFICACAO_MASSA_ALTA_ONLINE;CERTIFICACAO_MASSA_BAIXA;CERTIFICACAO_MASSA_BAIXA_BATCH;CERTIFICACAO_MASSA_BAIXA_ONLINE;CERTIFICACAO_EXECUCAO;CERTIFICACAO_PLANEJAMENTO;HOMOLOGACAO;HOMOLOGACAO_MASSA;HOMOLOGACAO_MASSA_ALTA;HOMOLOGACAO_MASSA_ALTA_BATCH;HOMOLOGACAO_MASSA_ALTA_ONLINE;HOMOLOGACAO_MASSA_BAIXA;HOMOLOGACAO_MASSA_BAIXA_BATCH;HOMOLOGACAO_MASSA_BAIXA_ONLINE;HOMOLOGACAO_EXECUCAO;HOMOLOGACAO_PLANEJAMENTO;NAO_FUNCIONAL;NAO_FUNCIONAL_MASSA;NAO_FUNCIONAL_EXECUCAO;NAO_FUNCIONAL_PLANEJAMENTO;\n")
# Ler as linhas do arquivo e verificar se todas as pastas foram devidamente criadas

VOB = ""
PASTA = ""
GRUPO_PASTA = ""

for linha in arquivo_dir:
    linha = linha.upper()
    if linha.find("DIRECTORY VERSION") > -1:
        if VOB == "":
            VOB = linha[linha.find("M:\F541364") + 19:linha.find('04-TESTES')-1]
        else:
            # Mudou a pasta -> Salvar as informações encontradas
            arquivo_saida.write(f"{VOB};{PASTA};{GRUPO_PASTA}\n")
            PASTA=""
            GRUPO_PASTA=""
            VOB = linha[linha.find("M:\F541364") + 19:linha.find('04-TESTES')-1]

    # PROCURA AS PASTAS E SUAS PROTEÇÕES
    if linha.find('04-TESTES@@') > -1:
        PASTA = '04-TESTES'

    # CERTIFICACAO
    if linha.find('04-TESTES\CERTIFICACAO@@') > -1:
        PASTA = 'CERTIFICACAO'
    if linha.find('04-TESTES\CERTIFICACAO\MASSA@@') > -1:
        PASTA = 'CERTIFICACAO_MASSA'
    if linha.find('04-TESTES\CERTIFICACAO\MASSA\ALTA@@') > -1:
        PASTA = 'CERTIFICACAO_MASSA_ALTA'
    if linha.find('04-TESTES\CERTIFICACAO\MASSA\ALTA\BATCH@@') > -1:
        PASTA = 'CERTIFICACAO_MASSA_ALTA_BATCH'
    if linha.find('04-TESTES\CERTIFICACAO\MASSA\ALTA\ONLINE@@') > -1:
        PASTA = 'CERTIFICACAO_MASSA_ALTA_ONLINE'
    if linha.find('04-TESTES\CERTIFICACAO\MASSA\BAIXA@@') > -1:
        PASTA = 'CERTIFICACAO_MASSA_BAIXA'
    if linha.find('04-TESTES\CERTIFICACAO\MASSA\BAIXA\BATCH@@') > -1:
        PASTA = 'CERTIFICACAO_MASSA_BAIXA_BATCH'
    if linha.find('04-TESTES\CERTIFICACAO\MASSA\BAIXA\ONLINE@@') > -1:
        PASTA = 'CERTIFICACAO_MASSA_BAIXA_ONLINE'
    if linha.find('04-TESTES\CERTIFICACAO\EXECUCAO@@') > -1:
        PASTA = 'CERTIFICACAO_EXECUCAO'
    if linha.find('04-TESTES\CERTIFICACAO\PLANEJAMENTO@@') > -1:
        PASTA = 'CERTIFICACAO_PLANEJAMENTO'

    # HOMOLOGACAO
    if linha.find('04-TESTES\HOMOLOGACAO@@') > -1:
        PASTA = 'HOMOLOGACAO'
    if linha.find('04-TESTES\HOMOLOGACAO\MASSA@@') > -1:
        PASTA = 'HOMOLOGACAO_MASSA'
    if linha.find('04-TESTES\HOMOLOGACAO\MASSA\ALTA@@') > -1:
        PASTA = 'HOMOLOGACAO_MASSA_ALTA'
    if linha.find('04-TESTES\HOMOLOGACAO\MASSA\ALTA\BATCH@@') > -1:
        PASTA = 'HOMOLOGACAO_MASSA_ALTA_BATCH'
    if linha.find('04-TESTES\HOMOLOGACAO\MASSA\ALTA\ONLINE@@') > -1:
        PASTA = 'HOMOLOGACAO_MASSA_ALTA_ONLINE'
    if linha.find('04-TESTES\HOMOLOGACAO\MASSA\BAIXA@@') > -1:
        PASTA = 'HOMOLOGACAO_MASSA_BAIXA'
    if linha.find('04-TESTES\HOMOLOGACAO\MASSA\BAIXA\BATCH@@') > -1:
        PASTA = 'HOMOLOGACAO_MASSA_BAIXA_BATCH'
    if linha.find('04-TESTES\HOMOLOGACAO\MASSA\BAIXA\ONLINE@@') > -1:
        PASTA = 'HOMOLOGACAO_MASSA_BAIXA_ONLINE'
    if linha.find('04-TESTES\HOMOLOGACAO\EXECUCAO@@') > -1:
        PASTA = 'HOMOLOGACAO_EXECUCAO'
    if linha.find('04-TESTES\HOMOLOGACAO\PLANEJAMENTO@@') > -1:
        PASTA = 'HOMOLOGACAO_PLANEJAMENTO'

    # NAO_FUNCIONAL
    if linha.find('04-TESTES\\NAO_FUNCIONAL@@') > -1:
        PASTA = 'NAO_FUNCIONAL'
    if linha.find('04-TESTES\\NAO_FUNCIONAL\\MASSA@@') > -1:
        PASTA = 'NAO_FUNCIONAL_MASSA'
    if linha.find('04-TESTES\\NAO_FUNCIONAL\\EXECUCAO@@') > -1:
        PASTA = 'NAO_FUNCIONAL_EXECUCAO'
    if linha.find('04-TESTES\\NAO_FUNCIONAL\\PLANEJAMENTO@@') > -1:
        PASTA = 'NAO_FUNCIONAL_PLANEJAMENTO'

    if linha.find("GROUP: ") > -1:
        GRUPO_PASTA = linha[linha.find("GROUP:") + 7:-1]

   
arquivo_dir.close()
arquivo_saida.close()