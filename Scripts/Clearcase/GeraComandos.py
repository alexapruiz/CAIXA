# Importando as bibliotecas
import os
import sys

# Verifica se esta sendo chamado por um interpretador python ou executavel
if sys.argv[0].find(".exe") > -1:
	caminho = sys.path[2]
else:
	caminho = sys.path[0]

# Cria a pasta 'Arquivos', caso não exista
if not os.path.exists(caminho + "\\Arquivos"):
	os.makedirs(caminho + "\\Arquivos")

# Gera os comandos de acordo com o arquivo de origem
try:
	print("Abrindo os arquivos de saida...")
	# Abre os arquivos de saida (DESC e NET SHARE)
	arquivo_saida_desc = open(f"{caminho}\\Arquivos\\Comandos_DESC.txt", mode="w", encoding = "UTF-8")
	arquivo_saida_NETSHARE_SP = open(f"{caminho}\\Arquivos\\Comandos_NETSHARE_SP.txt",mode="w",encoding="UTF-8")
	arquivo_saida_NETSHARE_BR = open(f"{caminho}\\Arquivos\\Comandos_NETSHARE_BR.txt",mode="w",encoding="UTF-8")
	arquivo_saida_NETSHARE_RJ = open(f"{caminho}\\Arquivos\\Comandos_NETSHARE_RJ.txt",mode="w",encoding="UTF-8")
	arquivo_saida_NETSHARE_CEPEM = open(f"{caminho}\\Arquivos\\Comandos_NETSHARE_CEPEM.txt",mode="w",encoding="UTF-8")
	arquivo_saida_NETSHARE_LOTERIAS = open(f"{caminho}\\Arquivos\\Comandos_NETSHARE_LOTERIAS.txt",mode="w",encoding="UTF-8")

	print("Lendo o arquivo LSVOB.txt e gerando os arquivos com os comandos...")
	with open(f"{caminho}\\Arquivos\\LSVOB.txt", mode="r", encoding = 'UTF-8') as arquivo_entrada:
		for linha in arquivo_entrada:
			# Para cada linha do arquivo LSVOB.txt, cria um comando DESC
			linha = linha.upper()

			POSICAO_INICIAL = linha.find("\\")
			POSICAO_FINAL = linha.find("\\\\")

			VOB = linha[linha.find("\\")+1 : linha.find("\\\\")].strip()
			
			comando_desc = f"cleartool desc vob:\\{VOB} >> DESC.txt\n"

			SERVIDOR = linha[POSICAO_FINAL + 2:POSICAO_FINAL + 34].strip()
			if SERVIDOR.find("CADSVAPRNT002") > -1:
				comando_NETSHARE_SP = f"net share {VOB}$ >> NETSHARE_SP.txt\n"
				arquivo_saida_NETSHARE_SP.write(comando_NETSHARE_SP)
			if SERVIDOR.find("CBRSVAPRNT005") > -1:
				comando_NETSHARE_BR = f"net share {VOB}$ >> NETSHARE_BR.txt\n"
				arquivo_saida_NETSHARE_BR.write(comando_NETSHARE_BR)
			if SERVIDOR.find("CADSVAPRNT009") > -1:
				comando_NETSHARE_RJ = f"net share {VOB}$ >> NETSHARE_RJ.txt\n"
				arquivo_saida_NETSHARE_RJ.write(comando_NETSHARE_RJ)
			if SERVIDOR.find("CBRSVAPRNT010") > -1:
				comando_NETSHARE_CEPEM = f"net share {VOB}$ >> NETSHARE_CEPEM.txt\n"
				arquivo_saida_NETSHARE_CEPEM.write(comando_NETSHARE_CEPEM)
			if SERVIDOR.find("CBRSVAPRNT013") > -1:
				comando_NETSHARE_LOTERIAS = f"net share {VOB}$ >> NETSHARE_LOTERIAS.txt\n"
				arquivo_saida_NETSHARE_LOTERIAS.write(comando_NETSHARE_LOTERIAS)

			arquivo_saida_desc.write(comando_desc)

except Exception as erro:
	print(f"Ocorreu um erro durante a criacao dos arquivos com os comandos -  [' {erro}' ]")

print(f"Arquivos gerados com sucesso!!!")