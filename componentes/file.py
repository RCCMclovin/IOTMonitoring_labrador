"""
Controle do arquivo de entrada
"""

def fopen(path="./SH_temperaturas.csv"):
    file = open(path, "r")
    serie = [float(i.replace(",","")) for i in file.readlines() if len(i) > 0]
    file.close()
    return serie

def update(nova, path="./SH_temperaturas.csv", lenmax = 30):
    file = open(path, "r")
    serie = [float(i.replace(",","")) for i in file.readlines() if len(i) > 0]
    file.close()
    serie.append(nova)
    while len(serie) > lenmax:
        serie=serie[1::]
    file = open(path,"w")
    for i in serie:
        file.write(str(i)+",\n")
    file.close()
    return serie

def create_csv(entradas, path="./SH_temperaturas"):
    file = open(path,"w")
    for i in entradas:
        file.write(str(i)+",\n")
    file.close()

