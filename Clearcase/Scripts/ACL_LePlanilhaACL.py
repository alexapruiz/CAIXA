#Importando as bibliotecas
import os
import sys

def LePlanilhaACL():
	# Le a planilha de Controle e extrai as VOBs, por comunidade

	arquivo_saida = open(f"{caminho}\\Arquivos\\VOBs.txt",mode="w",encoding="UTF-8")

	try:
		planilha = openpyxl.load_workbook(f"{caminho}\\Arquivos\\Controle VOBs Migradas ACL_nova.xlsx")

		COMUNIDADES = "SEM_COMUNIDADE_FABRICA;ARRECADACAO;CAMBIO;CANAIS_DIGITAIS;CANAIS_FISICOS;CLIENTES;CONTRATACOES;CREDITO;DADOS;DEPOSITO;ESTRUTURANTES_TI;FINANCEIRO_CONTROLADORIA;FOMENTO_DJ;FUNDOS_GOVERNO;HABITACAO;INSTITUCIONAL;MEIOS_PAGAMENTO;PESSOAS;PROGRAMAS_SOCIAIS;RISCO;SEGURANCA"
		lista_Comunidades = COMUNIDADES.split(";")
		
		for comunidade_atual in range(0,len(lista_Comunidades)):

			Inicio_VOBs = False
			for linha in range(1, int(planilha[lista_Comunidades[comunidade_atual]].dimensions.split(":")[1][1:])):
			
				if Inicio_VOBs == True:
					arquivo_saida.write(lista_Comunidades[comunidade_atual] + ";" + planilha[lista_Comunidades[comunidade_atual]][f"A{linha}"].value)
					arquivo_saida.write("\n")

				if planilha[lista_Comunidades[comunidade_atual]][f"A{linha}"].value == 'VOB':
					Inicio_VOBs = True
	

	except Exception as erro:
		print(f"Ocorreu um erro durante a leitura da planilha ACL - LePlanilhaACL - [' {erro}' ]")
		return


sys.path.insert(0, 'c://projetos//CAIXA//Funcoes')
caminho = sys.path[1]

# Gera a planilha com as VOBs e os grupos
LePlanilhaACL()
