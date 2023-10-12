import csv
import sys
from datetime import datetime

class Demandas():

    def Calcula_USTs_Demandas(arq_entrada):
        import csv

        servico_baixa = {'Apoio à Solução de Problemas Relacionados às Ferramentas': 4,
                         'Criação/Manutenção de área de projeto': 2,
                         'Mentoring': 2,
                         'Manutenção em permissões/perfis de usuário':1,
                         'Criação de área de projeto integrada/associação de áreas de projeto':1,
                         'Manutenção em Indicador / Relatório':8,
                         'Manutenção em Itens de Configuração (ex:Retirada de check-out)':2,
                         'Manutenção em painéis':2,
                         'Criação e Configuração de Projeto':4,
                         'Criação / Manutenção de Atributos':1,
                         'G1 - Capacitação':0,
                         'Criação / Manutenção de View':2,
                         'Criação / Manutenção de VOB':8,
                         'Criação / Manutenção de Artefatos':2,
                         'Criação / Manutenção de Trigger':16,
                         'Customização de modelos de script':4,
                         'Importação de itens de projeto': 4,
                         'Manutenção em Label': 4,
                         'Não Informado': 0
                         }


        servico_media = {'Apoio à Solução de Problemas Relacionados às Ferramentas': 8,
                         'Criação/Manutenção de área de projeto': 4,
                         'Mentoring': 4,
                         'Manutenção em permissões/perfis de usuário': 2,
                         'Criação de área de projeto integrada/associação de áreas de projeto': 2,
                         'Manutenção em Indicador / Relatório': 16,
                         'Manutenção em Itens de Configuração (ex:Retirada de check-out)': 2,
                         'Manutenção em painéis': 4,
                         'Criação e Configuração de Projeto': 4,
                         'Criação / Manutenção de Atributos': 2,
                         'G1 - Capacitação': 0,
                         'Criação / Manutenção de View': 2,
                         'Criação / Manutenção de VOB': 8,
                         'Criação / Manutenção de Artefatos': 4,
                         'Criação / Manutenção de Trigger': 16,
                         'Customização de modelos de script': 4,
                         'Importação de itens de projeto': 4,
                         'Manutenção em Label': 4,
                         'Não Informado': 0
                         }

        servico_alta = {'Apoio à Solução de Problemas Relacionados às Ferramentas': 12,
                         'Criação/Manutenção de área de projeto': 8,
                         'Mentoring': 8,
                         'Manutenção em permissões/perfis de usuário': 4,
                         'Criação de área de projeto integrada/associação de áreas de projeto': 4,
                         'Manutenção em Indicador / Relatório': 32,
                         'Manutenção em Itens de Configuração (ex:Retirada de check-out)': 2,
                         'Manutenção em painéis': 8,
                         'Criação e Configuração de Projeto': 4,
                         'Criação / Manutenção de Atributos': 4,
                         'G1 - Capacitação': 0,
                         'Criação / Manutenção de View': 2,
                         'Criação / Manutenção de VOB': 8,
                         'Criação / Manutenção de Artefatos': 8,
                         'Criação / Manutenção de Trigger': 16,
                         'Customização de modelos de script': 4,
                         'Importação de itens de projeto': 4,
                         'Manutenção em Label': 4,
                         'Não Informado': 0
                         }


        def Calcula_USTs(SERVICO, COMPLEXIDADE, QUANTIDADE):
            # De acordo com a complexidade, buscar a quantidade de UST no dicionário correspondente
            try:
                if (COMPLEXIDADE == 'Baixa'):
                    return int(servico_baixa[SERVICO]) * int(QUANTIDADE)
                elif (COMPLEXIDADE == 'Média'):
                    return int(servico_media[SERVICO]) * int(QUANTIDADE)
                else:
                    return int(servico_alta[SERVICO]) * int(QUANTIDADE)
            except:
                return 0

        # Abre a planilha original com as demandas do período
        try:
            planilha = csv.DictReader(open(arq_entrada, encoding='utf-8'), delimiter=';')
        #except Exception as e:
        #    print(str(e))
        except FileNotFoundError:
            return 'File Not Found'

        # Prepara o arquivo de saida, com as USTs calculadas
        try:
            arquivo_saida = open(arq_entrada[:-4] + "_saida.csv", "w", encoding="UTF-8")
        except:
            return 0

        # Escreve a primeira linha, com o cabeçalho
        linha_saida="ID;Resumo;Quantidade;Complexidade;Data de Criação;Prazo Final;Serviço;UST;Grupo SIGCT;Preposto" + "\n"
        arquivo_saida.write(linha_saida)

        try:
            for linha in planilha:
                linha_saida = ""
                linha_saida += str(linha["ID"]) + ";"
                linha_saida += str(linha["Resumo"])   + ";"
                linha_saida += str(linha["Quantidade"]) + ";"
                linha_saida += str(linha["Complexidade"]) + ";"
                linha_saida += str(linha["Data de Criação"]) + ";"
                linha_saida += str(linha["Prazo Final"]) + ";"
                linha_saida += str(linha["Serviço Especializado de Apoio a Ferramentas Rational"]) + ";"

                servico = linha["Serviço Especializado de Apoio a Ferramentas Rational"];
                complexidade = str(linha["Complexidade"]);
                qtde= str(linha["Quantidade"]);

                linha_saida += str(Calcula_USTs(servico,complexidade,qtde)) + ";"
                linha_saida += str(linha["Grupo SIGCT"]) + ";"
                linha_saida += str(linha["Preposto 2605"])
                linha_saida += "\n"
                arquivo_saida.write(linha_saida)

        except UnicodeDecodeError:
            return 'UnicodeDecodeError'

        finally:
            arquivo_saida.close

        return str(arq_entrada[:-4] + "_saida.csv")

    
    def Calcula_SLAs(arquivo_entrada):
        import csv
        from datetime import datetime
        
        sys.path.append('c:\\Projetos\\Python\\Funcoes')
        from BancodeDados import SQLite

        def Calcula_Periodo(DATA):
            if (DATA.day > 20):
                if (DATA.month == 12):
                    PERIODO = str(DATA.year + 1) + '/01'
                else:
                    PERIODO = str(DATA.year) + '/' + str(DATA.month + 1).rjust(2,'0')
            else:
                PERIODO = str(DATA.year) + '/' + str(DATA.month).rjust(2,'0')

            return PERIODO

        def Calcula_Indicador(indicador,periodo,TOTAL_DEMANDAS,DB_CAIXA,preposto=None):
            if preposto is None:
                # Para cada período, buscar as demandas atrasadas
                ComandoSQL=f"SELECT SUM(QTDE_ACIONAMENTOS) as QTDE_DEMANDAS FROM Resumo_Demandas_SLA WHERE PERIODO_PREVISTO = '{PERIODO}' and {indicador} = 1"
            else:
                ComandoSQL=f"SELECT SUM(QTDE_ACIONAMENTOS) as QTDE_DEMANDAS FROM Resumo_Demandas_SLA WHERE PERIODO_PREVISTO = '{PERIODO}' and {indicador} = 1 and PREPOSTO = '{preposto}'"

            cursor_indicador = DB_CAIXA.ConsultaSQL(ComandoSQL)
            indicador = cursor_indicador.fetchone()
            QTDE_DEMANDAS = indicador[0]
            if QTDE_DEMANDAS is None:
                QTDE_DEMANDAS = 0

            # Calcula o indicador ITE
            return round( ( (TOTAL_DEMANDAS - QTDE_DEMANDAS) / TOTAL_DEMANDAS ),2)

        # Cria a conexão com o banco de dados
        DB_CAIXA = SQLite('Demandas_SLA.db')

        try:
            # Limpa a tabela antes de iniciar a importação
            DB_CAIXA.ExecutaComandoSQL('delete from Resumo_Demandas_SLA')

            # Abre a planilha com o histórico das demandas
            planilha = csv.DictReader(open(arquivo_entrada, encoding='UTF-8'), delimiter=';')

            # Inicializa as variáveis de controle
            ID = 0
            ATRASADO = 0
            REJEITADO = 0
            ESTOQUE = 0
            CANCELADO = 0
            ENTREGUE = 0
            PERIODO = ''

            for linha in planilha:
                if ( (ID != linha['ID']) and (ID != 0) ):
                    if (CANCELADO == 0):
                        #Quebra de ID -> Inserir os dados na tabela de Resumo
                        ComandoSQL = f"insert into Resumo_Demandas_SLA (ID,REJEITADO,ATRASADO,ESTOQUE,PERIODO_PREVISTO,PERIODO_ENTREGA,QTDE_ACIONAMENTOS,PREPOSTO) values ( {ID} , {REJEITADO} , {ATRASADO} , {ESTOQUE} , '{PERIODO_PREVISTO}' , '{PERIODO_ENTREGA}' , {QTDE_ACIONAMENTOS} , '{PREPOSTO}')"
                        retorno = DB_CAIXA.ExecutaComandoSQL(ComandoSQL)

                    ATRASADO = 0
                    REJEITADO = 0
                    ESTOQUE = 0
                    CANCELADO = 0
                    ENTREGUE = 0
                    PERIODO_PREVISTO = ''
                    PERIODO_ENTREGA = ''
                    QTDE_ACIONAMENTOS = 0
                    PREPOSTO = ''

                ID = linha['ID']
                #Procurar por rejeitados
                if linha['Status'] == 'Rejeitado':
                    REJEITADO = 1

                # Verificar se foi entregue em atraso
                if ( (linha['Status'] == 'Entregue') and (ENTREGUE == 0) ):
                    # Verificar se a demanda foi entregue com atraso
                    if len(linha['Prazo_Final']) > 0:
                        DATA_ATUALIZACAO = datetime.strptime(linha['Data_Atualizacao'], '%d/%m/%y %H:%M')
                        PRAZO_FINAL = datetime.strptime(linha['Prazo_Final'], '%d/%m/%y %H:%M')
                        if str(DATA_ATUALIZACAO)[:10] > str(PRAZO_FINAL)[:10]:
                            ATRASADO = 1

                        # Calcular o período previsto para entrega
                        PERIODO_PREVISTO = Calcula_Periodo(PRAZO_FINAL)

                        # Calcular o período real da entrega
                        PERIODO_ENTREGA = Calcula_Periodo(DATA_ATUALIZACAO)
                    else:
                        PERIODO_PREVISTO = ''
                        PERIODO_ENTREGA = ''

                    #Marca um flag pra indicar que já considerou a entrega do item
                    ENTREGUE = 1
  
                    # Verificar se o item ficou em estoque, só verifica se o item tiver os campos de periodo preenchidos
                    if ( (PERIODO_PREVISTO != '') and (PERIODO_ENTREGA != '') ):
                        if PERIODO_ENTREGA > PERIODO_PREVISTO:
                            ESTOQUE = 1
                        else:
                            ESTOQUE = 0

                    # Ler a quantidade de acionamentos
                    QTDE_ACIONAMENTOS = linha['Quantidade']

                    # Ler o Preposto no momento da entrega
                    PREPOSTO = linha['Preposto']

                # Verificar se foi cancelado
                if linha['Status'] == 'Cancelado':
                    CANCELADO = 1

        except:
            # Se ocorreu algum erro, retorna mensagem de erro padrão
            return 'Erro ao Calcular SLAs'

        finally:
            # Independente de ter ocorrido algum erro, o programa deve fechar o arquivo de entrada
            planilha.close

        # Lê os dados armazenados na tabela Resumo_Demandas e calcula os indicadores
        try:
            # Pega apenas o diretório do arquivo de entrada, pra usar no arquivo de saída
            dir_saida=""
            caminho_saida = arquivo_entrada.split("\\")[:-1]
            for partes in caminho_saida:
                dir_saida = dir_saida + str(partes) + "\\"

            # Abre arquivo de saída e gravar a primeira linha (cabeçalho)
            arquivo_saida = open(dir_saida + "Indicadores_SLA_CAIXA.csv", mode="w" , encoding="UTF-8")
            arquivo_saida.write("PERIODO;ITE;IAE;IEE \n")

            arquivo_saida_prepostos = open(dir_saida + "Indicadores_SLA_CAIXA_Prepostos.csv", mode='w' , encoding='UTF-8')
            arquivo_saida_prepostos.write("PREPOSTO;PERIODO;ITE;IAE;IEE \n")

            # Lê os dados gerados e cria o arquivo de saída
            ComandoSQL = "select DISTINCT(PERIODO_PREVISTO) from Resumo_Demandas_SLA WHERE PERIODO_PREVISTO <> '' order by PERIODO_PREVISTO"
            cursor_periodos = DB_CAIXA.ConsultaSQL(ComandoSQL)
            periodos = cursor_periodos.fetchone()
            while periodos:
                PERIODO = periodos[0]

                # Total de demandas entregues para o período
                ComandoSQL = f"select sum(QTDE_ACIONAMENTOS) FROM Resumo_Demandas_SLA WHERE PERIODO_PREVISTO = '{PERIODO}'"
                cursor_total_demandas = DB_CAIXA.ConsultaSQL(ComandoSQL)
                total_demandas = cursor_total_demandas.fetchone()
                TOTAL_DEMANDAS = total_demandas[0]
                if TOTAL_DEMANDAS is None:
                    TOTAL_DEMANDAS = 0

                # Calcula os indicadores gerais
                ITE = Calcula_Indicador('ATRASADO',PERIODO,TOTAL_DEMANDAS,DB_CAIXA)
                IAE = Calcula_Indicador('REJEITADO',PERIODO,TOTAL_DEMANDAS,DB_CAIXA)
                IEE = Calcula_Indicador('ESTOQUE',PERIODO,TOTAL_DEMANDAS,DB_CAIXA)

                # Escreve a linha dos indicadores do período - Geral
                arquivo_saida.write(f"{PERIODO} ; {ITE} ; {IAE} ; {IEE} \n")

                # Escreve novamente o cabeçalho, pra separar cada período
                arquivo_saida_prepostos.write("\n")
                arquivo_saida_prepostos.write("\n")
                arquivo_saida_prepostos.write("PREPOSTO;PERIODO;ITE;IAE;IEE \n")

                # Pesquisa os prepostos das demandas e calcula os indicadores de cada preposto
                cursor_prepostos = DB_CAIXA.ConsultaSQL("select DISTINCT(PREPOSTO) from Resumo_Demandas_SLA where PREPOSTO <> '' and PREPOSTO is not null order by preposto")
                prepostos = cursor_prepostos.fetchone()
                while prepostos:
                    # Busca o total de demandas do preposto para o período
                    ComandoSQL = f"select sum(QTDE_ACIONAMENTOS) FROM Resumo_Demandas_SLA WHERE PERIODO_PREVISTO = '{PERIODO}' AND PREPOSTO = '{prepostos[0]}'"
                    cursor_total_demandas_preposto = DB_CAIXA.ConsultaSQL(ComandoSQL)
                    total_demandas_preposto = cursor_total_demandas_preposto.fetchone()
                    TOTAL_DEMANDAS_PREPOSTO = total_demandas_preposto[0]
                    if TOTAL_DEMANDAS_PREPOSTO is None:
                        TOTAL_DEMANDAS_PREPOSTO = 0
                        PREPOSTO = ''
                        ITE=0
                        IAE=0
                        IEE=0
                    else:
                        PREPOSTO = prepostos[0]
                        ITE = Calcula_Indicador('ATRASADO',PERIODO,TOTAL_DEMANDAS_PREPOSTO,DB_CAIXA,PREPOSTO)
                        IAE = Calcula_Indicador('REJEITADO',PERIODO,TOTAL_DEMANDAS_PREPOSTO,DB_CAIXA,PREPOSTO)
                        IEE = Calcula_Indicador('ESTOQUE',PERIODO,TOTAL_DEMANDAS_PREPOSTO,DB_CAIXA,PREPOSTO)

                    arquivo_saida_prepostos.write(f"{prepostos[0]} ; {PERIODO} ; {ITE} ; {IAE} ; {IEE} \n")

                    prepostos = cursor_prepostos.fetchone()

                # Lê o próximo registro (Períodos)
                periodos = cursor_periodos.fetchone()

        except:
            # Se ocorreu algum erro, retorna mensagem de erro padrão
            return 'Erro ao gerar o arquivo de saída'
        
        else:
            # Só retorna a mensagem de OK, se tudo deu certo
            return 'Dados dos SLAs gerados com sucesso'

        finally:
            # Independente de ter ocorrido algum erro, o programa deve fechar os arquivos
            arquivo_saida.close
            arquivo_saida_prepostos.close

        