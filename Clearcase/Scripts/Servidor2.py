import sys
from textwrap import indent
from flask import Flask , jsonify
import json


sys.path.append('C:\\Projetos\\CAIXA\\Clearcase\\Funcoes')
from BancodeDados import SQLite

# Abre a conexao do banco de dados
BancodeDados = SQLite('C:\\Projetos\\CAIXA\\Clearcase\\Clearcase.db')


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "<p> Serviços CAIXA!!!</p>"


@app.route('/clearcase', methods=['GET'])
def index_clearcase():
    return "<p> Página Clearcase </p>"


@app.route('/clearcase/vobs/', methods=['GET'])
def clearcase_retorna_todas_vobs():
    cursor_VOBs = BancodeDados.ConsultaSQL("SELECT VOB , SERVIDOR , COMUNIDADE , FABRICA FROM VOBS")
    VOBs = cursor_VOBs.fetchone()
    
    dic_dados = {}
    while VOBs:
        dic_dados[VOBs[0]] = {
            "VOB":VOBs[0] ,
            "SERVIDOR":VOBs[1] ,
            "COMUNIDADE":VOBs[2] ,
            "FABRICA":VOBs[3] ,
            }

        VOBs = cursor_VOBs.fetchone()

    return json.dumps(dic_dados,indent=4)


@app.route('/clearcase/vob/<nome_vob>', methods=['GET'])
def clearcase_pesquisa_vob(nome_vob):
    cursor_VOBs = BancodeDados.ConsultaSQL(f"SELECT VOB , SERVIDOR , COMUNIDADE , FABRICA FROM VOBS WHERE VOB = '{nome_vob}'")
    VOBs = cursor_VOBs.fetchone()
    
    dic_dados = {}
    if VOBs:
        dic_dados[VOBs[0]] = {
            "VOB":VOBs[0] ,
            "SERVIDOR":VOBs[1] ,
            "COMUNIDADE":VOBs[2] ,
            "FABRICA":VOBs[3] ,
            }

        VOBs = cursor_VOBs.fetchone()
        return json.dumps(dic_dados,indent=4)


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=8080)
