from componentes.file import *
from componentes.preprocess import *
from componentes.knn import *
from componentes.intervalo import *
from componentes.mqtt import MQTT
import serial

max_entradas=30
n_atualizar=5
janela=4
k = 3

conexao = MQTT()
conexao.setup()

try:
    serialPort = serial.Serial(port = "COM5", baudrate=9600,
                           bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
except:
    raise Exception("Erro ao conectar ao Serial")

try:
    serie = fopen()
    mat, l = gerar_matriz(serie, w=janela)
except: 
    print("Sem dados para Iniciar o modelo.")
    print(f"Serão feitas {max_entradas} leituras para iniciar o modelo.")
    n_entradas=0
    entradas = []
    while n_entradas<max_entradas:
        line = serialPort.readline().decode().strip()
        if '*' in line:
            print(line)
            dado = float(line.split("*")[1])
            print("Nova Leitura:", dado)
            conexao.publish(msg=f"Nova Leitura: {dado}")
            entradas.append(dado)
            n_entradas+=1
    create_csv(entradas)
    print("Arquivo de entrada inicializado.")
    serie = fopen()
    mat, l = gerar_matriz(serie, w=janela)

atualizar = 0
while True:
    line = serialPort.readline().decode().strip()
    if '*' in line:
        print(line)
        dado = float(line.split("*")[1])
        print("Nova Leitura:", dado)
        margem_de_erro = margem()
        last4 = serie[-4::]
        predicao = KNN_predict(last4, mat, l, k=k, size=len(mat))
        print(f"Intervalo de predição: [{predicao-margem_de_erro},{predicao+margem_de_erro}]")
        if dado >= predicao-margem_de_erro and dado <= predicao+margem_de_erro:
            print("Leitura dentro do intervalo.")
            update(dado)
            conexao.publish(msg=f"Nova Leitura: {dado}")
            atualizar = 1
        else:
            print("Leitura fora do intervalo.")
            conexao.publish(msg=f"Nova Leitura Possivelmente Alterada: {dado}")
    
    if atualizar == n_atualizar:
        atualizar=0
        serie = fopen()
        mat, l = gerar_matriz(serie, w=janela)




