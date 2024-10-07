from decimal import Decimal; #Libreria para redondeo
class OperacionesMF:
    @staticmethod
    def Redondeo(resultado,numeroDecimales):
        numero = 1/(10**numeroDecimales);
        presicion = Decimal(str(numero));#1/10**n
        return Decimal(resultado).quantize(presicion);
    @staticmethod
    def ConversionTiempo(tazaInteres,tazaT,periodoT):
        if(tazaT=="Diario"):
            if(periodoT=="Semanal"):
                tazaInteres*=7;
            elif(periodoT=="Mensual"):
                tazaInteres*=30;
            elif(periodoT=="Anual"):
                tazaInteres*=365;
        elif(tazaT=="Semanal"):
            if(periodoT=="Diario"):
                tazaInteres/=7;
            elif(periodoT=="Mensual"):
                tazaInteres*=4.345;
            elif(periodoT=="Anual"):
                tazaInteres*=52;
        elif(tazaT=="Mensual"):
            if(periodoT=="Diario"):
                tazaInteres/=30;
            elif(periodoT=="Semanal"):
                tazaInteres/=4.345;
            elif(periodoT=="Anual"):
                tazaInteres*=12;
        elif(tazaT=="Anual"):
            if(periodoT=="Diario"):
                tazaInteres/=365;
            if(periodoT=="Semanal"):
                tazaInteres/=52;
            elif(periodoT=="Mensual"):
                tazaInteres/=12;
        return float(OperacionesMF.Redondeo(tazaInteres,6));
    @staticmethod
    def Convertir_ComaPunto(valor):
        return valor.replace(',', '.');
    @staticmethod
    def InteresSimpleAcumulado(capital,tazaInteres,tazaTiempo,tazaFormato,periodo,periodoTiempo):   
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            tazaInteres = float(OperacionesMF.Convertir_ComaPunto(tazaInteres));
            if(tazaFormato=="porcentaje"):
                tazaInteres = tazaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la taza es diferente al del periodo
            if(tazaTiempo != periodoTiempo):
                tazaInteres=OperacionesMF.ConversionTiempo(tazaInteres,tazaTiempo,periodoTiempo);
            result = capital*tazaInteres*periodo;
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalSimpleFuturo(capital,interes):
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            interes = float(interes);
            result = capital+interes;
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;
    
    @staticmethod
    def InteresCompuestoAcumulado(capital,tazaInteres,tazaTiempo,tazaFormato,periodo,periodoTiempo):   
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            tazaInteres = float(OperacionesMF.Convertir_ComaPunto(tazaInteres));
            if(tazaFormato=="porcentaje"):
                tazaInteres = tazaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la taza es diferente al del periodo
            if(tazaTiempo != periodoTiempo):
                tazaInteres=OperacionesMF.ConversionTiempo(tazaInteres,tazaTiempo,periodoTiempo);
            result = capital*((((tazaInteres)+1)**periodo)-1);
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalCompuestoFuturo(capital,tazaInteres,tazaTiempo,tazaFormato,periodo,periodoTiempo):
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            tazaInteres = float(OperacionesMF.Convertir_ComaPunto(tazaInteres));
            if(tazaFormato=="porcentaje"):
                tazaInteres = tazaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la taza es diferente al del periodo
            if(tazaTiempo != periodoTiempo):
                tazaInteres=OperacionesMF.ConversionTiempo(tazaInteres,tazaTiempo,periodoTiempo);
            result = capital*((1+(tazaInteres))**periodo);
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;
    
    # ===== CREAR METODOS PARA AMORTIZACIÓN =====:
    """TODO: Metodo para calcular Cuota(C):"""
    @staticmethod
    def CalcularCuotaAmortizacion():
        try:
            #Codigo aqui:
            return;
        except ValueError:
            pass;
    
    """TODO: Metodo para calcular Interez(C)"""
    @staticmethod
    def InteresAmortizacion():
        try:
            #Codigo aqui:
            return;
        except ValueError:
            pass;
        
    """TODO: Metodo para calcular Amortizacion(A): Amortizacion = Cuota - interes"""
    @staticmethod
    def CalcularAmortizacion():
        try:
            #Codigo aqui:
            return;
        except ValueError:
            pass;
        
    """TODO: Metodo para calcular Saldo del préstamo(S): Saldo pendiente"""
    @staticmethod
    def CalcularSaldoPendiente():
        try:
            #Codigo aqui:
            return;
        except ValueError:
            pass;