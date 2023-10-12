import sys

# Abrindo o arquivo de entrada
arquivo_entrada = open(sys.path[0] + "\\Lista_Areas.txt",encoding='UTF-8')
arquivo_saida = open(sys.path[0] + "\\saida_areas.csv", "w")
arquivo_saida.write(f"Area_Projeto;Arquivada\n")

Area_Projeto = ''
flag_area = False
Arquivada = False

for linha in arquivo_entrada:
    if linha.find('<com.ibm.team.process.ProjectArea>') != -1:
        # Inicio das informações sobre a área de projeto
        flag_area = True
    
    if linha.find('<internalProcessProvider>') != -1:
        flag_area = False

    if (linha.find('<name>') != -1 and flag_area == True):
        Area_Projeto = linha[6:-8]

    if linha.find('<archived>') != -1:
        Arquivada = linha[10:-12]

    if linha.find('</com.ibm.team.process.ProjectArea>') != -1:
        arquivo_saida.write(f"{Area_Projeto};{Arquivada}\n")
        Area_Projeto = ''
        flag_area = False
