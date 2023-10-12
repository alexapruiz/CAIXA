import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QMainWindow, QLabel,QGridLayout, QDesktopWidget
import cryptocode

# Importando os arquivos das funções comuns
sys.path.append('c:\\Projetos\\CAIXA\\Funcoes')
from MessageBox import MessageBox

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Funcoes import BancodeDados

def Atualiza_Usuario_Senha(usuario,senha):
    # Importa a biblioteca de criptofrafia
    # Abre o arquivo de conexao
    arquivo = open('conexao.txt',mode='w',encoding='UTF-8')
    chave_cripto = 'caixa'
    usuario_cripto = cryptocode.encrypt(usuario,chave_cripto)
    senha_cripto = cryptocode.encrypt(senha,chave_cripto)
    arquivo.write(f"usuario={usuario_cripto}\n")
    arquivo.write(f"senha={senha_cripto}\n")
    arquivo.close
    MessageBox.Mensagem("Dados da conexão atualizados com sucesso!!!!","Informação",QMessageBox.Warning,QMessageBox.Ok)


def Recupera_Usuario_Senha(arquivo_conexao):
    # Abre o arquivo conexao.txt e recupera o usuario e senha para conexao ao JTS
    arquivo = open(arquivo_conexao,mode='r',encoding='UTF-8')
    for linha in arquivo:
        if linha.find('usuario') > -1:
            usuario = cryptocode.decrypt(linha[8:], "caixa")
            if usuario == False:
                usuario = ''
            else:
                usuario = usuario.replace('\n','')
        if linha.find('senha') > -1:
            senha = cryptocode.decrypt(linha[6:], "caixa")
            if senha == False:
                senha=''
            else:
                senha = senha.replace('\n','')

    return usuario , senha, 'OK'


def GeraArquivos(navegador,url,arquivo):

    # Acessa a URL da consulta OSLC pra buscar as áreas de projetos
    navegador.get(url)
    dados = navegador.page_source

    # Grava os dados da página em um arquivo texto
    arquivo_saida = open(arquivo,mode='w',encoding='UTF-8')
    arquivo_saida.write(dados)
    arquivo_saida.close


def Busca_Areas(area1,area2,usuario, senha):

    # Abre o navegador
    navegador = webdriver.Chrome()

    # Acessa o Jazz
    navegador.get('https://gid.caixa:9443/ccm/web')

    # Efetua o login
    navegador.find_element_by_xpath('//*[@id="details-button"]').click()
    navegador.find_element_by_xpath('//*[@id="proceed-link"]').click()
    navegador.find_element_by_xpath('//*[@id="jazz_app_internal_LoginWidget_0_userId"]').send_keys(usuario)
    navegador.find_element_by_xpath('//*[@id="jazz_app_internal_LoginWidget_0_password"]').send_keys(senha)
    navegador.find_element_by_xpath('//*[@id="jazz_app_internal_LoginWidget_0"]/div[1]/div[1]/div[3]/form/button').click()

    # Verifica quais consultas executar (por ferramenta)
    if (area1 == 'rtc') or (area2 == 'rtc'):
        GeraArquivos(navegador,'https://gid.caixa:9443/ccm/process/project-areas','areas_rtc.txt')
    if (area1 == 'rdng') or (area2 == 'rdng'):
        GeraArquivos(navegador,'https://gid.caixa:9443/rm/process/project-areas','areas_rdng.txt')
    if (area1 == 'rqm') or (area2 == 'rqm'):
        GeraArquivos(navegador,'https://gid.caixa:9443/qm/process/project-areas','areas_rqm.txt')

    navegador.quit

def RetornaAreaLimpa(area_suja):
    # Remover (Gerenciamento de XXXXX)
    tamanho_sufixo = len(area_suja) - area_suja.find(':')
    sufixo = area_suja[-tamanho_sufixo:]
    pesquisa_gerenc = area_suja.find('Gerenc')
    if pesquisa_gerenc > -1:
        area_limpa = area_suja[:pesquisa_gerenc-2]
        return area_limpa + sufixo
    else:
        return area_suja
    

def ComparaListas(arquivo1, arquivo2):

    # Lê arquivo1
    arq1 = open(f"areas_{arquivo1}.txt", mode="r", encoding="UTF-8")
    arq2 = open(f"areas_{arquivo2}.txt", mode="r", encoding="UTF-8")

    lista1 = []
    for linha in arq1:
        # Só considerar as linhas que tem a string 'jp06:project-area jp06:name'
        if (linha.find('jp06:project-area jp06:name') > -1) and (linha[34:36] == 'SI'):
            lista1.append(linha[34:-3] + ':' + arquivo1)

    arq1.close

    lista2 = []
    for linha in arq2:
        # Só considerar as linhas que tem a string 'jp06:project-area jp06:name'
        if (linha.find('jp06:project-area jp06:name') > -1) and (linha[34:36] == 'SI'):
            lista2.append(linha[34:-3] + ':' + arquivo2)

    arq2.close

    lista1.sort()
    lista2.sort()
    lista_completa = lista1 + lista2
    lista_completa.sort()

    arq_saida = open('saida.csv' , mode='w' , encoding='UTF-8')
    arq_saida.write(f"{arquivo1} ; {arquivo2}")
    arq_saida.write('\n')
    indice = 0
    total = len(lista_completa)
    tamanho_arq1 = len(arquivo1) + 1
    tamanho_arq2 = len(arquivo2) + 1
    while indice < total -1:
        area_limpa1 = RetornaAreaLimpa(lista_completa[indice])
        area_limpa2 = RetornaAreaLimpa(lista_completa[indice + 1])

        #if lista_completa[indice][:5] == lista_completa[indice + 1][:5]:
        if area_limpa1[:area_limpa1.find(':')] == area_limpa2[:area_limpa2.find(':')]:
            if ((lista_completa[indice].find(f"{arquivo1}") > -1) and (lista_completa[indice + 1].find(f"{arquivo2}") > -1)):
                # Encontrou 2 áreas correlatas, sendo a área do RTC com índice menor
                arq_saida.write(lista_completa[indice][:-tamanho_arq1] + ';' + lista_completa[indice + 1][:-tamanho_arq2])
                arq_saida.write('\n')
                indice += 1
            elif ((lista_completa[indice].find(f"{arquivo2}") > -1) and (lista_completa[indice + 1].find(f"{arquivo1}") > -1)):
                # Encontrou 2 áreas correlatas, sendo a área do RDNG com índice menor
                arq_saida.write(lista_completa[indice + 1][:-tamanho_arq1] + ';' + lista_completa[indice][:-tamanho_arq2])
                arq_saida.write('\n')
                indice += 1
            else:
                # Areas com nomes 'parecidos', mas são da mesma ferramenta
                if (lista_completa[indice].find(f"{arquivo1}") > -1):
                    arq_saida.write(lista_completa[indice][:-tamanho_arq1] + ';')
                    arq_saida.write('\n')
                elif (lista_completa[indice].find(f"{arquivo2}") > -1):
                    arq_saida.write(';' + lista_completa[indice][:-tamanho_arq2])
                    arq_saida.write('\n')
        else:
            if (lista_completa[indice].find(f"{arquivo1}") > -1):
                # Area 1 sem correlata, imprime sozinha
                arq_saida.write(lista_completa[indice][:-tamanho_arq1] + ';')
                arq_saida.write('\n')
            elif (lista_completa[indice].find(f"{arquivo2}") > -1):
                # Area 2 sem correlata, imprime sozinha
                arq_saida.write(';' + lista_completa[indice][:-tamanho_arq2])
                arq_saida.write('\n')
            else:
                print('Erro!!')

        indice += 1

    return 'OK'


def Btn_Comparar_Click():
    # Verifica se os 2 combos possuem itens válidos selecionados
    if ( Tela.Cbo_Ferramenta_1.currentText() == '' or Tela.Cbo_Ferramenta_2.currentText() == ''):
        MessageBox.Mensagem("É necessário informar as ferramentas!!!","Aviso",QMessageBox.Warning,QMessageBox.Ok)
    elif ( Tela.Cbo_Ferramenta_1.currentText() == Tela.Cbo_Ferramenta_2.currentText()):
        # Verifica se foi selecionada a mesma ferramenta em ambos os combos
        MessageBox.Mensagem("É necessário informar ferramentas diferentes para comparação!!!","Aviso",QMessageBox.Warning,QMessageBox.Ok)
    else:
        usuario , senha , status = Recupera_Usuario_Senha('conexao.txt')
        if status == 'OK':
            Busca_Areas(Tela.Cbo_Ferramenta_1.currentText().lower(),Tela.Cbo_Ferramenta_2.currentText().lower(),Tela.TxtUsuario.text(),Tela.TxtSenha.text())
            retorno = ComparaListas(Tela.Cbo_Ferramenta_1.currentText().lower(),Tela.Cbo_Ferramenta_2.currentText().lower())
            if retorno == 'OK':
                MessageBox.Mensagem("Arquivo Saida.csv gerado com sucesso!!!!","Informação",QMessageBox.Warning,QMessageBox.Ok)


def Btn_Atualizar_Usuario_e_Senha():
    # Verifica se o usuário e a senha foram informados
    if ( (Tela.TxtUsuario.text()) and (Tela.TxtSenha.text()) ):
        Atualiza_Usuario_Senha(Tela.TxtUsuario.text(),Tela.TxtSenha.text())


def Exibir_Esconder_Senha():
    if Tela.chkSenha.checkState() == 0:
        Tela.TxtSenha.setEchoMode(Tela.TxtSenha.Password)
    else:
        Tela.TxtSenha.setEchoMode(Tela.TxtSenha.Normal)
    


# Cria a tela
app = QtWidgets.QApplication([])

# Lê o arquivo .ui
Tela = uic.loadUi("Tela.ui")

# Configura a janela principal
Tela.setWindowTitle("Comparador de Areas de Projeto")
qtRectangle = Tela.frameGeometry()
centerPoint = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(centerPoint)
Tela.move(qtRectangle.topLeft())

lista_ferramentas = ["","RTC","RDNG","RQM"]
Tela.Cbo_Ferramenta_1.addItems(lista_ferramentas)
Tela.Cbo_Ferramenta_2.addItems(lista_ferramentas)
Tela.TxtSenha.setEchoMode(Tela.TxtSenha.Password)

# Busca o usuario e a senha, armazenados em conexao.txt
usuario, senha, retorno = Recupera_Usuario_Senha('conexao.txt')
if retorno == 'OK':
    Tela.TxtUsuario.insert(usuario)
    Tela.TxtSenha.insert(senha)

# Define as funções que vão implementar os botões
Tela.Btn_Comparar.clicked.connect(Btn_Comparar_Click)
Tela.Btn_Atualizar.clicked.connect(Btn_Atualizar_Usuario_e_Senha)
Tela.chkSenha.stateChanged.connect(Exibir_Esconder_Senha)


# Exibe a tela
Tela.show()
app.exec()