# Abrindo o arquivo de entrada
with open('C:\Projetos\CAIXA\Scripts\Clearcase\Arquivos\saida_Locks_SP.txt',mode='w',encoding="UTF-8") as saida:
    with open('C:\Projetos\CAIXA\Scripts\Clearcase\Arquivos\Locks_SP.txt',mode='r',encoding="UTF-8") as entrada:
        for linha in entrada:
            if linha.find("lock directory element") > -1:
                POSICAO_INICIAL = linha.find("M:\\f541364_view5") + 16
                POSICAO_FINAL = linha.find("@@")

                DIRETORIO = linha[POSICAO_INICIAL+1:POSICAO_FINAL]
                VOB = DIRETORIO[0:DIRETORIO.find("\\")]

                if ( (DIRETORIO.find(f"{VOB}\\.") != -1) and (len(DIRETORIO) != int(len(VOB)+2)) ):
                    saida.write(DIRETORIO + "\n")

                if ( (DIRETORIO.find(f"{VOB}\\01-Requisitos") != -1) and (len(DIRETORIO) != int(len(VOB)+14)) ):
                    saida.write(DIRETORIO + "\n")

                if ( (DIRETORIO.find(f"{VOB}\\04-Testes") != -1) and (len(DIRETORIO) != int(len(VOB)+10))):
                    saida.write(DIRETORIO + "\n")
