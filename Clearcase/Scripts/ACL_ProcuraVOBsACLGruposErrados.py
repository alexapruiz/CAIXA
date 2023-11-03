import sys

GRUPOS_COMUNIDADE="CC_ARRECADACAO,CC_CAMBIO,CC_CANAIS_DIGITAIS,CC_CANAIS_FISICOS,CC_CLIENTES,CC_CONTRATACOES,CC_CREDITO,CC_DADOS,CC_DEPOSITO,CC_ESTRUTURANTES_TI,CC_FINANCEIRO_CONTROLADORIA,CC_FOMENTO_DJ,CC_FUNDOS_GOVERNO,CC_HABITACAO,CC_INSTITUCIONAL,CC_LOTERIAS,CC_MEIOS_PAGAMENTO,CC_PESSOAS,CC_PROGRAMAS_SOCIAIS,CC_RISCO,CC_SEGURANCA"
GRUPOS_FABRICAS = "CC_ATOS,CC_BENNER,CC_BRQ,CC_BRY,CC_CAST,CC_CPQD,CC_DATAINFO,CC_DBA,CC_ESEC,CC_FIRST,CC_FOTON,CC_GLOBALWEB,CC_INDRA,CC_LATIN,CC_MAGNA,CC_MAPS,CC_MURAH,CC_PEOPLEWARE,CC_RESOURCE,CC_RJE,CC_SENIOR,CC_SONDA,CC_SPREAD,CC_STEFANINI,CC_TIVIT,CC_TREE,CC_TTY,CC_UNISYS,CC_VERT_SAS,CC_WIPRO"
OUTROS_GRUPOS = "CC_CERTIFICACAO,CC_CAIXA_ESCRITA,CC_TODOS_ESCRITA,CC_METRICA,CC_TRANSVERSAL"


# Abrindo os arquivos de entrada e saida
entrada = open(sys.path[0] + "\\Arquivos\\DESC5.txt",mode='r',encoding='UTF-8')
saida_BR = open(sys.path[0] + "\\Arquivos\\Comandos_Remocao_Grupos_BR.txt",mode='w',encoding='UTF-8')
saida_SP = open(sys.path[0] + "\\Arquivos\\Comandos_Remocao_Grupos_SP.txt",mode='w',encoding='UTF-8')
saida_RJ = open(sys.path[0] + "\\Arquivos\\Comandos_Remocao_Grupos_RJ.txt",mode='w',encoding='UTF-8')
saida_CEPEM = open(sys.path[0] + "\\Arquivos\\Comandos_Remocao_Grupos_CEPEM.txt",mode='w',encoding='UTF-8')

VOB = ""
SERVIDOR = ""
COMUNIDADE = ""
FABRICA = ""
ACL_ATIVADO = False
Possui_Grupos_Errados = False

for linha in entrada:
    linha = linha.upper()
    linha = linha.strip()
    if linha.find("VERSIONED OBJECT BASE") > -1:
        if (VOB == ""):
            # Apenas na primeira VOB
            VOB = linha[24:-1]
        else:
            if ACL_ATIVADO == True and Possui_Grupos_Errados == True:
                if SERVIDOR == 'CBRSVAPRNT005':
                    saida_BR.write(f"{VOB} {COMUNIDADE} {FABRICA}\n")
                if SERVIDOR == 'CADSVAPRNT002':
                    saida_SP.write(f"{VOB} {COMUNIDADE} {FABRICA}\n")
                if SERVIDOR == 'CADSVAPRNT009':
                    saida_RJ.write(f"{VOB} {COMUNIDADE} {FABRICA}\n")
                if SERVIDOR == 'CBRSVAPRNT010':
                    saida_CEPEM.write(f"{VOB} {COMUNIDADE} {FABRICA}\n")
                 
            
            VOB=linha[24:-1]
            SERVIDOR = ""
            ACL_ATIVADO = False
            Possui_Grupos_Errados = False

            
    if linha.find("ACLS FEATURE LEVEL:") != -1:
        ACL_ATIVADO = True

    if linha.find("VOB STORAGE HOST") != -1:
        SERVIDOR = linha[linha.find(".EXTRA.CAIXA")-13:linha.find(".EXTRA.CAIXA")]

    if linha.find("GROUP") > -1 and linha.find("DOMAIN USERS") == -1 and linha.find("G7259CCL") == -1 and linha.find("ADDITIONAL GROUPS") == -1 and linha.find("DF5222") > -1:
        Possui_Grupos_Errados = True


entrada.close()
saida_BR.close()
saida_SP.close()
saida_RJ.close()
saida_CEPEM.close()
