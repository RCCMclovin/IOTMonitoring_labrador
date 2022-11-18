from numpy import array
def gerar_matriz(serie, w=4, s=0):
    mat = []
    l = serie[w:]
    while s < len(serie)-w:
        mat.append(serie[s:s+w])
        s+=1
    return (array(mat),l)