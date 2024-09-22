class OperacionesMF:
    def InteresSimpleAcumulado(self,capital,tazaInteres,periodo):   
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            
            return capital*(tazaInteres/100)*periodo;
        except ValueError:
            pass;
        
    def CapitalSimpleFuturo(self,capital,interes):
        try:
            capital = float(capital);
            interes = float(interes);
            return capital+interes;
        except ValueError:
            pass;
        
    def InteresCompuestoAcumulado(self,capital,tazaInteres,periodo):   
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            
            return capital*(((tazaInteres+1)**periodo)-1);
        except ValueError:
            pass;
        
    def CapitalCompuestoFuturo(self,capital,interes,periodo):
        try:
            capital = float(capital);
            interes = float(interes);
            return capital*((1+interes)**periodo);
        except ValueError:
            pass;