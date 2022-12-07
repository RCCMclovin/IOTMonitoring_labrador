from componentes.file import *
from componentes.knn import *
from componentes.intervalo import Intervalo
from componentes.mqtt import MQTT
import serial
#Hiperparâmetros
max_entradas=30  #Tamanho da série histórica
n_atualizar=5    #Quantidade de amostras antes de atualizar as variáveis
janela=4         #Tamnho da janela da matriz
k = 3            #Número de vizinhos no KNN

#Inicializando a conexão MQTT
conexao = MQTT()
conexao.setup()

#Inicializando o intervalo
intervalo_temp = Intervalo()
#intervalo_turb = Intervalo()

#Conexão com a porta serial
try:
    serialPort = serial.Serial(port = "/dev/ttyACM1", baudrate=9600,
                           bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
except:
    raise Exception("Erro ao conectar ao Serial")

#Leitura da séria histórica e inicialização dos parâmetros
try:
    serie_temp = fopen(path="./SH_temperaturas.csv")
    mat_temp, l_temp = gerar_matriz(serie_temp, w=janela)
    intervalo_temp.update(l_temp)
    """
    serie_turb = fopen(path="./SH_turbidez.csv")
    mat_turb, l_turb = gerar_matriz(serie_turb, w=janela)
    intervalo_turb.update(l_turb)
    """
except: 
    #Não há série histórica, deverá ser construída
    print("Sem dados para Iniciar o modelo.")
    print(f"Serão feitas {max_entradas} leituras para iniciar o modelo.")
    n_entradas=0
    entradas_temp = []
    #entradas_turb = []
    while n_entradas<max_entradas:
        line = serialPort.readline().decode().strip()
        if '*' in line:
            print(line)
            print(line.split("*"))
            temp = float(line.split("*")[1])
            #turb = float(line.split("*")[2])
            print("Nova Leitura de Temperatura:", temp)
            conexao.publish(msg=f"Nova Leitura de Temperatura: {temp}")
            entradas_temp.append(temp)
            """
            print("Nova Leitura de Turbidez:", turb)
            conexao.publish(msg=f"Nova Leitura de Turbidez: {turb}")
            entradas_turb.append(turb)
            """
            n_entradas+=1
    create_csv(entradas_temp, path="./SH_temperaturas.csv")
    #create_csv(entradas_turb, path="./SH_turbidez.csv")
    print("Arquivo de entrada inicializado.")
    serie_temp = fopen(path="./SH_temperaturas.csv")
    mat_temp, l_temp = gerar_matriz(serie_temp, w=janela)
    intervalo_temp.update(l_temp)
    
    """
    serie_turb = fopen(path="./SH_turbidez.csv")
    mat_turb, l_turb = gerar_matriz(serie_turb, w=janela)
    intervalo_turb.update(l_turb)
    """

#Variáveis de controle
atualizar = 0
ultima_janela_temp = serie_temp[-1*janela::]
#ultima_janela_turb = serie_turb[-1*janela::]

#Loop de execução
while True:
    line = serialPort.readline().decode().strip()                            #Leitura do serial
    if '*' in line:                                                          #Se a linha contém dados
        print(line)
        temp = float(line.split("*")[1])
        #turb = float(line.split("*")[2])
        print("Nova Leitura de Temperatura:", temp)
        IP = intervalo_temp.get_margem()                                          #Definir Intervalo de Predição
        predicao = KNN_predict(ultima_janela_temp, mat_temp, l_temp, k=k, size=len(l_temp))      #Predição
        print(f"Intervalo de predição de Temperatura: [{predicao-IP},{predicao+IP}]")
        if temp >= predicao-IP and temp <= predicao+IP:
            print("Leitura de Temperatura dentro do intervalo.")
            update(temp, path="./SH_temperaturas.csv", lenmax=max_entradas)
            conexao.publish(msg=f"Nova Leitura de Temperatura: {temp}")                    #Publicar dado
            atualizar += 1
            ultima_janela_temp = ultima_janela_temp[1::]+[temp]
        else:
            print("Leitura de Temperatura fora do intervalo.")
            conexao.publish(msg=f"Nova Leitura de Temperatura Possivelmente Alterada: {temp}") #Publicar dado possivelmente alterado
        
        """
        print("Nova Leitura de Turbidez:", turb)
        IP = intervalo_turb.get_margem()                                          #Definir Intervalo de Predição
        predicao = KNN_predict(ultima_janela_turb, mat_turb, l_turb, k=k, size=len(l_turb))      #Predição
        print(f"Intervalo de predição de Turbidez: [{predicao-IP},{predicao+IP}]")
        if turb >= predicao-IP and turb <= predicao+IP:
            print("Leitura de Turbidez dentro do intervalo.")
            update(turb, path="./SH_turbidez.csv", lenmax=max_entradas)
            conexao.publish(msg=f"Nova Leitura de Turbidez: {turb}")                    #Publicar dado
            atualizar += 1
            ultima_janela_turb = ultima_janela_turb[1::]+[turb]
        else:
            print("Leitura de Turbidez fora do intervalo.")
            conexao.publish(msg=f"Nova Leitura de Turbidez Possivelmente Alterada: {turb}") #Publicar dado possivelmente alterado
    """
    if atualizar == n_atualizar:                                            #Atualizando variáveis internas
        print("Atualizando bancos de dados")
        atualizar=0
        serie_temp = fopen(path="./SH_temperaturas.csv")
        mat_temp, l_temp = gerar_matriz(serie_temp, w=janela)
        intervalo_temp.update(l_temp)
        """
        serie_turb = fopen(path="./SH_turbidez.csv")
        mat_turb, l_turb = gerar_matriz(serie_turb, w=janela)
        intervalo_turb.update(l_turb)
        """



