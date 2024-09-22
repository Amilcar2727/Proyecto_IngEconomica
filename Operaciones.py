from decimal import Decimal; #Libreria para redondeo
class OperacionesMF:
    @staticmethod
    def Redondeo(resultado):
        presicion = Decimal("0.01");
        return Decimal(resultado).quantize(presicion);
    
    @staticmethod
    def InteresSimpleAcumulado(capital,tazaInteres,periodo):   
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            result = capital*(tazaInteres/100)*periodo;
            return OperacionesMF.Redondeo(result);
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalSimpleFuturo(capital,interes):
        try:
            capital = float(capital);
            interes = float(interes);
            result = capital+interes;
            return OperacionesMF.Redondeo(result);
        except ValueError:
            pass;
    
    @staticmethod
    def InteresCompuestoAcumulado(capital,tazaInteres,periodo):   
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            result = capital*((((tazaInteres/100)+1)**periodo)-1);
            return OperacionesMF.Redondeo(result);
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalCompuestoFuturo(capital,interes,periodo):
        try:
            capital = float(capital);
            interes = float(interes);
            periodo = float(periodo);
            result = capital*((1+interes)**periodo);
            return OperacionesMF.Redondeo(result);
        except ValueError:
            pass;