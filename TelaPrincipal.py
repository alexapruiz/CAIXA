#Importando as bibliotecas
import os
import sys
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox , QFileDialog
from Analisa_TXT import Analisa_TXT
from Demandas import Demandas
from Areas_Projeto import Areas_Projeto
from RDNG import RDNG

#Importando os arquivos das funções comuns
sys.path.append('c:\\Projetos\\Python\\Funcoes')
from MessageBox import MessageBox


def CarregaListas():
    # Abre arquivo com lista de comunidades
    with open('comunidades.txt', mode='r', encoding='UTF-8') as comunidades:
        for linha in comunidades:
            Tela_Principal.Lista_Comunidades.addItem(linha[:-1])

    Tela_Principal.Lista_Comunidades.setSelectionMode(2)


# Define o comportamento do botão de seleção de arquivo de entrada
def Btn_Select_Arquivo_Entrada_click():
    caminho = QFileDialog.getOpenFileName(Tela_Principal,"Abrir Arquivo",sys.path[0],"Todos os arquivos (*.*) ;; Arquivos Excel (*.xlsx *.xls *.csv) ;; Arquivos Text (*.txt)")
    Tela_Principal.Txt_Arquivo_Entrada.setPlainText(str(caminho[0]))


def Btn_Select_Arquivo_Saida_click():
    caminho = QFileDialog.getSaveFileName(Tela_Principal,"Salvar Como...",sys.path[0])
    Tela_Principal.Txt_Arquivo_Saida.setPlainText(str(caminho[0]))


def Verifica_Entrada_Saida(tipo_validacao):
    if tipo_validacao == 'entrada':
        if Tela_Principal.Txt_Arquivo_Entrada.toPlainText() == '':
            MessageBox.Mensagem("É necessário informar o arquivo de entrada!!!","Aviso",QMessageBox.Warning,QMessageBox.Ok)
            return False
    elif tipo_validacao == 'saida':
        if Tela_Principal.Txt_Arquivo_Saida.toPlainText() == '':
            MessageBox.Mensagem("É necessário informar o arquivo de saída!!!","Aviso",QMessageBox.Warning,QMessageBox.Ok)
            return False
    elif tipo_validacao == 'entrada_saida':
        if (Tela_Principal.Txt_Arquivo_Entrada.toPlainText() == '') or (Tela_Principal.Txt_Arquivo_Saida.toPlainText() == ''):
            MessageBox.Mensagem("É necessário informar os arquivos de entrada e saída!!!","Aviso",QMessageBox.Warning,QMessageBox.Ok)
            return False
    
    return True


# Frame - Analisa Arquivos TXT
def Btn_Analisa_NETSHARE_click():
    if Verifica_Entrada_Saida('entrada_saida') == True:
        Analisa_TXT.Le_NETSHARE(Tela_Principal.Txt_Arquivo_Entrada.toPlainText(),Tela_Principal.Txt_Arquivo_Saida.toPlainText())


def Btn_Extrai_Areas_Report_click():
    if Verifica_Entrada_Saida('entrada') == True:
        Analisa_TXT.Extrai_Areas_Report(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())


def Btn_Analisa_Desc_FLevel_DbSchema_click():
    if Verifica_Entrada_Saida('entrada') == True:
        arquivo_saida = Analisa_TXT.Le_DESC_Flevel_schemadb(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())
        Tela_Principal.Txt_Arquivo_Saida.setPlainText(arquivo_saida)
        MessageBox.Mensagem("Arquivo com resultado da pesquisa de função gerado com sucesso!!!!","Informação",QMessageBox.Information,QMessageBox.Ok)


def Btn_Analisa_Desc_click():
    if Verifica_Entrada_Saida('entrada_saida') == True:
        Analisa_TXT.Le_DESC(Tela_Principal.Txt_Arquivo_Entrada.toPlainText(),Tela_Principal.Txt_Arquivo_Saida.toPlainText())


def Btn_Analisa_Dir_Gera_Comandos_click():
    if Verifica_Entrada_Saida('entrada') == True:
        arquivo_saida = Analisa_TXT.Le_dir_gera_comando(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())


def Btn_Analisa_Dir_Caso_Desenv_click():
    if Verifica_Entrada_Saida('entrada') == True:
        arquivo_saida = Analisa_TXT.Le_SaidaDir_Caso_Desenv(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())


def Btn_Tamanho_VOBs_click():
    if Verifica_Entrada_Saida('entrada') == True:
        arquivo_saida = Analisa_TXT.Gera_Arquivo_Tamanho_VOBs(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())
        Tela_Principal.Txt_Arquivo_Saida.setPlainText(arquivo_saida)
        MessageBox.Mensagem("Arquivo '" + arquivo_saida + "' gerado com sucesso!!!!","Informação",QMessageBox.Information,QMessageBox.Ok)


def Btn_Analisa_LSVOB_click():
    if Verifica_Entrada_Saida('entrada') == True:
        arquivo_saida = Analisa_TXT.Gera_Arquivo_VOBs_Servidor(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())
        Tela_Principal.Txt_Arquivo_Saida.setPlainText(arquivo_saida)
        MessageBox.Mensagem("Arquivo '" + arquivo_saida + "' gerado com sucesso!!!!","Informação",QMessageBox.Information,QMessageBox.Ok)


# Frame - Demandas
def Btn_Demandas_click():
    if Verifica_Entrada_Saida('entrada') == True:
        Arquivo_saida = Demandas.Calcula_USTs_Demandas(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())

        #Verifica se o retorno é um erro de codificação do arquivo
        if (Arquivo_saida == "UnicodeDecodeError"):
            MessageBox.Mensagem("Você precisa salvar o arquivo de entrada com a codificação 'UTF-8'","Aviso",QMessageBox.Warning,QMessageBox.Ok)
        elif (Arquivo_saida == "File Not Found"):
            MessageBox.Mensagem("O arquivo informado não foi localizado","Aviso",QMessageBox.Warning,QMessageBox.Ok)
        else:
            MessageBox.Mensagem("Arquivo '" + Arquivo_saida + "' gerado com sucesso!!!!","Informação",QMessageBox.Information,QMessageBox.Ok)
            Tela_Principal.Txt_Arquivo_Saida.setPlainText(str(Arquivo_saida))


def Btn_Calcula_SLAs_click():
    # Calcula os SLA's com base no último arquivo importado
    if Verifica_Entrada_Saida('entrada') == True:
        retorno = Demandas.Calcula_SLAs(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())

        #Verifica se o retorno é um erro de codificação do arquivo
        if retorno != 'Dados dos SLAs gerados com sucesso':
            if (retorno == "UnicodeDecodeError"):
                MessageBox.Mensagem("Você precisa salvar o arquivo de entrada com a codificação 'UTF-8'","Aviso",QMessageBox.Warning,QMessageBox.Ok)
            elif (retorno == "File Not Found"):
                MessageBox.Mensagem("O arquivo informado não foi localizado","Aviso",QMessageBox.Warning,QMessageBox.Ok)
            else:
                MessageBox.Mensagem(retorno,"Aviso",QMessageBox.Warning,QMessageBox.Ok)
        else:
            MessageBox.Mensagem(retorno,"Informação",QMessageBox.Information,QMessageBox.Ok)


# Frame - RDNG
def Btn_RDNG_Remocao_Links_click():
    if Verifica_Entrada_Saida('entrada') == True:
        #Lê a URL do arquivo de entrada
        RDNG.Gera_URLs_Remocao_Links(Tela_Principal.Txt_Arquivo_Entrada.toPlainText())


def Btn_RDNG_Gerar_Lista_Areas_click():
    # Executa a função que compara a lista de áreas
    retorno = RDNG.Gera_Lista_Areas()
    if retorno != 'Ok':
        MessageBox.Mensagem("Ocorreu um erro ao gerar a lista de áreas do RDNG","Aviso",QMessageBox.Warning,QMessageBox.Ok)
    else:
        MessageBox.Mensagem("Arquivo com áreas do RDNG, gerado com sucesso!!","Informação",QMessageBox.Information,QMessageBox.Ok)


#Cria a tela
app = QtWidgets.QApplication([])

#Lê o arquivo .ui
Tela_Principal = uic.loadUi("TelaPrincipal.ui")

#Configura a janela principal
#Tela_Principal.setGeometry(400,200,620,200)
Tela_Principal.setWindowTitle("Automatizador de Rotinas - CAIXA")

#Define as funções que serão chamadas nos clicks dos botões
#Botoões de pesquisa de arquivos / caminho de saída
Tela_Principal.Btn_Select_Arquivo_Entrada.clicked.connect(Btn_Select_Arquivo_Entrada_click)
Tela_Principal.Btn_Select_Arquivo_Saida.clicked.connect(Btn_Select_Arquivo_Saida_click)

#Botões do frame 'Demandas'
Tela_Principal.Btn_Demandas.clicked.connect(Btn_Demandas_click)
Tela_Principal.Btn_Calcula_SLAs.clicked.connect(Btn_Calcula_SLAs_click)


#Botões do frame 'RDNG'
Tela_Principal.Btn_RDNG_Remocao_Links.clicked.connect(Btn_RDNG_Remocao_Links_click)
Tela_Principal.Btn_RDNG_Gerar_Lista_Areas.clicked.connect(Btn_RDNG_Gerar_Lista_Areas_click)


#Botões do frame 'Analisa Arquivos TXT'
Tela_Principal.Btn_Analisa_NETSHARE.clicked.connect(Btn_Analisa_NETSHARE_click)
Tela_Principal.Btn_Analisa_Desc.clicked.connect(Btn_Analisa_Desc_click)
Tela_Principal.Btn_Extrai_Areas_Report.clicked.connect(Btn_Extrai_Areas_Report_click)
Tela_Principal.Btn_Analisa_Dir_Gera_Comandos.clicked.connect(Btn_Analisa_Dir_Gera_Comandos_click)
Tela_Principal.Btn_Analisa_Desc_FLevel_DbSchema.clicked.connect(Btn_Analisa_Desc_FLevel_DbSchema_click)
Tela_Principal.Btn_Analisa_Dir_Caso_Desenv.clicked.connect(Btn_Analisa_Dir_Caso_Desenv_click)
Tela_Principal.Btn_Tamanho_VOBs.clicked.connect(Btn_Tamanho_VOBs_click)
Tela_Principal.Btn_Analisa_LSVOB.clicked.connect(Btn_Analisa_LSVOB_click)


#Carrega lista de comunidades
CarregaListas()


#Exibe a tela
Tela_Principal.show()
app.exec()