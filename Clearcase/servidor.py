from flask import Flask, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import json
import sys
from BancodeDados import SQLite


app = Flask(__name__)

# SWAGGER
SWAGGER_URL = '/docs'

#API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)
API_URL = 'http://127.0.0.1:5000/v2/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

# Definindo as rotas
@app.route("/",methods=['GET'])
def home():
    dados = []
    dados.append("API CAIXA")

    return render_template('index.html',retornos=dados)


@app.route("/clearcase",methods=['GET'])
def clearcase():
    dados = []
    dados.append("Bem-vindo aos servicos WEB - Clearcase")
    dados.append("Tipos de Pesquisas")
    dados.append("")
    dados.append(" '/clearcase/vobs'                        -> Lista todas as VOBs, com informações da comunidade e fabrica")
    dados.append(" '/clearcase/vob/<VOB>'                   -> Lista informacoes da VOB informada")
    dados.append(" '/clearcase/comunidades'                 -> Lista todas as Comunidades")
    dados.append(" '/clearcase/comunidade/<COMUNIDADE>'     -> Lista informacoes das VOBs da Comunidade informada")
    dados.append(" '/clearcase/fabricas'                    -> Lista todas as Fabricas")
    dados.append(" '/clearcase/fabricas/<COMUNIDADE>'       -> Lista informacoes da Fabrica informada")
    dados.append(" '/clearcase/fabrica/<FABRICA>'           -> Lista informacoes das VOBs da Fabrica informada")
    dados.append(" '/clearcase/acl/<COMUNIDADE>/<FABRICA>'  -> Retorna informacoes de configuracao do ACL (Rolemaps) para a Comunidade e Fabrica informadas")

    return render_template('index.html',retornos=dados)


@app.route("/clearcase/vobs", methods=['GET'])
def Lista_VOBs():
    cursor_VOBs = BancodeDados.ConsultaSQL("SELECT VOB, COMUNIDADE,FABRICA FROM VOBs")
    VOBs = cursor_VOBs.fetchone()
    Lista_VOBs = []
    while VOBs:
        saida = {'VOB': VOBs[0],'comunidade': VOBs[1],'fabrica': VOBs[2] }
        Lista_VOBs.append(saida)

        VOBs = cursor_VOBs.fetchone()

    return jsonify(Lista_VOBs)


@app.route("/clearcase/vob/<VOB>",methods=['GET'])
def Pesquisa_VOB(VOB):
    cursor_VOB = BancodeDados.ConsultaSQL(f"SELECT VOB, COMUNIDADE,FABRICA FROM VOBs where VOB='{VOB}'")
    VOBs = cursor_VOB.fetchone()
    if VOBs:
        saida = {'VOB': VOBs[0],'comunidade': VOBs[1],'fabrica': VOBs[2] }
        return jsonify(saida)
    else:
        saida = {'Aviso': "VOB nao encontrada"}
        return jsonify(saida)


@app.route("/clearcase/comunidade/<COMUNIDADE>",methods=['GET'])
def Pesquisa_VOBs_Comunidade(COMUNIDADE):
    cursor_VOBs = BancodeDados.ConsultaSQL(f"SELECT VOB, COMUNIDADE,FABRICA FROM VOBs where trim(COMUNIDADE) = '{COMUNIDADE}'")
    VOBs = cursor_VOBs.fetchone()

    Lista_VOBs = []
    while VOBs:
        saida = {'VOB': VOBs[0],'comunidade': VOBs[1],'fabrica': VOBs[2] }
        Lista_VOBs.append(saida)

        VOBs = cursor_VOBs.fetchone()

    return jsonify(Lista_VOBs)


@app.route("/clearcase/comunidades",methods=['GET'])
def Pesquisa_Comunidades():
    cursor_comunidades = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(COMUNIDADE) FROM VOBs where COMUNIDADE is not '' and COMUNIDADE is not null")
    COMUNIDADES = cursor_comunidades.fetchone()

    Lista_comunidades = []
    while COMUNIDADES:
        saida = {'COMUNIDADE': COMUNIDADES[0].strip()}
        Lista_comunidades.append(saida)

        COMUNIDADES = cursor_comunidades.fetchone()

    return render_template('index.html',retornos=Lista_comunidades)


@app.route("/clearcase/fabricas",methods=['GET'])
def Pesquisa_Fabricas():
    cursor_fabricas = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(FABRICA) FROM VOBs where FABRICA is not '' and FABRICA is not null")
    FABRICAS = cursor_fabricas.fetchone()

    Lista_fabricas = []
    while FABRICAS:
        saida = {'FABRICA': FABRICAS[0].strip()}
        Lista_fabricas.append(saida)

        FABRICAS = cursor_fabricas.fetchone()

    return render_template('index.html',retornos=Lista_fabricas)


@app.route("/clearcase/fabricas/<COMUNIDADE>",methods=['GET'])
def Pesquisa_fabricas_Comunidade(COMUNIDADE):
    cursor_fabricas = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(FABRICA) FROM VOBs where trim(COMUNIDADE) = '{COMUNIDADE}' and FABRICA is not null and FABRICA is not ''")
    fabricas = cursor_fabricas.fetchone()

    Lista_fabricas = []
    while fabricas:
        saida = {'Fabrica': fabricas[0]}
        Lista_fabricas.append(saida)

        fabricas = cursor_fabricas.fetchone()

    return render_template('index.html',retornos=Lista_fabricas)


@app.route("/clearcase/fabrica/<FABRICA>",methods=['GET'])
def Pesquisa_VOBs_Fabrica(FABRICA):
    cursor_VOBs = BancodeDados.ConsultaSQL(f"SELECT VOB, COMUNIDADE,FABRICA FROM VOBs where trim(FABRICA) = '{FABRICA}'")
    VOBs = cursor_VOBs.fetchone()

    Lista_VOBs = []
    while VOBs:
        saida = {'VOB': VOBs[0],'comunidade': VOBs[1],'fabrica': VOBs[2] }
        Lista_VOBs.append(saida)

        VOBs = cursor_VOBs.fetchone()

    return jsonify(Lista_VOBs)


@app.route("/clearcase/acl/<COMUNIDADE>/<FABRICA>",methods=['GET'])
def Pesquisa_ACL_VOB(COMUNIDADE,FABRICA):
    cursor_grupos = BancodeDados.ConsultaSQL(f"SELECT DISTINCT(GRUPO_COMPART) FROM COMPARTILHAMENTOS WHERE GRUPO_COMPART like '%{COMUNIDADE}%' AND GRUPO_COMPART like '%{FABRICA}%'")
    grupos = cursor_grupos.fetchone()
    grupos_fabrica=[]
    while grupos:
        grupos_fabrica.append(f"{grupos[0]}")
        grupos = cursor_grupos.fetchone()

    saida = []
    saida.append("Rolemap_leitura")
    saida.append("")
    saida.append(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}")
    for grupo in grupos_fabrica:
        saida.append(f"Role:Leitura --> Group:CORPCAIXA\{grupo}")
    saida.append("")
    saida.append("")

    saida.append("Rolemap_caixa")
    saida.append("")
    saida.append(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL")
    saida.append(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}")
    for grupo in grupos_fabrica:
        saida.append(f"Role:Leitura --> Group:CORPCAIXA\{grupo}")
    grupos = cursor_grupos.fetchall()
    saida.append("")
    saida.append("")

    saida.append("Rolemap_desenvolvimento")
    saida.append("")
    saida.append(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL")
    saida.append(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}")
    for grupo in grupos_fabrica:
        saida.append(f"Role:Escrita --> Group:CORPCAIXA\{grupo}")
    saida.append("")
    saida.append("")

    saida.append("Rolemap_metrica")
    saida.append("")
    saida.append(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}")
    saida.append(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 Metricas")
    for grupo in grupos_fabrica:
        saida.append(f"Role:Leitura --> Group:CORPCAIXA\{grupo}")
    saida.append("")
    saida.append("")

    saida.append("Rolemap_certificacao")
    saida.append("")
    saida.append(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}")
    saida.append(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO")
    for grupo in grupos_fabrica:
        saida.append(f"Role:Leitura --> Group:CORPCAIXA\{grupo}")
    saida.append("")
    saida.append("")

    saida.append("Rolemap_todos")
    saida.append("")
    saida.append(f"Role:ADM --> Group:CORPCAIXA\G DF5222 CC_ADM")
    saida.append(f"Role:Leitura --> Group:CORPCAIXA\G DF5222 CC_TRANSVERSAL")
    saida.append(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_{COMUNIDADE}")
    saida.append(f"Role:Escrita --> Group:CORPCAIXA\G DF5222 CC_CERTIFICACAO")
    for grupo in grupos_fabrica:
        saida.append(f"Role:Escrita --> Group:CORPCAIXA\{grupo}")
    saida.append("")
    saida.append("")

    return render_template('index.html',retornos=saida)


# Verifica se esta sendo chamado por um interpretador python ou executavel
if sys.argv[0].find(".exe") > -1:
	caminho = sys.path[2]
else:
	caminho = sys.path[0]

# Abre a conexao do banco de dados
BancodeDados = SQLite("Clearcase.db")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
