class OperacionesMF:
    def InteresAcumulado(self,capital,tazaInteres,periodo):   
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            
            return capital*(tazaInteres/100)*periodo;
        except ValueError:
            pass;
        
        
    def CapitalFuturo(self,capital,interes):
        try:
            capital = float(capital);
            interes = float(interes);
            return capital+interes;
        except ValueError:
            pass;