#Importando as bibliotecas
import os
import sys
from PyQt5.QtWidgets import QMessageBox , QFileDialog
#import clipboard as area_transf
#from xml.etree import ElementTree as xml

#Importando os arquivos das funções comuns
sys.path.append('c:\\Projetos\\Python\\Funcoes')
from MessageBox import MessageBox


class RDNG(object):
    """description of class"""

    def Gera_URLs_Remocao_Links(caminho_entrada):
        # Abrindo os arquivos de entrada e saida
        arquivo_entrada = open(caminho_entrada)
        arquivo_saida = open(caminho_entrada[:-4] + '_saida.txt', "w")

        for linha in arquivo_entrada:
            # Identifica o ID da área de projeto
            UUID_AREA_PROJETO = linha[linha.find('Frm-projects%2F') + 15:linha.find('Frm-projects%2F') + 38 ]
            # Identifica o ID do componente
            UUID_COMPONENTE = linha[linha.find('2Fcomponents%2F') + 15:linha.find('2Fcomponents%2F') + 38 ]
            
            # Cria URL para obtenção do arquivo Types.rdf
            URL_TYPES = 'https://gid.caixa:9443/rm/types?accept=*&private=true&resourceContext=https://gid.caixa:9443/rm/process/project-areas/' + UUID_AREA_PROJETO + '/components/' + UUID_COMPONENTE

            print('Segue a URL para geração do arquivo types.rdf')
            print('')
            print(URL_TYPES)
            print('')
            area_transf.copy(URL_TYPES)
            arquivo_saida.write(URL_TYPES)
            MessageBox.Mensagem("URL para geração do arquivo Types.rdf copiado para a área de transferência e para o arquivo de saida: " + caminho_entrada[:-4] + '_saida.txt',"Informação",QMessageBox.Information,QMessageBox.Ok)

            # Vinculação 	- https://gid.caixa:9443/rm/types/_tuwbcXvYEemePcYu8juqzw
	        # Integração 	- https://gid.caixa:9443/rm/types/_txe_UXvYEemePcYu8juqzw
	        # Referencia 	- https://gid.caixa:9443/rm/types/_iqdAgXvYEemePcYu8juqzw

            #	Cabeçalhos:
	        # DoorsRP-Request-Type			private
	        # net.jazz.jfs.owning-context	https://gid.caixa:9443/rm/rm-projects/_ha3n8HvYEemePcYu8juqzw/components/_h8_dkHvYEemePcYu8juqzw
	        # vvc.configuration				https%3A%2F%2Fgid.caixa%3A9443%2Frm%2Fcm%2Fstream%2F_aiL4ANr4EeaTiJjPR2CG_w <somente para GC habilitado>


    def Gera_Lista_Areas():
        # Abrindo os arquivos de entrada
        arquivo_oslc = open('C:\Projetos\CAIXA\RDNG\Areas_RDNG_OSLC.txt',mode='r',encoding='UTF-8')
        arquivo_rb = open('C:\Projetos\CAIXA\RDNG\Areas_RDNG_RB.txt',mode='r',encoding='UTF-8')

        # Abrindo o arquivo de saida
        #saida = open('C:\Projetos\CAIXA\RDNG\Areas_RDNG_Total.csv',mode='w',encoding='UTF-8')

        # Inicializa as listas
        areas_oslc = []
        areas_rb = []
        # Lê o arquivo de OSLC (maior) e armazena as áreas de projeto do RDNG
        for linha in arquivo_oslc:
            if linha.find('</com.ibm.team.process.ProjectArea>') > -1:
                # Fim do dados da área -> gravar o resultado
                if (arquivada == 'false'):
                    #saida.write(area + ';' + master + '\n')
                    areas_oslc.append(area)
            elif linha.find('com.ibm.team.process.ProjectArea') > -1:
                # encontrou a chave da área
                chave = 'area'
            elif linha.find('internalProcessProvider') > -1:
                # encontrou a chave da área-modelo
                chave = 'master'
            elif linha.find('archived') > -1:
                arquivada = linha[10:-12]

            if linha.find('<name>') > -1:
                # Encontrou o nome de uma área de projeto, se a  chave for de área, lê os dados
                if (chave == 'area'):
                    area = linha[6:-8]
                elif (chave == 'master'):
                    master = linha[6:-8]

        # Lê o arquivo do RB e cria uma segunda lista
        for linha in arquivo_rb:
            if linha.find('Projeto RM') > -1:
                areas_rb.append(linha[1:-14])

        # Cria um conjunto com todas as áreas (removendo as duplicidades)
        areas_rdng = set(areas_oslc + areas_rb)
        with open('C:\Projetos\CAIXA\RDNG\Areas_RDNG_Total.txt',mode='w',encoding='UTF-8') as saida:
            for area in areas_rdng:
                saida.write(area + '\n')

        return 'Ok'