from componentes.file import *
from componentes.preprocess import *
from componentes.knn import *

mat, l = gerar_matriz(fopen())

print(KNN_predict([20,22,20,20], mat, l, size=len(l)))

update(25)