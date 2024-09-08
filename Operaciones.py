class OperacionesMF:
    def InteresAcumulado(self,capital,tazaInteres,periodo):    
        return capital*(tazaInteres/10)*periodo;
    def CapitalFuturo(self,capital,interes):
        return capital+interes;