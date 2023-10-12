import sys
import os

with open(sys.path[0] + '\Incidentes_abertos - Hudson.csv',mode='r',encoding='UTF-8') as entrada:
    for linha in entrada:
        linha = linha.upper()

        PROJETO = linha[0:5]
        ID_RTC = linha[6:14]
        STATUS = linha[15:-1]

        if os.path.isfile(sys.path[0] + f"\{PROJETO}.csv") == False:
            saida = open(sys.path[0] + f"\{PROJETO}.csv",mode='at',encoding='UTF-8')
            saida.write(f"ID;STATUS\n")

        saida.write(f"{ID_RTC};{STATUS}\n")