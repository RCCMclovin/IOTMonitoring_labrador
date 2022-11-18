from componentes.tools import dist, insert

#Execução do algoritmo KNN para prever a próxima entrada
def KNN_predict(alvo, matriz, labels, k = 3, size = 26):
    nn = []
    for i in range(size):
        d = dist(alvo,matriz[i])
        nn = insert(nn, (matriz[i], d, labels[i]))
        nn = nn[:k:]
            
    return sum([d[2] for d in nn])/k