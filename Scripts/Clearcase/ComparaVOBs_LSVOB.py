import sys
from openpyxl import Workbook

sys.path.append('c:\\Projetos\\CAIXA\\Funcoes')
from BancodeDados import SQLite

DB = SQLite(sys.path[0] + '\\Clearcase.db')

# Limpa a tabela
DB.ExecutaComandoSQL("delete from COMPARA_LSVOB")


def CarregaDadosLSVOB(arquivo,campo):
    try:
        # Carregar as VOBs do arquivo para a tabela
        with open(arquivo,mode='r',encoding='ANSI') as arquivo:
            for linha in arquivo:
                linha = linha.upper()
                POSICAO_INICIAL = linha.find("\\")
                POSICAO_FINAL = linha.find("\\\\")

                VOB = linha[POSICAO_INICIAL + 1:POSICAO_FINAL].strip()

                # Verifico se a VOB já existe
                cursor_VOB = DB.ConsultaSQL(f"select VOB from COMPARA_LSVOB where VOB = '{VOB}'")

                VOBs = cursor_VOB.fetchone()

                if VOBs:
                    # Encontrou a VOB, atualizar os dados
                    DB.ExecutaComandoSQL(f"update COMPARA_LSVOB set '{campo}' = '1' where VOB = '{VOB}'")
                else:
                    # Não encontrou a VOB, inserir os dados
                    DB.ExecutaComandoSQL(f"insert into COMPARA_LSVOB (VOB,{campo}) values ('{VOB}','1')")
    except Exception as erro:
        print(f"Ocorreu um erro durante a comparacao de arquivos LSVOB -  [' {erro}' ]")


def transforma(valor):
    if valor == 1:
        return 'Sim'
    else:
        return ''


def GeraPlanilhaLSVOBs():
    # Gera uma planilha com os dados da tabela COMPARA_LSVOB
    try:
        arquivo_saida = Workbook()

        cursor_LSVOB = DB.ConsultaSQL("select VOB,SERVIDOR_BR,SERVIDOR_SP,SERVIDOR_RJ,SERVIDOR_CEPEM,SERVIDOR_LOTERIAS from COMPARA_LSVOB")
        VOBs = cursor_LSVOB.fetchone()

        linha = 2

        plan = arquivo_saida.create_sheet(title='Compara_LSVOB')
        plan[f"B{linha}"] = "VOB"
        plan[f"C{linha}"] = "SERVIDOR_BR"
        plan[f"D{linha}"] = "SERVIDOR_SP"
        plan[f"E{linha}"] = "SERVIDOR_RJ"
        plan[f"F{linha}"] = "SERVIDOR_CEPEM"
        plan[f"G{linha}"] = "SERVIDOR_LOTERIAS"

        linha += 1
        while VOBs:
            plan[f"B{linha}"] = f"{VOBs[0]}"
            plan[f"C{linha}"] = transforma(VOBs[1])
            plan[f"D{linha}"] = transforma(VOBs[2])
            plan[f"E{linha}"] = transforma(VOBs[3])
            plan[f"F{linha}"] = transforma(VOBs[4])
            plan[f"G{linha}"] = transforma(VOBs[5])

            linha += 1
            VOBs = cursor_LSVOB.fetchone()

		# Remover a primeira aba (Sheet)
        aba_sheet = arquivo_saida['Sheet']
        arquivo_saida.remove(aba_sheet)

        # Salva a planilha
        arquivo_saida.save(sys.path[0] + '\\Arquivos\\Compara_LSVOB.xlsx')

    except Exception as erro:
        print(f"Ocorreu um erro durante a geração do arquivo XLS dos grupos - GeraPlanilhaGrupos_Excel - [' {erro}' ]")
        return


# Carrega os dados dos arquivos LSVOB
CarregaDadosLSVOB(sys.path[0] + '\\LSVOB\\VOBs_BR.txt','SERVIDOR_BR')
CarregaDadosLSVOB(sys.path[0] + '\\LSVOB\\VOBs_SP.txt','SERVIDOR_SP')
CarregaDadosLSVOB(sys.path[0] + '\\LSVOB\\VOBs_RJ.txt','SERVIDOR_RJ')
CarregaDadosLSVOB(sys.path[0] + '\\LSVOB\\VOBs_CEPEM.txt','SERVIDOR_CEPEM')
CarregaDadosLSVOB(sys.path[0] + '\\LSVOB\\VOBs_LOTERIAS.txt','SERVIDOR_LOTERIAS')

# Gera a planilha com o resultado
GeraPlanilhaLSVOBs()