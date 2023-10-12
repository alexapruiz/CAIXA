#Importando as bibliotecas
import os
import sys

from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox , QFileDialog , QApplication
from tkinter import *
from pathlib import Path
from openpyxl import Workbook

sys.path.append('c:\\Projetos\\CAIXA\\Funcoes')
from BancodeDados import SQLite
from MessageBox import MessageBox


def Preenche_Combos():
    # Busca as informações sobre comunidades, fábricas e servidores para o preenchimento dos combos

    # Combo Comunidades
    Principal.Cbo_Comunidades.clear()
    Principal.Cbo_Comunidades.addItem('')
    cursor_comunidades = BancodeDados.ConsultaSQL("SELECT DISTINCT COMUNIDADE FROM VOBS WHERE COMUNIDADE <> '' ORDER BY COMUNIDADE")
    COMUNIDADES = cursor_comunidades.fetchone()
    while COMUNIDADES:
        Principal.Cbo_Comunidades.addItem(COMUNIDADES[0])
        COMUNIDADES = cursor_comunidades.fetchone()

    # Combo Fabricas
    Principal.Cbo_Fabricas.clear()
    Principal.Cbo_Fabricas.addItem('')
    cursor_fabricas = BancodeDados.ConsultaSQL("SELECT DISTINCT FABRICA FROM VOBS WHERE FABRICA <> ''  ORDER BY FABRICA")
    FABRICAS = cursor_fabricas.fetchone()
    while FABRICAS:
        Principal.Cbo_Fabricas.addItem(FABRICAS[0])
        FABRICAS = cursor_fabricas.fetchone()

    # Combo Servidores
    Principal.Cbo_Servidores.clear()
    Principal.Cbo_Servidores.addItem('')
    cursor_servidores = BancodeDados.ConsultaSQL("SELECT * FROM SERVIDORES")
    SERVIDORES = cursor_servidores.fetchone()
    while SERVIDORES:
        Principal.Cbo_Servidores.addItem(SERVIDORES[1])
        SERVIDORES = cursor_servidores.fetchone()


def CarregaListaVOBs(comunidade, fabrica, servidor, vob):
    try:
        # Carrega as VOBs e demais informacoes no grid principal
        Principal.Tabela_VOBs.setColumnCount(4)
        Principal.Tabela_VOBs.setColumnWidth(0,250)
        Principal.Tabela_VOBs.setColumnWidth(1,290)
        Principal.Tabela_VOBs.setColumnWidth(2,250)
        Principal.Tabela_VOBs.setColumnWidth(3,184)

        CLAUSULA_COMUNIDADE=""
        CLAUSULA_FABRICA=""
        CLAUSULA_SERVIDOR=""
        CLAUSULA_VOB = ""

        # Verifica se a funcao foi chamada com algum parametro
        if len(comunidade) > 0:
            CLAUSULA_COMUNIDADE = f" AND COMUNIDADE = '{comunidade}'"

        if len(fabrica) > 0:
            CLAUSULA_FABRICA = f" AND FABRICA = '{fabrica}'"

        if len(servidor) > 0:
            CLAUSULA_SERVIDOR = f" AND SERVIDOR = '{servidor}'"

        if len(vob) > 0:
            vob = vob.rstrip()
            vob = vob.replace('*','%')
            CLAUSULA_VOB = f" AND VOB like '{vob}'"

        # Carrega a lista de VOBs de acordo com o filtro selecionado
        ComandoSQL = "SELECT VOB , COMUNIDADE , FABRICA , SERVIDOR FROM VOBS WHERE VOB is not null "
        ComandoSQL += CLAUSULA_COMUNIDADE
        ComandoSQL += CLAUSULA_FABRICA
        ComandoSQL += CLAUSULA_SERVIDOR
        ComandoSQL += CLAUSULA_VOB
        ComandoSQL += " ORDER BY VOB"
        cursor_VOBs = BancodeDados.ConsultaSQL(ComandoSQL)

        VOBs = cursor_VOBs.fetchone()
        linha=0
        SERVIDOR=''
        Principal.Tabela_VOBs.setRowCount(0)
    
        while VOBs:
            Principal.Tabela_VOBs.setRowCount(int(linha+1))

            Principal.Tabela_VOBs.setItem(linha,0,QtWidgets.QTableWidgetItem(VOBs[0]))
            Principal.Tabela_VOBs.setItem(linha,1,QtWidgets.QTableWidgetItem(VOBs[1]))
            Principal.Tabela_VOBs.setItem(linha,2,QtWidgets.QTableWidgetItem(VOBs[2]))
            Principal.Tabela_VOBs.setItem(linha,3,QtWidgets.QTableWidgetItem(VOBs[3]))

            VOBs = cursor_VOBs.fetchone()
            linha += 1

        #Principal.LCD_Qtde_Registros.display(int(linha))
        Principal.repaint()

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante o carregamento da informações das VOBs - CarregaListaVOBs - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def Grava_Dados_VOB_Comunidade_Fabrica(VOB,COMUNIDADE,FABRICA):
    # Atualiza as informações de Comunidade e Fábrica da VOB
    BancodeDados.ExecutaComandoSQL(f"UPDATE VOBs SET COMUNIDADE = '{COMUNIDADE}' , FABRICA = '{FABRICA}' WHERE VOB = '{VOB}'")


def InsereDadosCompartilhamento(NOME_COMPART,CAMINHO_COMPART,GRUPO_COMPART):
    # Grava o caminho do compartilhamento da tabela de VOBs
    BancodeDados.ExecutaComandoSQL(f"UPDATE VOBs SET CAMINHO_COMPART = '{CAMINHO_COMPART}' WHERE VOB = '{NOME_COMPART}'")

    # Insere registro com nome do compartilhamento e o grupo
    BancodeDados.ExecutaComandoSQL(f"INSERT INTO COMPARTILHAMENTOS (NOME_COMPART, GRUPO_COMPART) VALUES ('{NOME_COMPART}','{GRUPO_COMPART}')")


def InsereDadosNETSHARE(NOME_COMPART, CONTEUDO_LINHA):
    # Grava a linha atual do arquivo NET_SHARE, para exibir pelo botão de detalhes (tela)
    BancodeDados.ExecutaComandoSQL(f"INSERT INTO NET_SHARE (NOME_COMPART , CONTEUDO_COMPART) VALUES ('{NOME_COMPART}','{CONTEUDO_LINHA}')")


def Habilita_Desabilita_Botoes(flag):
    # Habilita ou Desabilita os botões
    Principal.Btn_Atualiza_Base.setEnabled(flag)
    Principal.Btn_Gera_Planilha_Grupos.setEnabled(flag)
    Principal.Btn_Troca_Comunidade.setEnabled(flag)
    Principal.Btn_Troca_Fabrica.setEnabled(flag)
    Principal.Btn_Troca_GC.setEnabled(flag)
    Principal.Btn_Exibir_DESC.setEnabled(flag)
    Principal.Btn_Exibir_Compartilhamento.setEnabled(flag)
    Principal.repaint()


def LeDados_NETSHARE(arquivo):
    # Abre os arquivos com o resultado dos comandos 'NET SHARE' e grava na base de dados

    try:
        NOME_COMPART = ""
        CAMINHO_COMPART = ""
        GRUPO_COMPART = ""
        with open(caminho + f"\\Arquivos\\{arquivo}", encoding = 'UTF-8') as arquivo:
            for linha in arquivo:
                linha = linha.upper()
                linha = linha.strip()

                if linha.find("SHARE NAME") > -1:
                    NOME_COMPART = linha[18:-1]

                if linha.find("PATH") > -1:
                    CAMINHO_COMPART = linha[18:]

                if linha.find("CORPCAIXA") > -1:
                    GRUPO_COMPART = linha[int(linha.find("CORPCAIXA")+10):int(linha.find(","))]

                    InsereDadosCompartilhamento(NOME_COMPART,CAMINHO_COMPART,GRUPO_COMPART)

                InsereDadosNETSHARE(NOME_COMPART,linha)

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a analise do arquivo: '{arquivo}' - LeDados_NETSHARE - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def Btn_Atualiza_Base_click():
    # Executa os comandos, gera os arquivos e atualiza a base de dados
    # tamanho_arquivo = Path(sys.path[0] + "\\Arquivos\\LSVOB.txt").stat().st_size

    # Desabilita os botões até o final do processo
    Habilita_Desabilita_Botoes(False)

    try:
        # Limpa as tabelas
        BancodeDados.ExecutaComandoSQL(f"DELETE FROM VOBS")
        BancodeDados.ExecutaComandoSQL(f"DELETE FROM VOB_COMUNIDADE")
        BancodeDados.ExecutaComandoSQL(f"DELETE FROM COMPARTILHAMENTOS")
        BancodeDados.ExecutaComandoSQL(f"DELETE FROM NET_SHARE")

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a limpeza das tabelas - Btn_Atualiza_Base_click - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return

    # Arquivo LSVOB
    VOB = ""
    POSICAO_INICIAL = ""
    POSICAO_FINAL = ""
    try:
        print("Gerando arquivo LSVOB.txt ....")
        # Gera o arquivo com o LSVOB
        #os.system(f"cleartool lsvob >> {caminho}\\Arquivos\\LSVOB.txt")

        print("Abrindo arquivo LSVOB.txt ....")
        with open(f"{caminho}\\Arquivos\\LSVOB.txt", encoding = 'UTF-8') as Arquivo_LSVOB:
            for linha in Arquivo_LSVOB:
                # Para cada linha do arquivo LSVOB.txt, cria um comando DESC
                linha = linha.upper()

                POSICAO_INICIAL = linha.find("\\")
                POSICAO_FINAL = linha.find("\\\\")

                VOB = linha[linha.find("\\")+1 : linha.find("\\\\")].strip()

                #os.system(f"cleartool desc vob:\\{VOB} >> {caminho}\\Arquivos\\DESC.txt")
                #print(f"cleartool desc vob:\\{VOB} >> {caminho}\\Arquivos\\DESC.txt")
    
                SERVIDOR = linha[POSICAO_FINAL + 2:POSICAO_FINAL + 34].strip()
                if SERVIDOR.find("CADSVAPRNT002") > -1:
                    SERVIDOR = "SAO PAULO"
                if SERVIDOR.find("CBRSVAPRNT005") > -1:
                    SERVIDOR = "BRASILIA"
                if SERVIDOR.find("CADSVAPRNT009") > -1:
                    SERVIDOR = "RIO DE JANEIRO"
                if SERVIDOR.find("CBRSVAPRNT010") > -1:
                    SERVIDOR = "CEPEM"
                if SERVIDOR.find("CBRSVAPRNT013") > -1:
                    SERVIDOR = "LOTERIAS"
    
                BancodeDados.ExecutaComandoSQL(f"INSERT INTO VOBS (VOB,SERVIDOR) VALUES ('{VOB}','{SERVIDOR}')")
                Principal.repaint()

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a geração e leitura do arquivo LSVOB - Btn_Atualiza_Base_click - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        # Habilita os botões novamente
        Habilita_Desabilita_Botoes(True)
        return

    # DESC
    try:
        VOB = ""
        COMUNIDADE = ""
        FABRICA = ""
        print("Analisando arquivo DESC.txt ....")

        with open(f"{caminho}\\Arquivos\\DESC.txt", encoding = 'UTF-8') as arquivo:
            for linha in arquivo:
                linha = linha.upper()
                linha = linha.strip()
                if linha.find("VERSIONED") > -1:
                    if VOB != '':
                        Grava_Dados_VOB_Comunidade_Fabrica(VOB,COMUNIDADE,FABRICA)

                    VOB=linha[24:-1]
                    COMUNIDADE=''
                    FABRICA=''
                else:
                    if linha.find("G DF5222 CC_ARRECADACAO") > -1:
                        COMUNIDADE += " ARRECADACAO "
                    if linha.find("G DF5222 CC_CAMBIO") > -1:
                        COMUNIDADE += " CAMBIO "
                    if linha.find("G DF5222 CC_CANAIS_CLIENTES") > -1:
                        COMUNIDADE += " CANAIS_CLIENTES "
                    if linha.find("G DF5222 CC_CANAIS_INTERNO") > -1:
                        COMUNIDADE += " CANAIS_INTERNO "
                    if linha.find("G DF5222 CC_DADOS") > -1:
                        COMUNIDADE += " DADOS "
                    if linha.find("G DF5222 CC_CONTRATACOES") > -1:
                        COMUNIDADE += " CONTRATACOES "
                    if linha.find("G DF5222 CC_CONTROLADORIA") > -1:
                        COMUNIDADE += " CONTROLADORIA "
                    if linha.find("G DF5222 CC_CREDITO") > -1:
                        COMUNIDADE += " CREDITO "
                    if linha.find("G DF5222 CC_DEPOSITO") > -1:
                        COMUNIDADE += " DEPOSITO "
                    if linha.find("G DF5222 CC_ESTRUTURANTES_TI") > -1:
                        COMUNIDADE += " ESTRUTURANTES_TI "
                    if linha.find("G DF5222 CC_FINANCEIRO") > -1:
                        COMUNIDADE += " FINANCEIRO "
                    if linha.find("G DF5222 CC_FOMENTO_DJ") > -1:
                        COMUNIDADE += " FOMENTO_DJ "
                    if linha.find("G DF5222 CC_FUNDOS_GOVERNO") > -1:
                        COMUNIDADE += " FUNDOS_GOVERNO "
                    if linha.find("G DF5222 CC_HABITACAO") > -1:
                        COMUNIDADE += " HABITACAO "
                    if linha.find("G DF5222 CC_INSTITUCIONAL") > -1:
                        COMUNIDADE += " INSTITUCIONAL "
                    if linha.find("G DF5222 CC_LOTERIAS") > -1:
                        COMUNIDADE += " LOTERIAS "
                    if linha.find("G DF5222 CC_MEIOS_PAGAMENTO") > -1:
                        COMUNIDADE += " MEIOS_PAGAMENTO "
                    if linha.find("G DF5222 CC_OPERACOES_BANCARIAS") > -1:
                        COMUNIDADE += " OPERACOES_BANCARIAS "
                    if linha.find("G DF5222 CC_OPEN_BANKING") > -1:
                        COMUNIDADE += " OPEN_BANKING "
                    if linha.find("G DF5222 CC_PESSOAS") > -1:
                        COMUNIDADE += " PESSOAS "
                    if linha.find("G DF5222 CC_PROGRAMAS_SOCIAIS") > -1:
                        COMUNIDADE += " PROGRAMAS_SOCIAIS "
                    if linha.find("G DF5222 CC_RISCO") > -1:
                        COMUNIDADE += " RISCO "
                    if linha.find("G DF5222 CC_SEGURANCA") > -1:
                        COMUNIDADE += " SEGURANCA "
                    if linha.find("G DF5222 CC_CRM_CADASTRO") > -1:
                        COMUNIDADE += " CRM_CADASTRO "
                    if linha.find("G DF5222 CC_BRQ") > -1:
                        FABRICA += " BRQ "
                    if linha.find("G DF5222 CC_CAST") > -1:
                        FABRICA += " CAST "
                    if linha.find("G DF5222 CC_ESEC") > -1:
                        FABRICA += " ESEC "
                    if linha.find("G DF5222 CC_FIRST") > -1:
                        FABRICA += " FIRST "
                    if linha.find("G DF5222 CC_FOTON") > -1:
                        FABRICA += " FOTON "
                    if linha.find("G DF5222 CC_GLOBALWEB") > -1:
                        FABRICA += " GLOBALWEB "
                    if linha.find("G DF5222 CC_QINTESS") > -1:
                        FABRICA += " QINTESS "
                    if linha.find("G DF5222 CC_RESOURCE") > -1:
                        FABRICA += " RESOURCE "
                    if linha.find("G DF5222 CC_RJE") > -1:
                        FABRICA += " RJE "
                    if linha.find("G DF5222 CC_SPREAD") > -1:
                        FABRICA += " SPREAD "
                    if linha.find("G DF5222 CC_STEFANINI") > -1:
                        FABRICA += " STEFANINI "
                    if linha.find("G DF5222 CC_TIVIT") > -1:
                        FABRICA += " TIVIT "
                    if linha.find("G DF5222 CC_TTY") > -1:
                        FABRICA += " TTY "
                    if linha.find("G DF5222 CC_MAGNA") > -1:
                        FABRICA += " MAGNA "
                    if linha.find("CORPCAIXA\G CS7266") > -1:
                        COMUNIDADE = " MODELO ANTIGO - SP "
                        FABRICA = " MODELO ANTIGO - SP "
                    if linha.find("CORPCAIXA\G DF7390") > -1:
                        COMUNIDADE = " MODELO ANTIGO - BR "
                        FABRICA = " MODELO ANTIGO - BR "
                    if linha.find("CORPCAIXA\G RJ7265") > -1:
                        COMUNIDADE = " MODELO ANTIGO - RJ "
                        FABRICA = " MODELO ANTIGO - RJ "
                    if linha.find("CORPCAIXA\G DF5088") > -1:
                        COMUNIDADE = " GRUPOS DF5088 "
                        FABRICA = " GRUPOS DF5088 "

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a importação do arquivo DESC - Btn_Atualiza_Base_click - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        # Habilita os botões novamente
        Habilita_Desabilita_Botoes(True)
        return

    # Arquivo NETSHARE_BR
    print("Analisando arquivos NETSHARE_BR.txt ....")
    LeDados_NETSHARE('NET_SHARE_BR.txt')
    print("Analisando arquivos NETSHARE_SP.txt ....")
    LeDados_NETSHARE('NET_SHARE_SP.txt')
    print("Analisando arquivos NETSHARE_RJ.txt ....")
    LeDados_NETSHARE('NET_SHARE_RJ.txt')
    print("Analisando arquivos NETSHARE_CEPEM.txt ....")
    LeDados_NETSHARE('NET_SHARE_CEPEM.txt')

    MessageBox.Mensagem("Arquivos analisados com sucesso. As informações foram atualizadas na base local!!!","Informação",QMessageBox.Information,QMessageBox.Ok)
    CarregaListaVOBs('','','','')
    Preenche_Combos()

    # Habilita os botões novamente
    Habilita_Desabilita_Botoes(True)


def Btn_Filtro_click():
    if Principal.Cbo_Comunidades.currentIndex() > -1:
        COMUNIDADE = Principal.Cbo_Comunidades.currentText()

    if Principal.Cbo_Fabricas.currentIndex() > -1:
        FABRICA = Principal.Cbo_Fabricas.currentText()

    if Principal.Cbo_Servidores.currentIndex() > -1:
        SERVIDORES = Principal.Cbo_Servidores.currentText()

    if len(Principal.Txt_VOB.text()) > -1:
        VOB = Principal.Txt_VOB.text()

    CarregaListaVOBs(COMUNIDADE,FABRICA,SERVIDORES,VOB)


def Btn_Exibir_Compartilhamento_click(COMPART):
    if ( Principal.Tabela_VOBs.currentRow() > -1 ):
        COMPART = Principal.Tabela_VOBs.item(Principal.Tabela_VOBs.currentRow(),0).text()
    else:
        return

    CONTEUDO_NETSHARE = ""
    cursor_netshare = BancodeDados.ConsultaSQL(f"SELECT CONTEUDO_COMPART FROM NET_SHARE WHERE NOME_COMPART = '{COMPART}'")
    LINHAS_NETSHARE = cursor_netshare.fetchone()
    while LINHAS_NETSHARE:
        CONTEUDO_NETSHARE += str(LINHAS_NETSHARE[0]) + "\n"
        LINHAS_NETSHARE = cursor_netshare.fetchone()

    Principal.Txt_Detalhes.setPlainText(CONTEUDO_NETSHARE)
    Principal.Txt_Detalhes.setVisible(not Principal.Txt_Detalhes.isVisible())
    Principal.Btn_Sair_Detalhes.setVisible(not Principal.Btn_Sair_Detalhes.isVisible())
    

def Btn_Sair_Detalhes_click():
    Principal.Txt_Detalhes.setVisible(not Principal.Txt_Detalhes.isVisible())
    Principal.Btn_Sair_Detalhes.setVisible(not Principal.Btn_Sair_Detalhes.isVisible())


def GeraArquivoTXTGrupos():
    # Gera o arquivo TXT com as informações dos grupos, coletadas pelo NET SHARE
    try:
        with open(caminho + "\\Arquivos\Grupos_Clearcase.txt", mode="w", encoding="UTF-8") as arquivo_saida:
            # Le as comunidades
            cursos_comunidades = BancodeDados.ConsultaSQL("SELECT distinct(comunidade) FROM VOBs where COMUNIDADE IS NOT NULL AND COMUNIDADE <> '' ORDER BY COMUNIDADE")
            COMUNIDADES = cursos_comunidades.fetchone()
            while COMUNIDADES:
                # Para cada comunidade, busca os grupos
                cursor_grupos = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(GRUPO_COMPART) FROM COMPARTILHAMENTOS WHERE GRUPO_COMPART like '%{COMUNIDADES[0].strip()}%' ORDER BY GRUPO_COMPART")
                GRUPOS = cursor_grupos.fetchone()

                if GRUPOS:
                    arquivo_saida.write("\n")
                    arquivo_saida.write(f"******* {COMUNIDADES[0]} \n")

                while GRUPOS:
                    arquivo_saida.write(GRUPOS[0] + "\n")
                    GRUPOS = cursor_grupos.fetchone()

                COMUNIDADES = cursos_comunidades.fetchone()

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a geração do arquivo TXT dos grupos - GeraArquivoTXTGrupos - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def GeraPlanilhaGrupos_Excel():
    # Gera uma planilha com as informações dos grupos, coletadas pelo NET SHARE
    try:
        arquivo_saida = Workbook()
        #plan = arquivo_saida.active

        cursos_comunidades = BancodeDados.ConsultaSQL("SELECT distinct(comunidade) FROM VOBs where COMUNIDADE IS NOT NULL AND COMUNIDADE <> '' ORDER BY COMUNIDADE")
        COMUNIDADES = cursos_comunidades.fetchone()
        while COMUNIDADES:
            cursor_grupos = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(GRUPO_COMPART) FROM COMPARTILHAMENTOS WHERE GRUPO_COMPART like '%{COMUNIDADES[0].strip()}%' ORDER BY GRUPO_COMPART")
            GRUPOS = cursor_grupos.fetchone()

            if GRUPOS:
                NOME_COMUNIDADE = COMUNIDADES[0][0:30].strip()
                plan = arquivo_saida.create_sheet(title=NOME_COMUNIDADE)
                linha = 1

            while GRUPOS:
                plan[f"A{linha}"] = f"{GRUPOS[0].strip()}"
                linha += 1
                GRUPOS = cursor_grupos.fetchone()

            COMUNIDADES = cursos_comunidades.fetchone()

        # Remover a primeira aba (Sheet)
        aba_sheet = arquivo_saida['Sheet']
        arquivo_saida.remove(aba_sheet)

        # Salva a planilha
        arquivo_saida.save(caminho + '\\Arquivos\\Grupos_Clearcase.xlsx')

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a geração do arquivo XLS dos grupos - GeraPlanilhaGrupos_Excel - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def Btn_Gera_Arquivos_Grupos_click():
    try:
        # Desabilitar os botões até o final do processo
        Habilita_Desabilita_Botoes(False)

        # Verifica se o arquivo já existe, para removê-lo
        if os.path.exists(caminho + "\\Arquivos\\GRUPOS_CLEARCASE.txt"):
            os.remove(caminho + "\\Arquivos\\GRUPOS_CLEARCASE.txt")

        # Cria a pasta 'Arquivos', caso não exista
        if not os.path.exists(caminho + "\\Arquivos"):
            os.makedirs(caminho + "\\Arquivos")

        # Para cada comunidade, gravar os grupos no arquivo de saida
        GeraArquivoTXTGrupos()
        GeraPlanilhaGrupos_Excel()

        # Habilitar os botões novamente
        Habilita_Desabilita_Botoes(True)

        MessageBox.Mensagem("O arquivo com as informações dos grupos foi gerado com sucesso!!!","Informação",QMessageBox.Information,QMessageBox.Ok)

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a geração dos arquivos dos grupos - Btn_Gera_Arquivos_Grupos_click - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def Btn_Exibir_DESC_click():
    try:
        if ( Principal.Tabela_VOBs.currentRow() > -1 ):
            VOB = Principal.Tabela_VOBs.item(Principal.Tabela_VOBs.currentRow(),0).text()
        else:
            return

        # Cria a pasta 'Arquivos', caso não exista
        if not os.path.exists(caminho + "\\tmp"):
            os.makedirs(caminho + "\\tmp")

        saida = ""
        # Executa o comando CLEARTOOL DESC e grava o resultado num arquivo texto (temporário)
        os.system(f"cleartool desc vob:\\{VOB} >> {caminho}\\tmp\\DESC_{VOB}.txt")

        CONTEUDO_DESC = ""
        with open(f"{caminho}\\tmp\\DESC_{VOB}.txt", mode="r", encoding="ANSI") as Arquivo_DESC:
            for linha in Arquivo_DESC:
                CONTEUDO_DESC += linha

        Principal.Txt_Detalhes.setPlainText(CONTEUDO_DESC)
        Principal.Txt_Detalhes.setVisible(not Principal.Txt_Detalhes.isVisible())
        Principal.Btn_Sair_Detalhes.setVisible(not Principal.Btn_Sair_Detalhes.isVisible())

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a execução do comando 'DESC' - Btn_Exibir_DESC_click - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


# Verifica se esta sendo chamado por um interpretador python ou executavel
if sys.argv[0].find(".exe") > -1:
    caminho = sys.path[2]
else:
    caminho = sys.path[0]


# Abre uma instancia do TKinter para ler a resolução da tela
root = Tk()
monitor_width = root.winfo_screenwidth()
monitor_height = root.winfo_screenheight()
largura_tela = 1200
altura_tela = 800
borda_esquerda = int((monitor_width - largura_tela) / 2)
borda_superior = int((monitor_height - altura_tela) / 2)

# Cria a tela
app = QtWidgets.QApplication([])

# Lê o arquivo .ui
Principal = uic.loadUi(caminho + "\\Principal.ui")

# Configura a janela principal
Principal.setGeometry(borda_esquerda , borda_superior , largura_tela , altura_tela)
Principal.setWindowTitle("Manutenção Clearcase - CAIXA")

# Define os botões e suas funções
Principal.Btn_Atualiza_Base.clicked.connect(Btn_Atualiza_Base_click)
Principal.Btn_Filtro.clicked.connect(Btn_Filtro_click)
Principal.Btn_Sair_Detalhes.clicked.connect(Btn_Sair_Detalhes_click)
Principal.Btn_Gera_Planilha_Grupos.clicked.connect(Btn_Gera_Arquivos_Grupos_click)
Principal.Btn_Exibir_Compartilhamento.clicked.connect(Btn_Exibir_Compartilhamento_click)
Principal.Btn_Exibir_DESC.clicked.connect(Btn_Exibir_DESC_click)

# Define os objetos do detalhe como invisivel
Principal.Txt_Detalhes.setVisible(False)
Principal.Btn_Sair_Detalhes.setVisible(False)

# Abre a conexao do banco de dados
BancodeDados = SQLite(caminho + "\\Clearcase.db")

# Preenche os combos e o grid principal
Preenche_Combos()
CarregaListaVOBs('','','','')

# Exibe a tela
Principal.show()
app.exec()