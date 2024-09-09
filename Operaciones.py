class OperacionesMF:
    def InteresAcumulado(self,capital,tazaInteres,periodo):   
        try:
            capital = int(capital);
            tazaInteres = float(tazaInteres);
            periodo = int(periodo);
            
            return capital*(tazaInteres/100)*periodo;
        except ValueError:
            pass;
        
        
    def CapitalFuturo(self,capital,interes):
        try:
            capital = int(capital);
            interes = int(interes);
            return capital+interes;
        except ValueError:
            pass;