from numpy import array
import numpy as np
#from scipy.stats import norm
import math

dados = np.array([26, 30, 27, 25, 25, 26, 27, 30, 28, 25, 26, 26, 25, 29, 26, 25, 24, 24, 24, 28, 26, 24, 23, 24, 23, 28])

n = len(dados)
media = np.mean(dados)
desvio_padrao = np.std(dados)
alfa = 0.05 #definindo nivel de confiança do calculo como 95%
z = np.linalg.norm.ppf(1- alfa) 

lim_inferior = media - z * (desvio_padrao / math.sqrt(n))
lim_inferior

lim_superior = media + z * (desvio_padrao / math.sqrt(n))
lim_superior

margem_erro = abs(media - lim_superior)
margem_erro
