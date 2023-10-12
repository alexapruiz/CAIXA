import subprocess
import sys
import os

#result = subprocess.run([sys.executable, "-c" , "dir"] , capture_output=True )

command = "dir c:\\alex >> c:\\alex\\saida.txt "

if os.system(command) == 0: #Esta função retorna 0 caso deu tudo certo e 1 se deu erro
    print("Executado com sucesso.")
else:
    print("Erro ao executar o comando.")

#retorno = os.system('dir')
#print(retorno)
