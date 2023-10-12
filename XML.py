import sys


class XML():

    def Le_XML_Gera_CSV(arquivo_entrada, arquivo_saida):

        try:
            #Abrir arquivo XML
            arq_entrada = open(arquivo_entrada)

            #Criar arquivo de saida
            arq_saida = open(arquivo_saida, "w", encoding="ANSI")

            #Escrever a primeira linha, com o cabeçalho
            linha_saida = '' + '\n'
            arq_saida.write(linha_saida)

            for linha in arq_entrada:
                if linha.find('/obj') != -1:
                    #Gravar as linhas encontradas
                    linha_saida = SIGLA + ';' + SQUAD + ';' + COMUNIDADE + ';' + MATRICULA + ';' + PAPEL + '\n'
                    arq_saida.write(linha_saida)
                if linha.find('SIGLA') != -1:
                    SIGLA = linha[15:20]
                if linha.find('<SQUAD>') != -1:
                    FIM_SQUAD = int(linha.find('</SQUAD>'))
                    SQUAD = linha[15:FIM_SQUAD]
                if linha.find('<COMUNIDADE>') != -1:
                    FIM_COMUNIDADE = int(linha.find('</COMUNIDADE>'))
                    COMUNIDADE = linha[20:FIM_COMUNIDADE]
                if linha.find('MATRICULA') != -1:
                    MATRICULA = linha[19:26]
                if linha.find('PAPEL') != -1:
                    FIM_PAPEL = int(linha.find('</PAPEL>'))
                    PAPEL = linha[15:FIM_PAPEL]

        except:
            print("Unexpected error:", sys.exc_info()[0])
        else:
            print("Unexpected error:", sys.exc_info()[0])
            pass