import os
import sys
from textwrap import indent
from flask import Flask , jsonify
import json

# Inclui um novo caminho, com os arquivos de funções
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Funcoes import BancodeDados

# Abre a conexao do banco de dados
MeuBanco = BancodeDados.SQLite(sys.path[0] + '\\Clearcase.db')

# Inicializa a aplicação
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "<p> Serviços CAIXA!!!</p>"

# Serviços Clearcase
@app.route('/clearcase', methods=['GET'])
def index_clearcase():
    return "<p> Página Clearcase </p>"

# Retorna todas as VOBs
@app.route('/clearcase/vobs/', methods=['GET'])
def clearcase_retorna_todas_vobs():
    cursor_VOBs = MeuBanco.ConsultaSQL("SELECT VOB , SERVIDOR , COMUNIDADE , FABRICA FROM VOBS")
    VOBs = cursor_VOBs.fetchone()
    
    dados = []
    dict_VOB = {}
    while VOBs:
        dict_VOB = {'VOB':VOBs[0] , 'SERVIDOR':VOBs[1] , 'COMUNIDADE':VOBs[2] , 'FABRICA':VOBs[3]}

        dados.append(dict_VOB)
        VOBs = cursor_VOBs.fetchone()
    return dados

# Pesquisa por VOB
@app.route('/clearcase/vob/<nome_vob>', methods=['GET'])
def clearcase_pesquisa_vob(nome_vob):
    cursor_VOBs = MeuBanco.ConsultaSQL(f"SELECT VOB , SERVIDOR , COMUNIDADE , FABRICA FROM VOBS WHERE VOB = '{nome_vob}'")
    VOBs = cursor_VOBs.fetchone()
    
    dados = []
    dict_VOB = {}
    while VOBs:
        dict_VOB = {'VOB':VOBs[0] , 'SERVIDOR':VOBs[1] , 'COMUNIDADE':VOBs[2] , 'FABRICA':VOBs[3]}
        dados.append(dict_VOB)
        VOBs = cursor_VOBs.fetchone()
    return dados

# Pesquisa por comunidade
@app.route('/clearcase/comunidade/<nome_comunidade>', methods=['GET'])
def clearcase_pesquisa_comunidade(nome_comunidade):
    cursor_VOBs = MeuBanco.ConsultaSQL(f"SELECT VOB , SERVIDOR , COMUNIDADE , FABRICA FROM VOBS WHERE LTRIM(RTRIM(COMUNIDADE)) = '{nome_comunidade}'")
    VOBs = cursor_VOBs.fetchone()
    
    dados = []
    dict_VOB = {}
    while VOBs:
        dict_VOB = {'VOB':VOBs[0] , 'SERVIDOR':VOBs[1] , 'COMUNIDADE':VOBs[2] , 'FABRICA':VOBs[3]}
        dados.append(dict_VOB)
        VOBs = cursor_VOBs.fetchone()
    return dados


# Executa o serviço
if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=8080)
