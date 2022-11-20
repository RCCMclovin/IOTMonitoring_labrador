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
intervalo = Intervalo()

#Conexão com a porta serial
try:
    serialPort = serial.Serial(port = "COM5", baudrate=9600,
                           bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)
except:
    raise Exception("Erro ao conectar ao Serial")

#Leitura da séria histórica e inicialização dos parâmetros
try:
    serie = fopen()
    mat, l = gerar_matriz(serie, w=janela)
    intervalo.update(l)
except: 
    #Não há série histórica, deverá ser construída
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
    intervalo.update(l)

#Variáveis de controle
atualizar = 0
ultima_janela = serie[-1*janela::]

#Loop de execução
while True:
    line = serialPort.readline().decode().strip()                            #Leitura do serial
    if '*' in line:                                                          #Se a linha contém dados
        print(line)
        dado = float(line.split("*")[1])                                     #Separar o dado
        print("Nova Leitura:", dado)
        IP = intervalo.get_margem()                                          #Definir Intervalo de Predição
        predicao = KNN_predict(ultima_janela, mat, l, k=k, size=len(l))      #Predição
        print(f"Intervalo de predição: [{predicao-IP},{predicao+IP}]")
        if dado >= predicao-IP and dado <= predicao+IP:
            print("Leitura dentro do intervalo.")
            update(dado)
            conexao.publish(msg=f"Nova Leitura: {dado}")                    #Publicar dado
            atualizar += 1
            ultima_janela = ultima_janela[1::]+[dado]
        else:
            print("Leitura fora do intervalo.")
            conexao.publish(msg=f"Nova Leitura Possivelmente Alterada: {dado}") #Publicar dado possivelmente alterado
    
    if atualizar == n_atualizar:                                            #Atualizando variáveis internas
        print("Atualizando bancos de dados")
        atualizar=0
        serie = fopen()
        mat, l = gerar_matriz(serie, w=janela)
        intervalo.update(l)




