import sys

VOB = ""
ACL_ATIVADO = False
ENCONTROU_GRUPO = False
GRUPOS = ""
qtde = 0

arquivo_saida1 = open("C:\\projetos\\CAIXA\\Clearcase\\Scripts\\Arquivos\\VOBs_sem_ACL_sem_grupos.txt", mode='w', encoding='UTF-8')

with open("C:\\projetos\\CAIXA\\Clearcase\\Scripts\\Arquivos\\DESC_ACL.txt", mode='r', encoding='UTF-8') as arquivo_DESC:
    for linha in arquivo_DESC:
        linha2 = linha.upper()

        if linha2.find("VERSIONED OBJECT BASE") > -1:
            if VOB == "":
                # Apenas na primeira VOB
                VOB = linha2.split("\\")[1].split('"')[0]
            else:
                if ACL_ATIVADO == False and ENCONTROU_GRUPO == False:
                    # A VOB não está com o ACL ativado e não tem outros grupos adicionais além do CORPCAIXA\Domain Users
                    qtde += 1
                    arquivo_saida1.write(f"{VOB}\n")

                VOB = linha2.split("\\")[1].split('"')[0]
                ACL_ATIVADO = False
                ENCONTROU_GRUPO = False
                GRUPOS = ""

        if linha2.find("ACLS FEATURE LEVEL") > -1:
            ACL_ATIVADO = True

        if linha2.find("ACLS ENABLED: NO") > -1:
            ACL_ATIVADO = False

        if linha2.find("GROUP CORPCAIXA") > -1:
            if (linha2.find("DOMAIN USERS") == -1) and (linha2.find("G7259CCL") == -1) :
                ENCONTROU_GRUPO = True
                GRUPOS += linha2.strip()[6:] + ";"

print(qtde)
