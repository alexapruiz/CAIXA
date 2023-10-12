from socket import timeout
import pyodbc
import sqlite3

class SQLServer():

    def __init__(self,DATABASE):
        self.StringConexao = 'DRIVER=SQL Server;SERVER=NOVO\SQLEXPRESS;PORT=1433;DATABASE=' + DATABASE + ';Trustedconnection=yes'

    def ConsultaSQL(self, ComandoSQL) -> object:
        try:
            conn = pyodbc.connect(self.StringConexao)
            cursor = conn.cursor()
            cursor.execute(ComandoSQL)
            return cursor
        except pyodbc.DatabaseError as err:
            return err.args[0]

    def ExecutaComandoSQL(self, ComandoSQL):
        try:
            conn = pyodbc.connect(self.StringConexao)
            cursor = conn.cursor()
            cursor.execute(ComandoSQL)
            conn.commit()

            return 0
        except pyodbc.DatabaseError as err:
            return err.args[1]


class SQLite():

    def __init__(self,arquivo):
        self.Database = arquivo
        
    def ConsultaSQL(self,ComandoSQL) -> object:
        try:
            conexao = sqlite3.connect(self.Database, timeout=30.0, check_same_thread=False, isolation_level=None)
            conexao.execute('pragma journal_mode=wal;')
            cursor = conexao.cursor()
            cursor.execute(ComandoSQL)
            return cursor
        except pyodbc.DatabaseError as err:
            return err.args[0]


    def ExecutaComandoSQL(self,ComandoSQL) -> object:
        try:
            conexao = sqlite3.connect(self.Database)
            conexao.execute(ComandoSQL)
            conexao.commit()
            conexao.close()
            return True
        except pyodbc.DatabaseError as err:
            return err.args[0]