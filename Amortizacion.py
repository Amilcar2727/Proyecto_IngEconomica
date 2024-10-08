from tkinter import *
from tkinter import ttk
from Operaciones import OperacionesMF
#Grafico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Verificacion
import re;

class InterfazAmortizacion:
    #Metodo Inicial
    def __init__(self,root):
        self.root = root;
        self.interfazAmort = Toplevel();
        self.interfazAmort.geometry("320x300+250+25");
        self.interfazAmort.title("Calculando Amortizacion");
        self.timer_id = None;
        self.datosBlancos = None;
        self.MenuAmortizacion();
    
    #Interfaz Interes Simple
    def MenuAmortizacion(self):
        self.datos_frame = ttk.Frame(self.interfazAmort,borderwidth=5,relief="solid",width=300, height=300);
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10,padx=10, sticky=(N,E,S,W));
        self.datos_frame.grid_propagate(False);
        
        self.tituloLb = ttk.Label(self.datos_frame, text="CALCULO DE AMORTIZACION",font=("Helvetica", 12, "bold"));
        self.tituloLb.grid(column=0,row=0,columnspan=2,padx=5,pady=10,sticky=(N,S,W));
        self.Check_Deuda_wrapper = (self.datos_frame.register(self.Check_Deuda),"%P");
        self.Check_Interes_wrapper = (self.datos_frame.register(self.Check_Interes),"%P");
        self.Check_Periodo_wrapper = (self.datos_frame.register(self.Check_Periodo),"%P");
        #Lectura Deuda
        self.DeudaInicTxt = StringVar();
        self.DeudaLb = ttk.Label(self.datos_frame, text="Deuda en Soles (P):");
        self.DeudaLb.grid(column=0,row=1,padx=5,pady=5,sticky=W);
        self.Deuda_leer = ttk.Entry(self.datos_frame,textvariable=self.DeudaInicTxt,validate="key",validatecommand=self.Check_Deuda_wrapper);
        self.Deuda_leer.grid(column=1,row=1,padx=5,pady=5,sticky=(W,E));
        
        #Lectura Tasa de Interez:
        self.tasaTxt = StringVar();
        self.tasaIntLb = ttk.Label(self.datos_frame, text="Tasa de Interés (i):");
        self.tasaIntLb.grid(column=0,row=2,padx=4,pady=4,sticky=W);
        self.tasaInput_frame = ttk.Frame(self.datos_frame,width=140, height=25);
        self.tasaInput_frame.grid(column=1, row=2, sticky=(N,E,S,W));
        self.tasaInput_frame.grid_propagate(False);
        self.tasaInt_leer = ttk.Entry(self.tasaInput_frame,textvariable=self.tasaTxt,validate="key",validatecommand=self.Check_Interes_wrapper,width=9);
        self.tasaInt_leer.grid(column=0,row=0,padx=(5,0),pady=5,sticky=(W,E));
        self.tasaTxtComboBox = StringVar(value="--");
        self.opciones = ["Diario","Semanal","Mensual","Anual"];
        self.combobox = ttk.Combobox(self.tasaInput_frame, textvariable=self.tasaTxtComboBox,values=self.opciones,width=8);
        self.combobox["state"]="readonly";
        self.combobox.grid(column=1,row=0,padx=(0,5),pady=1,sticky=(E,W));
        ## => Botones Seleccionables para % o Decimales (0,1)
        self.botonesI_frame = ttk.Frame(self.datos_frame,width=150, height=25);
        self.botonesI_frame.grid(column=1, row=3, sticky=(N,E,S,W));
        self.seleccion_boton_I = StringVar(value="porcentaje"); ##Formato interes seleccionado
        self.botonI_porcentaje = ttk.Radiobutton(self.botonesI_frame, text='%', variable=self.seleccion_boton_I, value='porcentaje',command=self.Borrar_Entrada_Tasa);
        self.botonI_porcentaje.grid(column=0,row=0,padx=(8,5),pady=5,sticky=W);
        self.botonI_decimal = ttk.Radiobutton(self.botonesI_frame, text='Decimal', variable=self.seleccion_boton_I, value='decimal',command=self.Borrar_Entrada_Tasa);
        self.botonI_decimal.grid(column=1,row=0,padx=5,pady=5,sticky=W);
        #Lectura Periodo:
        self.periodoTxt = StringVar();
        self.periodoLb = ttk.Label(self.datos_frame, text="Periodo/Tiempo (n):");
        self.periodoLb.grid(column=0,row=4,padx=5,pady=5,sticky=W);
        self.periodo_leer = ttk.Entry(self.datos_frame,textvariable=self.periodoTxt,validate="key",validatecommand=self.Check_Periodo_wrapper);
        self.periodo_leer.grid(column=1,row=4,padx=5,pady=5,sticky=(W,E));
        ## => Botones Seleccionables para Periodo o Tiempo(dias, semanal,meses, años)
        self.botonesT_frame = ttk.Frame(self.datos_frame,width=250, height=25);
        self.botonesT_frame.grid(column=0, row=5,columnspan=4, sticky=(N,E,S,W));
        self.seleccion_boton_T = StringVar(value="Anual"); ##Tiempo seleccionado
        self.botonT_dias = ttk.Radiobutton(self.botonesT_frame, text='Dias', variable=self.seleccion_boton_T, value='Diario');
        self.botonT_dias.grid(column=0,row=0,padx=(20,5),pady=5,sticky=N);
        self.botonT_semanal = ttk.Radiobutton(self.botonesT_frame, text='Semanas', variable=self.seleccion_boton_T, value='Semanal');
        self.botonT_semanal.grid(column=1,row=0,padx=5,pady=5,sticky=N);
        self.botonT_meses = ttk.Radiobutton(self.botonesT_frame, text='Meses', variable=self.seleccion_boton_T, value='Mensual');
        self.botonT_meses.grid(column=2,row=0,padx=5,pady=5,sticky=N);
        self.botonT_años = ttk.Radiobutton(self.botonesT_frame, text='Años', variable=self.seleccion_boton_T, value='Anual');
        self.botonT_años.grid(column=3,row=0,padx=5,pady=5,sticky=N);
        
        #Boton Interés Acumulado y Deuda Futuro
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=0,row=6,padx=5,pady=(30,10),sticky=(S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=1,row=6,padx=5,pady=(30,10),sticky=(S));
        
        #Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.interfazAmort.protocol("WM_DELETE_WINDOW",self.Cerrado_manual);
    
    #Validar solo entrada numerica
    def Check_Deuda(self,newval):
        return re.match(r'^[0-9]*[.,]?[0-9]*$', newval) is not None and newval.count('.') <= 1 and newval.count(',') <= 1 and len(newval) <= 12;
    def Check_Interes(self, newval):
        if newval == "":
            return True;
        elif self.seleccion_boton_I.get() == "porcentaje":
            regex = r'^(100(?:[.,]0{1,3})?|[0-9]{1,2}(?:[.,][0-9]{0,3})?)$';
            return (re.match(regex, newval) is not None and newval.count('.') <= 1 and newval.count(',') <= 1);
        elif self.seleccion_boton_I.get() == "decimal":
            regex = r'^(0(?:[.,][0-9]{0,3})?|1)$';
            return re.match(regex, newval) is not None and newval.count('.') <= 1 and newval.count(',') <= 1;
    def Check_Periodo(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=5;
    
    def Borrar_Entrada_Tasa(self):
        self.tasaTxt.set("");
    
    def MostrarResultados(self):
        #Mostrar Resultado en Pantalla
        ## Frame para la columna derecha (resultados)
        self.resultados_frame = ttk.Frame(self.interfazAmort,borderwidth=5,relief="groove",width=210, height=300);
        self.resultados_frame.grid(column=1, row=0, rowspan=7, padx=(0,10), pady=10, sticky=(N,E,S,W));
        self.resultados_frame.grid_propagate(False);
        ##Titulo
        self.tituloResultadosLb = ttk.Label(self.resultados_frame,text="RESULTADOS:",font=("Helvetica",10,"bold"));
        self.tituloResultadosLb.grid(column=0,row=0,padx=5,pady=5,sticky=(W,N))
        ##Cuota
        self.resulIntLb = ttk.Label(self.resultados_frame,text="Deuda Total:",font=("Helvetica", 9, "bold"));
        self.resulIntLb.grid(column=0,row=1,padx=5,pady=5,sticky=(W));
        self.deudaTotalText = StringVar();
        self.deudaLb = ttk.Label(self.resultados_frame,textvariable=self.deudaTotalText);
        self.deudaLb.grid(column=0,row=2,padx=5,pady=(0,5),sticky=(W,N));
        ##Deuda Futuro
        self.resulCuota = ttk.Label(self.resultados_frame,text="Cuota RECOMENDADA:",font=("Helvetica", 9, "bold"));
        self.resulCuota.grid(column=0,row=3,padx=5,pady=5,sticky=(W));
        self.cuotaText = StringVar();
        self.cuotaLB = ttk.Label(self.resultados_frame,textvariable=self.cuotaText);
        self.cuotaLB.grid(column=0,row=4,padx=5,sticky=(W,N));
        """
        #Grafico pie
        self.grafico_frame = ttk.Frame(self.resultados_frame);
        self.grafico_frame.grid(column=0, row=5, rowspan=2,pady=10, sticky=(N,E,S,W));
        
        #Grafico lineas
        self.resultados_lineas_frame = ttk.Frame(self.interfazAmort,borderwidth=5,relief="groove",width=210, height=350);
        self.resultados_lineas_frame.grid(column=0, row=7, columnspan=7, padx=10, sticky=(N,E,S,W));
        self.grafico_lineas_frame = ttk.Frame(self.resultados_lineas_frame);
        self.grafico_lineas_frame.grid(column=0, row=0, rowspan=3,pady=5, sticky=(N,E,S,W));
        """
    #Llamado a las Operaciones
    def CalcularResultados(self):
        #ELiminamos graficos anteriores
        plt.close('all');
        #Si se da textos en blancos o vacios
        if((self.DeudaInicTxt.get()=="" or self.DeudaInicTxt == None) or
           (self.tasaTxt.get()=="" or self.tasaTxt == None) or
           (self.tasaTxtComboBox.get()=="--" or self.tasaTxtComboBox==None) or 
           (self.periodoTxt.get()=="" or self.periodoTxt == None) or
           (self.seleccion_boton_I.get()=="" or self.seleccion_boton_I == None) or
           (self.seleccion_boton_T.get()=="" or self.seleccion_boton_T == None)):
            #Si hay datos previos, limpiarlos
            if self.datosBlancos is not None:
                self.datosBlancos.destroy();
            #Solicitar datos
            self.datosBlancos = ttk.Label(self.datos_frame, text="Por favor, rellena todos los espacios",font=("Helvetica", 9, "bold"),foreground="red");
            self.datosBlancos.grid(column=0,row=7,columnspan=2,sticky=(S,W));
            #Timer
            self.timer_id = self.datos_frame.after(5000,self.datosBlancos.destroy);
            return;
        #Caso contrario
        ##Aumentar tamaño de ventana
        self.interfazAmort.geometry("540x700+250+25");
        self.MostrarResultados();
        
        ##calcular Interes y Deuda Futuro
        cuotaPago = self.CalcularCuota();
        deudaT = self.CalcularDeudaTotal(cuotaPago);
        self.deudaTotalText.set(deudaT);
        self.cuotaText.set(cuotaPago);
        #Mostrar Grafico
        """
        self.MostrarGrafico(self.DeudaInicTxt.get(),deudaT);
        #Mostrar Grafico Lineas
        self.MostrarGraficoLineas();
        """
    def MostrarGrafico(self, DeudaInicial, deudaT):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_frame.winfo_children():
            widget.destroy();
        
        # Datos para el gráfico
        etiquetas = ['C', 'I'];
        valores = [float(OperacionesMF.Convertir_ComaPunto(DeudaInicial)), float(deudaT)];
        
        # Crear gráfico de pie
        fig, ax = plt.subplots(figsize=(2,1.5)); #Escala del grafico
        ax.set_title("Deuda Inicial (C) VS Interés (I)").set_fontsize(7);
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90,textprops={"fontsize":8});
        ax.axis('equal')  # Verificar grafico es circulo cerrado.
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame);
        canvas.draw();
        canvas.get_tk_widget().pack(fill=BOTH, expand=True);
        
    def CalcularDeudaTotal(self,cuota):
        resultado = OperacionesMF.PagoTotalAmortizacion(cuota,self.periodoTxt.get());
        return resultado;
    def CalcularCuota(self):
        resultado = OperacionesMF.CalcularCuotaAmortizacion(self.DeudaInicTxt.get(),self.tasaTxt.get(),self.tasaTxtComboBox.get(),self.seleccion_boton_I.get(),self.periodoTxt.get(),self.seleccion_boton_T.get());
        return resultado;
    # Metodos para la tabla
    
    # Operaciones de apoyo para evitar bugs
    def Cerrado_manual(self):
        if self.timer_id is not None:
            self.interfazAmort.after_cancel(self.timer_id);
        self.interfazAmort.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");
        
    def VolverMenu(self):
        if self.interfazAmort.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazAmort.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();
        