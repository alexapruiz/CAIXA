import sys

# Abrindo o arquivo de entrada
arquivo_dir = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\Pasta_Metrica_VOBx.txt',mode='r',encoding='UTF-8')
arquivo_saida = open('c:\\projetos\\CAIXA\\scripts\\clearcase\\arquivos\\Comandos_Metrica_VOBx.txt',mode='w',encoding='UTF-8')

VOB = ""
PASTA = ""
POSSUI_CONTEUDO = False

for linha in arquivo_dir:
    linha_uper = linha.upper()
    
    if linha_uper.find("DIRECTORY OF") > -1:
        if PASTA == "":
            PASTA = linha_uper[14:-1]
        else:
            # Verifica se deve salvar o resultado
            if ( (PASTA.find('04-TESTES\CERTIFICACAO\MASSA\BATCH') > -1) or (PASTA.find('04-TESTES\CERTIFICACAO\MASSA\ONLINE') > -1)) and (POSSUI_CONTEUDO == False):
                arquivo_saida.write(f"{PASTA2}\n")
                PASTA = linha_uper[14:-1]
                PASTA2 = linha[14:-1]
                POSSUI_CONTEUDO = False
            else:
                PASTA = linha_uper[14:-1]
                PASTA2 = linha[14:-1]
                POSSUI_CONTEUDO = False

    else:
        if not ((linha_uper.find('<DIR>          ..') > -1) or (linha_uper.find('<DIR>          .') > -1) or (linha_uper.find('\n') == 0) or (linha_uper.find('VOLUME IN DRIVE') > -1) or (linha_uper.find('VOLUME SERIAL NUMBER') > -1) or (linha_uper.find('FILE(S)') > -1) ):
            # Pasta com conteúdo
            POSSUI_CONTEUDO = True


arquivo_dir.close()
arquivo_saida.close()
