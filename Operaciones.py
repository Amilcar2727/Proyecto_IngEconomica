from decimal import Decimal; #Libreria para redondeo
class OperacionesMF:
    @staticmethod
    def Redondeo(resultado,numeroDecimales):
        numero = 1/(10**numeroDecimales);
        presicion = Decimal(str(numero));#1/10**n
        return Decimal(resultado).quantize(presicion);
    @staticmethod
    def ConversionTiempo(tiempo,tazaT,periodoT):
        if(tazaT=="Diario"):
            if(periodoT=="Semanal"):
                tiempo=tiempo*7;
            elif(periodoT=="Mensual"):
                tiempo=tiempo*30;
            elif(periodoT=="Anual"):
                tiempo=tiempo*365;
        elif(tazaT=="Semanal"):
            if(periodoT=="Diario"):
                tiempo=tiempo/7;
            elif(periodoT=="Mensual"):
                tiempo=tiempo*4.345;
            elif(periodoT=="Anual"):
                tiempo=tiempo*52;
        elif(tazaT=="Mensual"):
            if(periodoT=="Diario"):
                tiempo=tiempo/30;
            elif(periodoT=="Semanal"):
                tiempo=tiempo/4.345;
            elif(periodoT=="Anual"):
                tiempo=tiempo*12;
        elif(tazaT=="Anual"):
            if(periodoT=="Diario"):
                tiempo=tiempo/365;
            if(periodoT=="Semanal"):
                tiempo=tiempo/52;
            elif(periodoT=="Mensual"):
                tiempo=tiempo/12;
        return OperacionesMF.Redondeo(tiempo,6);
    @staticmethod
    def InteresSimpleAcumulado(capital,tazaInteres,tazaTiempo,tazaFormato,periodo,periodoTiempo):   
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            #Si el tiempo de la taza es diferente al del periodo
            if(tazaTiempo != periodoTiempo):
                periodo=OperacionesMF.ConversionTiempo(periodo,tazaTiempo,periodoTiempo);
            periodo=float(periodo);
            if(tazaFormato=="porcentaje"):
                print(periodo);
                result = capital*(tazaInteres/100)*periodo;
            elif(tazaFormato=="decimal"):
                result = capital*tazaInteres*periodo;
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalSimpleFuturo(capital,interes):
        try:
            capital = float(capital);
            interes = float(interes);
            result = capital+interes;
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;
    
    @staticmethod
    def InteresCompuestoAcumulado(capital,tazaInteres,tazaTiempo,tazaFormato,periodo,periodoTiempo):   
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            #Si el tiempo de la taza es diferente al del periodo
            if(tazaTiempo != periodoTiempo):
                periodo=OperacionesMF.ConversionTiempo(periodo,tazaTiempo,periodoTiempo);
            periodo=float(periodo);
            if(tazaFormato=="porcentaje"):
                result = capital*((((tazaInteres/100)+1)**periodo)-1);
            elif(tazaFormato=="decimal"):
                result = capital*((((tazaInteres)+1)**periodo)-1);
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalCompuestoFuturo(capital,tazaInteres,tazaTiempo,tazaFormato,periodo,periodoTiempo):
        try:
            capital = float(capital);
            tazaInteres = float(tazaInteres);
            periodo = float(periodo);
            #Si el tiempo de la taza es diferente al del periodo
            if(tazaTiempo != periodoTiempo):
                periodo=OperacionesMF.ConversionTiempo(periodo,tazaTiempo,periodoTiempo);
            periodo=float(periodo);
            if(tazaFormato=="porcentaje"):
                result = capital*((1+(tazaInteres/100))**periodo);
            elif(tazaFormato=="decimal"):
                result = capital*((1+(tazaInteres))**periodo);
            return OperacionesMF.Redondeo(result,2);
        except ValueError:
            pass;