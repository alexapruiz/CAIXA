import os, sys

#currentdir = os.path.dirname(os.path.realpath(__file__))
#parentdir = os.path.dirname(currentdir)
#sys.path.append(parentdir)
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from Funcoes import BancodeDados

MyDB = BancodeDados.SQLite(sys.path[0] + '\Clearcase.db')

cursor_X = MyDB.ConsultaSQL('SELECT * FROM VOBS')
VOBs = cursor_X.fetchone()

while VOBs:
    print(VOBs[0])
    VOBs = cursor_X.fetchone()
