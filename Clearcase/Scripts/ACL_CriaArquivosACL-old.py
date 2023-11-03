# Importando as bibliotecas
import os
import sys

sys.path.insert(0, 'c://Projetos//CAIXA//Funcoes')
from BancodeDados import SQLite


def CriaArquivoACLsemFabrica(COMUNIDADE):
	# Rolemap_leitura
	with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_leitura.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
		arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")

	# Rolemap_caixa
	with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_caixa.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
		arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
		arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")

	# Rolemap_desenvolvimento
	with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_desenvolvimento.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
		arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
		arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")

	# Rolemap_metrica
	with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_metrica.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
		arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
		arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
		arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")

	# Rolemap_certificacao
	with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_certificacao.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
		arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
		arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")

	# Rolemap_todos
	with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\Rolemap_todos.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
		arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
		arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
		arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
		arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")



def GeraArquivosACL():
	try:
		# Pesquisar as comunidades na base de dados
		cursor_comunidades = BancodeDados.ConsultaSQL("SELECT DISTINCT(comunidade) FROM VOBs where COMUNIDADE IS NOT NULL AND COMUNIDADE <> '' ORDER BY COMUNIDADE")
		COMUNIDADES = cursor_comunidades.fetchone()
		while COMUNIDADES:
			# Para cada comunidade, criar a pasta e pesquisar pelas fábricas
			COMUNIDADE = COMUNIDADES[0].strip()

			os.mkdir(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}")

			CriaArquivoACLsemFabrica(COMUNIDADE)

			# Para cada comunidade, pesquisar os grupos de compartilhamento
			cursor_grupos_comunidade = BancodeDados.ConsultaSQL(f"SELECT GRUPO_COMUNIDADE FROM GRUPOS_COMUNIDADE WHERE COMUNIDADE = '{COMUNIDADE}'")
			GRUPOS_COMUNIDADE = cursor_grupos_comunidade.fetchone()
			lista_grupos_comunidade = []
			while GRUPOS_COMUNIDADE:
				lista_grupos_comunidade.append(GRUPOS_COMUNIDADE[0].strip())
				GRUPOS_COMUNIDADE = cursor_grupos_comunidade.fetchone()


			# Pesquisar as fabricas
			cursor_fabricas = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(FABRICA) FROM VOBs where COMUNIDADE like '%{COMUNIDADE}%' AND FABRICA <> ''")
			FABRICAS = cursor_fabricas.fetchone()
			while FABRICAS:
				FABRICA = FABRICAS[0].strip()

				# Para cada fabrica, pesquisar os grupos de compartilhamento
				cursor_grupos_fabricas = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(GRUPO_COMPART) FROM COMPARTILHAMENTOS where GRUPO_COMPART like '%{COMUNIDADE}%' AND GRUPO_COMPART like '%{FABRICA}%'")
				GRUPOS_FABRICA = cursor_grupos_fabricas.fetchone()
				lista_grupos_fabrica = []
				while GRUPOS_FABRICA:
					lista_grupos_fabrica.append(GRUPOS_FABRICA[0].strip())
					GRUPOS_FABRICA = cursor_grupos_fabricas.fetchone()

				# Criar as pastas da fabrica, dentro da comunidade
				os.mkdir(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}")

				# Rolemap_leitura
				with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_leitura.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
					arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
					for grupo_comunidade in lista_grupos_comunidade:
						arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{grupo_comunidade}" + "\n")

					for grupo_fsw in lista_grupos_fabrica:
						arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{grupo_fsw}" + "\n")

				# Rolemap_caixa
				with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_caixa.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
					arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
					arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
					for grupo_comunidade in lista_grupos_comunidade:
						arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{grupo_comunidade}" + "\n")

					for grupo_fsw in lista_grupos_fabrica:
						arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{grupo_fsw}" + "\n")


				# Rolemap_desenvolvimento
				with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_desenvolvimento.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
					arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
					arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
					for grupo_comunidade in lista_grupos_comunidade:
						arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{grupo_comunidade}" + "\n")

					for grupo_fsw in lista_grupos_fabrica:
						arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{grupo_fsw}" + "\n")


				# Rolemap_metrica
				with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_metrica.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
					arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
					arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
					arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas" + "\n")
					for grupo_comunidade in lista_grupos_comunidade:
						arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{grupo_comunidade}" + "\n")

					for grupo_fsw in lista_grupos_fabrica:
						arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{grupo_fsw}" + "\n")


				# Rolemap_certificacao
				with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_certificacao.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
					arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
					arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
					for grupo_comunidade in lista_grupos_comunidade:
						arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{grupo_comunidade}" + "\n")

					for grupo_fsw in lista_grupos_fabrica:
						arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\{grupo_fsw}" + "\n")


				# Rolemap_todos
				with open(caminho + f"\\Arquivos\\ACL\\{COMUNIDADE}\\{FABRICA}\\Rolemap_todos.txt",mode="w",encoding="UTF-8") as arquivo_rolemap:
					arquivo_rolemap.write(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM" + "\n")
					arquivo_rolemap.write(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL" + "\n")
					arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}" + "\n")
					arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO" + "\n")
					for grupo_comunidade in lista_grupos_comunidade:
						arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{grupo_comunidade}" + "\n")

					for grupo_fsw in lista_grupos_fabrica:
						arquivo_rolemap.write(f"Role:Escrita --> Group:CORPCAIXA\{grupo_fsw}" + "\n")


				FABRICAS = cursor_fabricas.fetchone()

			COMUNIDADES = cursor_comunidades.fetchone()

	except Exception as erro:
		print(f"Ocorreu um erro durante a geracao dos arquivos ACL -  [' {erro}' ]")


caminho = sys.path[1]

# Abre a conexao do banco de dados
BancodeDados = SQLite(f"{caminho}\\Clearcase.db")

# Gera os arquivos de configuracao do ACL
GeraArquivosACL()

print("O arquivo com as informações dos grupos (ACL) foram gerados com sucesso!!!")