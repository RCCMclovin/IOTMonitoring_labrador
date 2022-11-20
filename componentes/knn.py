from numpy import array

# Gerando matrizes de entrada e labels para o KNN
def gerar_matriz(serie, w=4, s=0):
    mat = []
    l = serie[w:]
    while s < len(serie)-w:
        mat.append(serie[s:s+w])
        s+=1
    return (array(mat),l)

# Distância Euclidiana
def dist(a, b):
    return (sum((a-b)**2))**0.5

# Inserção em lista
def insert(lista, valor):
    valor_nao_esta_na_lista = True
    for i in range(len(lista)):
        if valor[1] < lista[i][1]:
            lista = lista[:i]+[valor]+lista[i:]
            valor_nao_esta_na_lista = False
            break
    if valor_nao_esta_na_lista:
        lista+=[valor]
    return lista

#Execução do algoritmo KNN para prever a próxima entrada
def KNN_predict(alvo, matriz, labels, k = 3, size = 26):
    nn = []
    for i in range(size):
        d = dist(alvo,matriz[i])
        nn = insert(nn, (matriz[i], d, labels[i]))
        nn = nn[:k:]
            
    return sum([d[2] for d in nn])/k