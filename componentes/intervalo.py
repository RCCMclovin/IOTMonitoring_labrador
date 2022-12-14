from numpy import std, mean
from numpy.linalg import norm

class Intervalo:
    def __init__(self):
        pass
    def update(self, predictions):
        media = mean(predictions)
        desvio = std(predictions)
        zscore = [(i - media)/desvio for i in predictions]
        z = norm(zscore)
        self.margem = z * desvio * (1+1/len(predictions))**0.5
    
    def get_margem(self):
        return self.margem