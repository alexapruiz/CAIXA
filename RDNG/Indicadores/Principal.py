import sys
from tkinter import *
from PyQt5 import uic , QtWidgets #, Qt
from PyQt5.QtWidgets import QMessageBox , QFileDialog
from Manutencao import Manutencao

# Importando os arquivos das funções comuns
sys.path.append('c:\\Projetos\\CAIXA\\Funcoes')
from MessageBox import MessageBox
from BancodeDados import SQLite


# Define o comportamento do botão de seleção de arquivo de entrada
def Btn_Select_Arquivo_click():
    caminho = QFileDialog.getOpenFileName(Tela_RDNG_Indica,"Abrir Arquivo",sys.path[0], " Arquivos Excel (*.xlsx *.xls ) ;; Todos os arquivos (*.*)")
    Tela_RDNG_Indica.Txt_Arquivo_Entrada.setPlainText(str(caminho[0]))


def Preenche_Combos():
    # Busca as informações sobre comunidades, fábricas e servidores para o preenchimento dos combos
    try:
        # Combo Comunidades
        Tela_RDNG_Indica.Cbo_Comunidades.clear()
        Tela_RDNG_Indica.Cbo_Comunidades_Evolucao.clear()

        Tela_RDNG_Indica.Cbo_Comunidades.addItem('')
        Tela_RDNG_Indica.Cbo_Comunidades_Evolucao.addItem('')
        cursor_comunidades = BancodeDados.ConsultaSQL("SELECT DISTINCT(COMUNIDADE) FROM INDICADORES_RDNG ORDER BY COMUNIDADE")
        COMUNIDADES = cursor_comunidades.fetchone()
        while COMUNIDADES:
            Tela_RDNG_Indica.Cbo_Comunidades.addItem(COMUNIDADES[0])
            Tela_RDNG_Indica.Cbo_Comunidades_Evolucao.addItem(COMUNIDADES[0])
            COMUNIDADES = cursor_comunidades.fetchone()

        # Combo de Datas de Importacao
        Tela_RDNG_Indica.Cbo_Data_Importacao.clear()
        Tela_RDNG_Indica.Cbo_Data_Importacao_Manut.clear()
        cursor_datas = BancodeDados.ConsultaSQL("SELECT DISTINCT(DATA_IMPORTACAO) FROM INDICADORES_RDNG ORDER BY DATA_IMPORTACAO")
        DATAS = cursor_datas.fetchone()
        while DATAS:
            Tela_RDNG_Indica.Cbo_Data_Importacao.addItem(str(DATAS[0])[6:] + "/" + str(DATAS[0])[4:6] + "/" + str(DATAS[0])[:4])
            Tela_RDNG_Indica.Cbo_Data_Importacao_Manut.addItem(str(DATAS[0])[6:] + "/" + str(DATAS[0])[4:6] + "/" + str(DATAS[0])[:4])
            DATAS = cursor_datas.fetchone()

        # Seleciona como padrão a data mais recente
        Tela_RDNG_Indica.Cbo_Data_Importacao.setCurrentIndex(Tela_RDNG_Indica.Cbo_Data_Importacao.count()-1)

    except Exception as erro:
        print(f"Ocorreu um erro durante o preenchimento dos combos - Preenche_Combos - [' {erro}' ]")
        return

    # Preenche o combo de Ferramenta / Indicador
    Tela_RDNG_Indica.Cbo_Indicador.clear()
    Tela_RDNG_Indica.Cbo_Indicador.addItem("")
    Tela_RDNG_Indica.Cbo_Indicador.addItem("RDNG")
    Tela_RDNG_Indica.Cbo_Indicador.addItem("Clearcase")
    Tela_RDNG_Indica.Cbo_Indicador.addItem("Justificativa")


def Btn_Atualiza_Base_click():
    if Tela_RDNG_Indica.Txt_Arquivo_Entrada.toPlainText() == "":
        MessageBox.Mensagem("É necessário informar o arquivo de entrada!!!","Aviso",QMessageBox.Warning,QMessageBox.Ok)
        return

    # Zera o grid na tela
    Tela_RDNG_Indica.Tabela_HUs.setRowCount(0)
    Tela_RDNG_Indica.LCD_Qtde_Registros.display(0)
    Tela_RDNG_Indica.repaint()

    manut.ImportaPlanilha(Tela_RDNG_Indica.Txt_Arquivo_Entrada.toPlainText())
    
    # Recarrega os combos
    Preenche_Combos()

    # Limpa o campo do arquivo de origem
    Tela_RDNG_Indica.Txt_Arquivo_Entrada.setPlainText("")

    # Exibe a mensagem do final do processo
    MessageBox.Mensagem("Dados importados e Indicadores Calculados com Sucesso!!!","Informação",QMessageBox.Information,QMessageBox.Ok)


def CarregaListaHUs(data_importacao,comunidade,indicador, hus_corretas, hus_inconsistentes):
    try:
        # Carrega as VOBs e demais informacoes no grid principal
        Tela_RDNG_Indica.Tabela_HUs.setColumnCount(5)
        Tela_RDNG_Indica.Tabela_HUs.setColumnWidth(0,200)
        Tela_RDNG_Indica.Tabela_HUs.setColumnWidth(1,200)
        Tela_RDNG_Indica.Tabela_HUs.setColumnWidth(2,200)
        Tela_RDNG_Indica.Tabela_HUs.setColumnWidth(3,200)
        Tela_RDNG_Indica.Tabela_HUs.setColumnWidth(4,200)

        CLAUSULA_COMUNIDADE = ""
        CLAUSULA_INDICADOR = ""
        # Verifica se a funcao foi chamada com algum parametro
        if len(comunidade) > 0:
            CLAUSULA_COMUNIDADE = f" AND COMUNIDADE = '{comunidade}'"

        if len(indicador) > 0:
            if hus_corretas == False and hus_inconsistentes == False:
                MessageBox.Mensagem(f"É necessário selecionar uma opção entre 'HUs Corretas' ou 'HUs Inconsistentes' !!!","Aviso sobre filtro",QMessageBox.Information,QMessageBox.Ok)
                return
            else:
                if indicador == 'RDNG':
                    if hus_corretas == True:
                        CLAUSULA_INDICADOR = "AND QTDE_NAO_RASTREADO = '1'"
                    else:
                        CLAUSULA_INDICADOR = "AND QTDE_NAO_RASTREADO <> '1'"

                if indicador == 'Clearcase':
                    if hus_corretas == True:
                        CLAUSULA_INDICADOR = "AND INDICADOR_CAMINHO_CC_INVALIDO = '1'"
                    else:
                        CLAUSULA_INDICADOR = "AND INDICADOR_CAMINHO_CC_INVALIDO <> '1'"

                if indicador == 'Justificativa':
                    if hus_corretas == True:
                        CLAUSULA_INDICADOR = "AND INDICADOR_JUSTIFICATIVA = '1'"
                    else:
                        CLAUSULA_INDICADOR = "AND INDICADOR_JUSTIFICATIVA <> '1'"

        # Carrega a lista de VOBs de acordo com o filtro selecionado
        ComandoSQL = f"SELECT COMUNIDADE, SQUAD, FSW, SISTEMA, HU FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO = '{data_importacao}' "
        ComandoSQL += CLAUSULA_COMUNIDADE
        ComandoSQL += CLAUSULA_INDICADOR
        ComandoSQL += " ORDER BY DATA_IMPORTACAO , COMUNIDADE , SQUAD , FSW , SISTEMA , HU"
        cursor_HUs = BancodeDados.ConsultaSQL(ComandoSQL)

        HUs = cursor_HUs.fetchone()
        linha=0
        Tela_RDNG_Indica.Tabela_HUs.setRowCount(0)

        while HUs:
            Tela_RDNG_Indica.Tabela_HUs.setRowCount(int(linha+1))

            Tela_RDNG_Indica.Tabela_HUs.setItem(linha,0,QtWidgets.QTableWidgetItem(HUs[0]))
            Tela_RDNG_Indica.Tabela_HUs.setItem(linha,1,QtWidgets.QTableWidgetItem(HUs[1]))
            Tela_RDNG_Indica.Tabela_HUs.setItem(linha,2,QtWidgets.QTableWidgetItem(HUs[2]))
            Tela_RDNG_Indica.Tabela_HUs.setItem(linha,3,QtWidgets.QTableWidgetItem(HUs[3]))
            Tela_RDNG_Indica.Tabela_HUs.setItem(linha,4,QtWidgets.QTableWidgetItem(str(HUs[4])))

            HUs = cursor_HUs.fetchone()
            linha += 1

        Tela_RDNG_Indica.LCD_Qtde_Registros.display(int(linha))

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante o carregamento da informações das HUs na tabela - CarregaListaHUs - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def Btn_Filtro_click():
    # Verifica os filtros e carrega a lista de HUs
    Tela_RDNG_Indica.Tabela_HUs.setRowCount(0)

    COMUNIDADE = ""
    INDICADOR = ""
    HUS_CORRETAS = False
    HUS_INCONSISTENTES = False

    if Tela_RDNG_Indica.Cbo_Comunidades.currentIndex() > -1:
        COMUNIDADE = Tela_RDNG_Indica.Cbo_Comunidades.currentText()

    if Tela_RDNG_Indica.Cbo_Indicador.currentIndex() > -1:
        INDICADOR = Tela_RDNG_Indica.Cbo_Indicador.currentText()

    if Tela_RDNG_Indica.Rd_HUs_Corretas.isChecked() == True:
        HUS_CORRETAS = True

    if Tela_RDNG_Indica.Rd_HUs_Inconsistentes.isChecked() == True:
        HUS_INCONSISTENTES = True


    CarregaListaHUs(str(Tela_RDNG_Indica.Cbo_Data_Importacao.currentText())[6:]+str(Tela_RDNG_Indica.Cbo_Data_Importacao.currentText())[3:5]+str(Tela_RDNG_Indica.Cbo_Data_Importacao.currentText())[:2] , COMUNIDADE, INDICADOR, HUS_CORRETAS, HUS_INCONSISTENTES)


def BuscaValoresIndicadores(data_importacao,comunidade):
    # Preenche o quadro com os valores dos indicadores
    FILTRO_DATA = ""
    FILTRO_DATA = f"AND DATA_IMPORTACAO = '{data_importacao}'"
    FILTRO_COMUNIDADE = ""
    if len(comunidade) > 0:
        FILTRO_COMUNIDADE = f"AND COMUNIDADE = '{comunidade}'"
    try:
        # Indicador 1 - Só Check Combo, sem link
        ComandoSQL = f"SELECT COUNT(DISTINCT(HU)) AS 'SO_CHECK_COMBO_SEM_LINK' FROM INDICADORES_RDNG WHERE QTDE_NAO_RASTREADO = '1' {FILTRO_DATA} {FILTRO_COMUNIDADE}"
        cursor_Indicador1 = BancodeDados.ConsultaSQL(ComandoSQL)
        indicador1 = cursor_Indicador1.fetchone()
        if indicador1:
            RETORNO_INDICADOR1 = indicador1[0]

        # Indicador 2 - Caminho CC Válido
        ComandoSQL = f"SELECT COUNT(DISTINCT(HU)) AS 'INDICADOR_CAMINHO_CC_INVALIDO' FROM INDICADORES_RDNG WHERE INDICADOR_CAMINHO_CC_INVALIDO = '1' AND DATA_IMPORTACAO = '{data_importacao}' {FILTRO_COMUNIDADE}"
        cursor_Indicador2 = BancodeDados.ConsultaSQL(ComandoSQL)
        indicador2 = cursor_Indicador2.fetchone()
        if indicador2:
            RETORNO_INDICADOR2 = indicador2[0]

        # Indicador 3 - Justificativa
        ComandoSQL = f"SELECT COUNT(DISTINCT(HU)) AS 'INDICADOR_JUSTIFICATIVA' FROM INDICADORES_RDNG WHERE INDICADOR_JUSTIFICATIVA = '1' AND DATA_IMPORTACAO = '{data_importacao}' {FILTRO_COMUNIDADE}"
        cursor_Indicador3 = BancodeDados.ConsultaSQL(ComandoSQL)
        indicador3 = cursor_Indicador3.fetchone()
        if indicador3:
            RETORNO_INDICADOR3 = indicador3[0]

        # Total de registros
        ComandoSQL = f"SELECT COUNT(DISTINCT(HU)) AS 'TOTAL_REGISTROS' FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO = '{data_importacao}' {FILTRO_COMUNIDADE}"
        cursor_Total = BancodeDados.ConsultaSQL(ComandoSQL)
        total = cursor_Total.fetchone()
        if total:
            TOTAL = total[0]

        return RETORNO_INDICADOR1 , RETORNO_INDICADOR2 , RETORNO_INDICADOR3 , TOTAL

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante a busca de valores dos indicadores - BuscaValoresIndicadores - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def CarregaDadosEvolucao(comunidade):
    # Monta a tabela com as informações sobre a evolução dos indicadores
    try:
        # Configura os LABELs dos grids
        if len(comunidade) == 0:
            Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Resumo.setText("Resumo Geral")
        else:
            Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Resumo.setText(f"Resumo - {comunidade}")

        # Configura a tabela de evolução (resumo)
        Tela_RDNG_Indica.Tabela_Evolucao.setColumnWidth(0,170)
        Tela_RDNG_Indica.Tabela_Evolucao.setColumnWidth(1,250)
        Tela_RDNG_Indica.Tabela_Evolucao.setColumnWidth(2,140)
        Tela_RDNG_Indica.Tabela_Evolucao.setColumnWidth(3,140)
        Tela_RDNG_Indica.Tabela_Evolucao.setColumnWidth(4,0)

        # Cria os títulos das colunas
        Tela_RDNG_Indica.Tabela_Evolucao.setItem(0,0,QtWidgets.QTableWidgetItem("Indicador"))
        Tela_RDNG_Indica.Tabela_Evolucao.setItem(0,1,QtWidgets.QTableWidgetItem("Item"))
        Tela_RDNG_Indica.Tabela_Evolucao.setItem(0,4,QtWidgets.QTableWidgetItem("Evolução"))

        # Preenche as linhas
        Tela_RDNG_Indica.Tabela_Evolucao.setItem(1,0,QtWidgets.QTableWidgetItem("RDNG"))
        Tela_RDNG_Indica.Tabela_Evolucao.setItem(1,1,QtWidgets.QTableWidgetItem("Só está checado o Combo, sem link"))

        Tela_RDNG_Indica.Tabela_Evolucao.setItem(2,0,QtWidgets.QTableWidgetItem("Clearcase"))
        Tela_RDNG_Indica.Tabela_Evolucao.setItem(2,1,QtWidgets.QTableWidgetItem("Caminho do Clearcase Inválido"))

        Tela_RDNG_Indica.Tabela_Evolucao.setItem(3,0,QtWidgets.QTableWidgetItem("Justificativa"))
        Tela_RDNG_Indica.Tabela_Evolucao.setItem(3,1,QtWidgets.QTableWidgetItem("Total de Justificativas"))
    
        # Pesquisa as datas disponíveis -> Preciso selecionar as ultimas 2 datas de importação, trazendo a mais antiga primeiro
        cursor_Datas = BancodeDados.ConsultaSQL("SELECT DISTINCT(DATA_IMPORTACAO) FROM INDICADORES_RDNG WHERE DATA_IMPORTACAO IN (SELECT DISTINCT(DATA_IMPORTACAO) AS DATAS_IMPORTACAO FROM INDICADORES_RDNG order by DATAS_IMPORTACAO DESC LIMIT 2) ORDER BY DATA_IMPORTACAO ASC")

        Datas = cursor_Datas.fetchone()
        coluna_atual = 2
        INDICADOR1 = 0
        INDICADOR2 = 0
        INDICADOR3 = 0
        TOTAL = 0
        while Datas:
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(0,coluna_atual,QtWidgets.QTableWidgetItem(Datas[0]))
            Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(0,coluna_atual-1,QtWidgets.QTableWidgetItem(Datas[0]))

            INDICADOR1 , INDICADOR2 , INDICADOR3 , TOTAL = BuscaValoresIndicadores(Datas[0],comunidade)

            PERCENTUAL = "{:.2f}".format((INDICADOR1 / TOTAL) * 100) + " %"
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(1,coluna_atual,QtWidgets.QTableWidgetItem(f"{INDICADOR1}   ( {PERCENTUAL} )"))
            PERCENTUAL = "{:.2f}".format((INDICADOR2 / TOTAL) * 100) + " %"
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(2,coluna_atual,QtWidgets.QTableWidgetItem(f"{INDICADOR2}   ( {PERCENTUAL} )"))
            PERCENTUAL = "{:.2f}".format((INDICADOR3 / TOTAL) * 100) + " %"
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(3,coluna_atual,QtWidgets.QTableWidgetItem(f"{INDICADOR3}   ( {PERCENTUAL} )"))

            coluna_atual += 1
            Datas = cursor_Datas.fetchone()

        # Calcula o percentual de evolução
        # Separar os valores absolutos de cada indicador, para o cálculo da evolução
        # Testa se o valor está zerado, para não dividir por zero e gerar um erro em runtime
        if float(Tela_RDNG_Indica.Tabela_Evolucao.item(1,2).text().split(" ( ")[0]) == 0:
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(1,4,QtWidgets.QTableWidgetItem("0"))
        else:
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(1,4,QtWidgets.QTableWidgetItem(str(float("{:.2f}".format(float(Tela_RDNG_Indica.Tabela_Evolucao.item(1,3).text().split(" ( ")[0]) / float(Tela_RDNG_Indica.Tabela_Evolucao.item(1,2).text().split(" ( ")[0]) * 100 ))) + " %"))

        if float(Tela_RDNG_Indica.Tabela_Evolucao.item(2,2).text().split(" ( ")[0]) == 0:
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(2,4,QtWidgets.QTableWidgetItem("0"))
        else:
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(2,4,QtWidgets.QTableWidgetItem(str(float("{:.2f}".format(float(Tela_RDNG_Indica.Tabela_Evolucao.item(2,3).text().split(" ( ")[0]) / float(Tela_RDNG_Indica.Tabela_Evolucao.item(2,2).text().split(" ( ")[0]) * 100 ))) + " %"))

        if float(Tela_RDNG_Indica.Tabela_Evolucao.item(3,2).text().split(" ( ")[0]) == 0:
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(3,4,QtWidgets.QTableWidgetItem("0"))
        else:
            Tela_RDNG_Indica.Tabela_Evolucao.setItem(3,4,QtWidgets.QTableWidgetItem(str(float("{:.2f}".format(float(Tela_RDNG_Indica.Tabela_Evolucao.item(3,3).text().split(" ( ")[0]) / float(Tela_RDNG_Indica.Tabela_Evolucao.item(3,2).text().split(" ( ")[0]) * 100 ))) + " %"))

        # Configura a tabela de detalhes da evolução
        Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setColumnWidth(0,350)
        Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setColumnWidth(1,100)
        Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setColumnWidth(2,100)
        Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setColumnWidth(3,200)

        # Define o tooltip de cada célula do grid
        #Tela_RDNG_Indica.Tabela_Evolucao.item(0,0).setToolTip("Ferramenta")
        Btn_Evolucao_Exibe_Inibe_Detalhes_click()

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante o carregamento da informações da evolução dos indicadores - Btn_Evolucao_click - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def Btn_Remove_Dados_click():
    # Pede confirmação para exclusão dos dados
    if (MessageBox.Mensagem(f"Confirma a exclusão dos dados de '{Tela_RDNG_Indica.Cbo_Data_Importacao_Manut.currentText()}' ?","Remoção de Dados",QMessageBox.Information,QMessageBox.Ok | QMessageBox.Cancel)) == QMessageBox.Ok:
        DATA_IMPORTACAO = Tela_RDNG_Indica.Cbo_Data_Importacao_Manut.currentText()
        manut.RemoveDados(DATA_IMPORTACAO[6:]+DATA_IMPORTACAO[3:5]+DATA_IMPORTACAO[:2])

        Preenche_Combos()

        MessageBox.Mensagem(f"Os dados referentes ao dia '{DATA_IMPORTACAO}' foram removidos da base de dados local!!!","Informação",QMessageBox.Information,QMessageBox.Ok)


def Calcula_Detalhes_Indicador_RDNG(ComandoSQL):
    cursor_tmp = BancodeDados.ConsultaSQL(ComandoSQL)
    RESULTADO = cursor_tmp.fetchone()
    if RESULTADO:
        return int(RESULTADO[0])


def Btn_Evolucao_Exibe_Inibe_Detalhes_click():
    try:
        # Exibe os detalhes do indicador / Esconde os detalhes do indicador
        if Tela_RDNG_Indica.Btn_Evolucao_Exibe_Inibe_Detalhes.text() == "Inibir Detalhes":
            Tela_RDNG_Indica.Btn_Evolucao_Exibe_Inibe_Detalhes.setText("Exibir Detalhes")

            # Torna os objetos (label e grid) invisíveis
            Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Detalhes.setVisible(False)
            Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setVisible(False)

        else:
            CLAUSULA_COMUNIDADE = ""
            if Tela_RDNG_Indica.Cbo_Comunidades_Evolucao.currentIndex() > 0:
                CLAUSULA_COMUNIDADE = f" AND COMUNIDADE = '{Tela_RDNG_Indica.Cbo_Comunidades_Evolucao.currentText()}'"

            # Só vai exibir os detalhes se um dos indicadores for selecionado
            if Tela_RDNG_Indica.Tabela_Evolucao.currentRow() > 0:
                # Verifica a linha selecionada e exibe os detalhes de acordo com o indicador
                if Tela_RDNG_Indica.Tabela_Evolucao.currentRow() == 1:
                    # Indicador RDNG
                    # Prepara o grid dos detalhes RDNG
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setRowCount(3)
                    Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Detalhes.setText("Detalhes Indicador RDNG")
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(0,0,QtWidgets.QTableWidgetItem("RDNG"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,0,QtWidgets.QTableWidgetItem("Só está checado o Combo, sem Link de Requisito(s)"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,0,QtWidgets.QTableWidgetItem("Link com Requisito(s) correto"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,3,QtWidgets.QTableWidgetItem("Selecionar o Combo e anexar o(s) Requisito(s)"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,3,QtWidgets.QTableWidgetItem("Ação Correta"))
                
                    # Repetir o total de não-rastreados do indicador
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,1,QtWidgets.QTableWidgetItem(Tela_RDNG_Indica.Tabela_Evolucao.item(1,2).text().split(" ( ")[0].strip()))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,2,QtWidgets.QTableWidgetItem(Tela_RDNG_Indica.Tabela_Evolucao.item(1,3).text().split(" ( ")[0].strip()))

                    # Calcular e inserir os dados do detalhamento do indicador RDNG
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,1,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT count(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE QTDE_RASTREADO = '1' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,1).text()}' {CLAUSULA_COMUNIDADE}"))))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,2,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT count(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE QTDE_RASTREADO = '1' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,2).text()}' {CLAUSULA_COMUNIDADE}"))))
                    #Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,2,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT count(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE QTDE_NAO_RASTREADO <> '1' AND QTDE_RASTREADO <> '1' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,2).text()}' {CLAUSULA_COMUNIDADE}"))))

                elif Tela_RDNG_Indica.Tabela_Evolucao.currentRow() == 2:
                    # Indicador Clearcase
                    # Prepara o grid dos detalhes RDNG
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setRowCount(4)
                    Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Detalhes.setText("Detalhes Indicador Clearcase")
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(0,0,QtWidgets.QTableWidgetItem("Clearcase"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,0,QtWidgets.QTableWidgetItem("Itens com Caminho Inválido"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,0,QtWidgets.QTableWidgetItem("Itens Migrados"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(3,0,QtWidgets.QTableWidgetItem("Caminho correto"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,3,QtWidgets.QTableWidgetItem("Utilizar o caminho correto"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,3,QtWidgets.QTableWidgetItem("N/A"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(3,3,QtWidgets.QTableWidgetItem("Ação Correta"))

                    # Repetir o total de não-rastreados do indicador
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,1,QtWidgets.QTableWidgetItem(Tela_RDNG_Indica.Tabela_Evolucao.item(2,2).text().split(" ( ")[0].strip()))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,2,QtWidgets.QTableWidgetItem(Tela_RDNG_Indica.Tabela_Evolucao.item(2,3).text().split(" ( ")[0].strip()))

                    # Calcular e inserir os dados do detalhamento do indicador Clearcase
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,1,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT COUNT(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE INCLUSAO_REQ_CLEARCASE like '%MIGRADO PARA A COMUNIDADE%' AND INCLUSAO_REQ_CLEARCASE not like '%01-REQ%' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,1).text()}' {CLAUSULA_COMUNIDADE}"))))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,2,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT COUNT(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE INCLUSAO_REQ_CLEARCASE like '%MIGRADO PARA A COMUNIDADE%' AND INCLUSAO_REQ_CLEARCASE not like '%01-REQ%' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,2).text()}' {CLAUSULA_COMUNIDADE}"))))

                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(3,1,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT COUNT(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE INCLUSAO_REQ_CLEARCASE like '%01-REQ%' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,1).text()}' {CLAUSULA_COMUNIDADE}"))))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(3,2,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT COUNT(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE INCLUSAO_REQ_CLEARCASE like '%01-REQ%' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,2).text()}' {CLAUSULA_COMUNIDADE}"))))

                elif Tela_RDNG_Indica.Tabela_Evolucao.currentRow() == 3:
                    # Indicador Justificativa
                    # Prepara o grid dos detalhes RDNG
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setRowCount(3)
                    Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Detalhes.setText("Detalhes Indicador Justificativa")
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(0,0,QtWidgets.QTableWidgetItem("Justificativa"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,0,QtWidgets.QTableWidgetItem("Total de itens Justificados"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,0,QtWidgets.QTableWidgetItem("Itens Migrados"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,3,QtWidgets.QTableWidgetItem("Justificar com coerência"))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,3,QtWidgets.QTableWidgetItem("N/A"))

                    # Repetir o total de não-rastreados do indicador
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,1,QtWidgets.QTableWidgetItem(Tela_RDNG_Indica.Tabela_Evolucao.item(3,2).text().split(" ( ")[0].strip()))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(1,2,QtWidgets.QTableWidgetItem(Tela_RDNG_Indica.Tabela_Evolucao.item(3,3).text().split(" ( ")[0].strip()))

                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,1,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT COUNT(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE JUSTIF_AUSENCIA_REQ like '%MIGRADO PARA A COMUNIDADE%' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,1).text()}' {CLAUSULA_COMUNIDADE}"))))
                    Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(2,2,QtWidgets.QTableWidgetItem(str(Calcula_Detalhes_Indicador_RDNG(f"SELECT COUNT(DISTINCT(HU)) FROM INDICADORES_RDNG WHERE JUSTIF_AUSENCIA_REQ like '%MIGRADO PARA A COMUNIDADE%' AND DATA_IMPORTACAO = '{Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.item(0,2).text()}' {CLAUSULA_COMUNIDADE}"))))

                Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setItem(0,3,QtWidgets.QTableWidgetItem("Ação"))
                # Muda o texto do botão
                Tela_RDNG_Indica.Btn_Evolucao_Exibe_Inibe_Detalhes.setText("Inibir Detalhes")

                # Torna os objetos (label e grid) visíveis
                Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Detalhes.setVisible(True)
                Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setVisible(True)

    except Exception as erro:
        MessageBox.Mensagem(f"Ocorreu um erro durante o carregamento do detalhamento dos indicadores - Btn_Evolucao_Exibe_Inibe_Detalhes_click - [' {erro}' ]" ,"Erro",QMessageBox.Critical,QMessageBox.Ok)
        return


def Tabela_Evolucao_click():
    # Se o grid de detalhes da evolução estiver visível, ele aciona o botão para escondê-lo
    COMUNIDADE = ""
    if Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.isVisible() == True:
        Btn_Evolucao_Exibe_Inibe_Detalhes_click()


def Btn_Seleciona_Comunidade_Evolucao_click():
    # Verifica se o usuário selecionou uma comunidade
    COMUNIDADE = ""

    if Tela_RDNG_Indica.Cbo_Comunidades_Evolucao.currentIndex() > -1:
        COMUNIDADE = Tela_RDNG_Indica.Cbo_Comunidades_Evolucao.currentText()

    CarregaDadosEvolucao(COMUNIDADE)


def Btn_Limpar_Filtros_click():
    Tela_RDNG_Indica.Cbo_Comunidades.setCurrentIndex(0)
    Tela_RDNG_Indica.Cbo_Indicador.setCurrentIndex(0)
    Tela_RDNG_Indica.Rd_HUs_Inconsistentes.setChecked(False)
    Tela_RDNG_Indica.Rd_HUs_Corretas.setChecked(False)

def Cbo_Data_Importacao_click():
    # Evento acionado quando o usuário escolhe alguma opção no Combo 'Cbo_Data_Importacao'
    # Como o usuário alterou a seleção do combo, a lista de HUs será zerada
    Tela_RDNG_Indica.Tabela_HUs.setRowCount(0)
    Tela_RDNG_Indica.LCD_Qtde_Registros.display(0)
    Tela_RDNG_Indica.repaint()


# Abre uma instancia do TKinter para ler a resolução da tela
root = Tk()
monitor_width = root.winfo_screenwidth()
monitor_height = root.winfo_screenheight()
largura_tela = 1280
altura_tela = 720
borda_esquerda = int((monitor_width - largura_tela) / 2)
borda_superior = int((monitor_height - altura_tela) / 2)

# Verifica se esta sendo chamado por um interpretador python ou executavel
if sys.argv[0].find(".exe") > -1:
	caminho = sys.path[2]
else:
	caminho = sys.path[0]

# Cria a tela
app = QtWidgets.QApplication([])

# Lê o arquivo .ui
Tela_RDNG_Indica = uic.loadUi(sys.path[0] + "\\Indicadores_RDNG.ui")

# Configura a janela principal
Tela_RDNG_Indica.setGeometry(borda_esquerda , borda_superior , largura_tela , altura_tela)
Tela_RDNG_Indica.setWindowTitle("Indicadores RDNG")

# Define as funções que serão chamadas em eventos de objetos da tela
Tela_RDNG_Indica.Btn_Select_Arquivo.clicked.connect(Btn_Select_Arquivo_click)
Tela_RDNG_Indica.Btn_Atualiza_Base.clicked.connect(Btn_Atualiza_Base_click)
Tela_RDNG_Indica.Btn_Filtro.clicked.connect(Btn_Filtro_click)
Tela_RDNG_Indica.Btn_Remove_Dados.clicked.connect(Btn_Remove_Dados_click)
Tela_RDNG_Indica.Btn_Evolucao_Exibe_Inibe_Detalhes.clicked.connect(Btn_Evolucao_Exibe_Inibe_Detalhes_click)
Tela_RDNG_Indica.Btn_Seleciona_Comunidade_Evolucao.clicked.connect(Btn_Seleciona_Comunidade_Evolucao_click)
Tela_RDNG_Indica.Tabela_Evolucao.cellClicked.connect(Tabela_Evolucao_click)
Tela_RDNG_Indica.Cbo_Data_Importacao.activated.connect(Cbo_Data_Importacao_click)
Tela_RDNG_Indica.Btn_Limpar_Filtros.clicked.connect(Btn_Limpar_Filtros_click)

# Deixa os objetos dos detalhes da evolução invisíveis
Tela_RDNG_Indica.Lbl_Evolucao_Titulo_Detalhes.setVisible(False)
Tela_RDNG_Indica.Tabela_Evolucao_Detalhes.setVisible(False)

# Abre a conexao do banco de dados
BancodeDados = SQLite(f"{caminho}\\Indicadores_RDNG.db")

manut = Manutencao(f"{caminho}\\Indicadores_RDNG.db")

# Preenche os combos de filtro
Preenche_Combos()

# Exibe a tela
Tela_RDNG_Indica.show()
app.exec()