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