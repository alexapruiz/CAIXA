#Importando as bibliotecas
import os
import sys

OUTROS_GRUPOS="CC_ARRECADACAO,CC_CAMBIO,CC_CANAIS_DIGITAIS,CC_CANAIS_FISICOS,CC_CLIENTES,CC_CONTRATACOES,CC_CREDITO,CC_DADOS,CC_DEPOSITO,CC_ESTRUTURANTES_TI,CC_FINANCEIRO_CONTROLADORIA,CC_FOMENTO_DJ,CC_FUNDOS_GOVERNO,CC_HABITACAO,CC_INSTITUCIONAL,CC_LOTERIAS,CC_MEIOS_PAGAMENTO,CC_PESSOAS,CC_PROGRAMAS_SOCIAIS,CC_RISCO,CC_SEGURANCA,CC_CERTIFICACAO,CC_CAIXA_ESCRITA,CC_TODOS_ESCRITA,CC_METRICA,CC_TRANSVERSAL"


arquivo_saida = "C:\\projetos\\CAIXA\\Clearcase\\Arquivos\\Grupos_5222.txt"
saida = open(arquivo_saida,mode='w',encoding = 'UTF-8')

# Abre o arquivo com o DESC e escreve os grupos DF5222 no arquivo de saida
try:
    with open("C:\\projetos\\CAIXA\\Clearcase\\Arquivos\\DESC.txt", mode='r', encoding = 'UTF-8') as arquivo:
        for linha in arquivo:
            linha2 = linha.upper()

            if linha2.find("G DF5222") > -1:
                if OUTROS_GRUPOS.find(linha2[linha2.find("CC_"):-1]) == -1:
                    saida.write(linha)

    saida.close()
    
except Exception as erro:
    print(f"Ocorreu um erro durante a analise do arquivo DESC.txt - LeGruposDESC - [' {erro}' ]")
