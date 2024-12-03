from decimal import Decimal; #Libreria para redondeo
class OperacionesMF:
    @staticmethod
    def Redondeo(resultado,numeroDecimales):
        numero = 1/(10**numeroDecimales);
        presicion = Decimal(str(numero));#1/10**n
        return Decimal(resultado).quantize(presicion);
    @staticmethod
    def ConversionTiempo(tasaInteres,tasaT,periodoT):
        if(tasaT=="Diario"):
            if(periodoT=="Semanal"):
                tasaInteres*=7;
            elif(periodoT=="Mensual"):
                tasaInteres*=30;
            elif(periodoT=="Anual"):
                tasaInteres*=365;
        elif(tasaT=="Semanal"):
            if(periodoT=="Diario"):
                tasaInteres/=7;
            elif(periodoT=="Mensual"):
                tasaInteres*=4.345;
            elif(periodoT=="Anual"):
                tasaInteres*=52;
        elif(tasaT=="Mensual"):
            if(periodoT=="Diario"):
                tasaInteres/=30;
            elif(periodoT=="Semanal"):
                tasaInteres/=4.345;
            elif(periodoT=="Anual"):
                tasaInteres*=12;
        elif(tasaT=="Anual"):
            if(periodoT=="Diario"):
                tasaInteres/=365;
            if(periodoT=="Semanal"):
                tasaInteres/=52;
            elif(periodoT=="Mensual"):
                tasaInteres/=12;
        result = float(OperacionesMF.Redondeo(tasaInteres,6));
        return result;
    @staticmethod
    def Convertir_ComaPunto(valor):
        return valor.replace(',', '.');
    @staticmethod
    def InteresSimpleAcumulado(capital,tasaInteres,tasaTiempo,tasaFormato,periodo,periodoFormato):
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            tasaInteres = float(OperacionesMF.Convertir_ComaPunto(tasaInteres));
            if(tasaFormato=="porcentaje"):
                tasaInteres = tasaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la tasa es diferente al del periodo
            if(tasaTiempo != periodoFormato):
                tasaInteres=OperacionesMF.ConversionTiempo(tasaInteres,tasaTiempo,periodoFormato);
            result = capital*tasaInteres*periodo;
            return float(OperacionesMF.Redondeo(result,2));
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalSimpleFuturo(capital,interes):
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            interes = float(interes);
            result = capital+interes;
            return float(OperacionesMF.Redondeo(result,2));
        except ValueError:
            pass;
    
    @staticmethod
    def InteresCompuestoAcumulado(capital,tasaInteres,tasaTiempo,tasaFormato,periodo,periodoFormato):   
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            tasaInteres = float(OperacionesMF.Convertir_ComaPunto(tasaInteres));
            if(tasaFormato=="porcentaje"):
                tasaInteres = tasaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la tasa es diferente al del periodo
            if(tasaTiempo != periodoFormato):
                tasaInteres=OperacionesMF.ConversionTiempo(tasaInteres,tasaTiempo,periodoFormato);
            result = capital*((((tasaInteres)+1)**periodo)-1);
            return float(OperacionesMF.Redondeo(result,2));
        except ValueError:
            pass;
    
    @staticmethod
    def CapitalCompuestoFuturo(capital,tasaInteres,tasaTiempo,tasaFormato,periodo,periodoFormato):
        try:
            capital = float(OperacionesMF.Convertir_ComaPunto(capital));
            tasaInteres = float(OperacionesMF.Convertir_ComaPunto(tasaInteres));
            if(tasaFormato=="porcentaje"):
                tasaInteres = tasaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la tasa es diferente al del periodo
            if(tasaTiempo != periodoFormato):
                tasaInteres=OperacionesMF.ConversionTiempo(tasaInteres,tasaTiempo,periodoFormato);
            result = capital*((1+(tasaInteres))**periodo);
            return float(OperacionesMF.Redondeo(result,2));
        except ValueError:
            pass;
    
    # ===== METODOS PARA AMORTIZACIÓN =====:
    ## ===> FRANCES <===
    """Metodo para calcular Cuota(C):"""
    @staticmethod
    def CalcularCuotaFrances(Deuda,tasaInteres,tasaTiempo,tasaFormato,periodo,periodoFormato):
        try:
            #Codigo aqui:
            Deuda = float(OperacionesMF.Convertir_ComaPunto(str(Deuda)));
            tasaInteres = float(OperacionesMF.Convertir_ComaPunto(str(tasaInteres)));
            if(tasaFormato=="porcentaje"):
                tasaInteres = tasaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la tasa es diferente al del periodo
            if(tasaTiempo != periodoFormato):
                tasaInteres=OperacionesMF.ConversionTiempo(tasaInteres,tasaTiempo,periodoFormato);
            #Calcular la cuota
            num = Deuda * tasaInteres * ((1+tasaInteres)**periodo);
            dem = (((1+tasaInteres)**periodo) - 1);
            cuota = num/dem;
            return float(OperacionesMF.Redondeo(cuota,2));
        except ValueError:
            pass;
    @staticmethod
    def PagoTotalFrances(cuota,periodo):
        try:
            #Codigo aqui:
            pagoT = float(cuota)*float(periodo);
            return float(OperacionesMF.Redondeo(pagoT,2));
        except ValueError:
            pass;
    #------------ TABLA ------------
    
    ## ===> ALEMAN <===
    @staticmethod
    def CalcularAmortizacionAleman(Deuda,periodo):
        try:
            Deuda = float(OperacionesMF.Convertir_ComaPunto(str(Deuda)));
            periodo = float(periodo);
            AmortFija = Deuda/periodo;
            return float(OperacionesMF.Redondeo(AmortFija,2));
        except ValueError:
            pass;
    @staticmethod
    def InteresTotalesAleman(Deuda,tasaInteres,tasaTiempo,tasaFormato,periodo,periodoFormato):
        try:
            Deuda = float(OperacionesMF.Convertir_ComaPunto(str(Deuda)));
            tasaInteres = float(OperacionesMF.Convertir_ComaPunto(str(tasaInteres)));
            if(tasaFormato=="porcentaje"):
                tasaInteres = tasaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la tasa es diferente al del periodo
            if(tasaTiempo != periodoFormato):
                tasaInteres=OperacionesMF.ConversionTiempo(tasaInteres,tasaTiempo,periodoFormato);
            #Calcular el interes
            interesT = tasaInteres*(Deuda*(periodo+1)/2)
            return float(OperacionesMF.Redondeo(interesT,2));
        except ValueError:
            pass;
    @staticmethod
    def PagoTotalAleman(Deuda,interesesT):
        try:
            Deuda = float(OperacionesMF.Convertir_ComaPunto(str(Deuda)));
            pagoT = Deuda + interesesT;
            return float(OperacionesMF.Redondeo(pagoT,2));
        except ValueError:
            pass;
    ## ===> AMERICANA <===
    @staticmethod
    def CalcularInteresesAmericano(Deuda,tasaInteres,tasaTiempo,tasaFormato,periodo,periodoFormato):
        try:
            Deuda = float(OperacionesMF.Convertir_ComaPunto(str(Deuda)));
            tasaInteres = float(OperacionesMF.Convertir_ComaPunto(str(tasaInteres)));
            if(tasaFormato=="porcentaje"):
                tasaInteres = tasaInteres/100;
            periodo = float(periodo);
            #Si el tiempo de la tasa es diferente al del periodo
            if(tasaTiempo != periodoFormato):
                tasaInteres=OperacionesMF.ConversionTiempo(tasaInteres,tasaTiempo,periodoFormato);
            #Calcular Interes
            interesPeriodico = Deuda * tasaInteres;
            return float(OperacionesMF.Redondeo(interesPeriodico,2));
        except ValueError:
            pass;
    @staticmethod
    def InteresTotalesAmericano(InteresPeriodico, periodo):
        try:
            periodo = float(periodo);
            interesesTotales = InteresPeriodico * periodo;
            return float(OperacionesMF.Redondeo(interesesTotales,2));
        except ValueError:
            pass;
    @staticmethod
    def PagoTotalAmericano(Deuda,interesTotales):
        try:
            Deuda = float(OperacionesMF.Convertir_ComaPunto(str(Deuda)));
            #Codigo aqui:
            pagoT = Deuda+interesTotales;
            return float(OperacionesMF.Redondeo(pagoT,2));
        except ValueError:
            pass;
    ### ============== CALCULAR DEPRECIACION LINEA RECTA ============= ###
    @staticmethod
    def DepreciacionLR(costoActivoFijo,valorDeRescate,periodo):
        try:
            costoAF = float(OperacionesMF.Convertir_ComaPunto(costoActivoFijo));
            valorR = float(OperacionesMF.Convertir_ComaPunto(valorDeRescate));
            periodo = float(periodo);
            #Calcular Depreciacion
            depreciacion = (costoAF-valorR)/periodo;
            return float(OperacionesMF.Redondeo(depreciacion,2));
        except ValueError:
            pass;