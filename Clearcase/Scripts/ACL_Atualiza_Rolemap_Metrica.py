import sys

caminho = sys.path[0]

arquivo_saida = open(caminho + f"\\Arquivos\\comandos_atualiza_rolemap_metrica.txt",mode="w",encoding="UTF-8")

with open(caminho + f"\\Arquivos\\Atualizar_rolemap_metrica.txt",mode="r",encoding="UTF-8") as arquivo_origem:
    for linha in arquivo_origem:
        if len(linha) > 1:
            linha = linha.split(";")
            VOB = linha[0]
            FABRICA = linha[1]
            COMUNIDADE = linha[2]
            COMUNIDADE = COMUNIDADE.replace("\n","")

            arquivo_saida.write(f"cleartool mkrolemap -nc -replace -set \\cbrsvaprnt005.extra.caixa.gov.br\Clearcase_Admin\ACL\arquivos_config\{COMUNIDADE}\{FABRICA}\Rolemap_metrica.txt -policy CAIXA@/{VOB} Rolemap_metrica@\{VOB}\n")

    arquivo_saida.close()