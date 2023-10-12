import sys

sys.path.append('c:\\Projetos\\CAIXA\\Funcoes')
from BancodeDados import SQLite

DB = SQLite(sys.path[0] + '\\Clearcase.db')


def Importa_Grupos_NETSHARE(arquivo):
    # Importar dados do NETSHARE para banco de dados
    Arquivo_NET_SHARE = open(sys.path[0] + f"\\Arquivos\\{arquivo}",mode='r',encoding='UTF-8')
    for linha_NETSHARE in Arquivo_NET_SHARE:
        if linha_NETSHARE.find("Share name") > -1:
            VOB = linha_NETSHARE[18:-1]

        if linha_NETSHARE.find("Path") > -1:
            PATH = linha_NETSHARE[18:-1] + "$"

        if linha_NETSHARE.find("The command completed successfully") > -1:
            VOB = ''
            GRUPO = ''
            PATH = ''

        if linha_NETSHARE.find("CORPCAIXA") > -1:
            # Insere o grupo / permissão
            GRUPO = linha_NETSHARE[18:-1]
            DB.ExecutaComandoSQL(f"INSERT INTO DADOS_NETSHARE2 (SERVIDOR,VOB,PATH,GRUPO) VALUES ('{arquivo}','{VOB}','{PATH}','{GRUPO}')")


# Importa os dados dos grupos de compartilhamento
Importa_Grupos_NETSHARE('NET_SHARE_SP.txt')
Importa_Grupos_NETSHARE('NET_SHARE_BR.txt')
Importa_Grupos_NETSHARE('NET_SHARE_RJ.txt')
Importa_Grupos_NETSHARE('NET_SHARE_CEPEM.txt')

# Abrindo os arquivos de entrada e saida
arquivo_VOBs_sem_grupo = open(sys.path[0] + "\\Arquivos\\VOBs_reproteger.txt",mode='r',encoding='UTF-8')
arquivo_comandos_incluir_TRANSVERSAL = open(sys.path[0] + "\\Arquivos\\Comandos_para_incluir_TRANSVERSAL.txt",mode='w',encoding='UTF-8')

VOB=''
for linha_VOB in arquivo_VOBs_sem_grupo:
    VOB = linha_VOB[:-1]

    # Pesquisa os grupos atuais do compartilhamento
    cursor_compart = DB.ConsultaSQL(f"select VOB,PATH,GRUPO from DADOS_NETSHARE where VOB = '{VOB}$'")
    Compart = cursor_compart.fetchone()

    Comando_grupos=""
    if Compart:
        PATH = Compart[1]
        while Compart:
            Comando_grupos += f'/GRANT:"{Compart[2].strip()}" '
    
            Compart = cursor_compart.fetchone()

    arquivo_comandos_incluir_TRANSVERSAL.write(f"net share {VOB}$ /del \n")

    Comando_grupos += '/GRANT:"CORPCAIXA\G DF5222 CC_TRANSVERSAL",CHANGE'
    Comando = f'net share {VOB}$="{PATH[:-1]}" {Comando_grupos}/CACHE:None \n'
    arquivo_comandos_incluir_TRANSVERSAL.write(Comando )

arquivo_VOBs_sem_grupo.close()
arquivo_comandos_incluir_TRANSVERSAL.close()
