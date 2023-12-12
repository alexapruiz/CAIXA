import sys

# Abrindo o arquivo de entrada
entrada = open(sys.path[0] + "\\Arquivos\\DIR_LOST.txt",mode='r',encoding='UTF-8')
#saida1 = open(sys.path[0] + "\\Arquivos\\DIR_LOST-saida.txt",mode='w',encoding='UTF-8')
saida2 = open(sys.path[0] + "\\Arquivos\\DIR_LOST-saida_por_VOB.txt",mode='w',encoding='UTF-8')

VOB = ""
qtde_arquivos = 0
data_ultima_alteracao = ""
data_arquivo = ""

for linha in entrada:
    if linha.find("Directory of") > -1:
        if not (VOB == ""):
            if qtde_arquivos > 100 and int(data_ultima_alteracao[:4]) < 2023:
                saida2.write(f"VOB: {VOB} - Qtde arquivos: {qtde_arquivos} - Data Ultima Alteracao: {data_ultima_alteracao} \n")

        VOB = linha.split("\\")[2]
        qtde_arquivos=0
        data_ultima_alteracao=""

    else:
        # Se os primeiros caracteres corresponderem a uma data valida, é um elemento a ser contado
        if len(linha) > 37:
            if not ( (linha[36] == ".") or (linha[37] == ".") or (linha.find("bytes") > 0) ):
                qtde_arquivos += 1
                data_arquivo = linha[6:10] + linha[3:5] + linha[0:2]
                if data_arquivo > data_ultima_alteracao:
                    data_ultima_alteracao = data_arquivo
                #saida1.write(linha)

    
    
entrada.close()
#saida1.close()
saida2.close()