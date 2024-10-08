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
        """
        self.resultados_lineas_frame = ttk.Frame(self.resultados_frame,width=210, height=350);
        self.resultados_lineas_frame.grid(column=0, row=5, columnspan=3,padx=1, sticky=(N,E,S,W));
        self.resultados_lineas_frame.grid_propagate(False);
        self.grafico_lineas_frame = ttk.Frame(self.resultados_lineas_frame);
        self.grafico_lineas_frame.grid(column=0, row=0, rowspan=2,pady=2, sticky=(N,E,S,W));
        self.grafico_lineas_frame.grid_propagate(False);
        
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
        self.interfazAmort.geometry("540x570+250+25");
        self.MostrarResultados();
        
        #Mostrar Grafico Lineas
        self.MostrarGraficoLineas();
        ##calcular Cuota y Deuda Futuro
        nuevaTasaInteres,cuotaPago = self.CalcularCuota();
        deudaT = self.CalcularDeudaTotal(cuotaPago);
        self.deudaTotalText.set(deudaT);
        self.cuotaText.set(cuotaPago);
        #Mostrar Tablas
        datos_amortizacion = self.GenerarDatosAmortizacion(cuotaPago,nuevaTasaInteres);
        self.CrearTablaAmortizacion(datos_amortizacion);
        
    def MostrarGraficoLineas(self):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_lineas_frame.winfo_children():
            widget.destroy();
        
        # Convertir los valores ingresados
        deuda_inicial = float(OperacionesMF.Convertir_ComaPunto(self.DeudaInicTxt.get()));
        tasa_interes = float(OperacionesMF.Convertir_ComaPunto(self.tasaTxt.get())) / 100;
        periodo = int(self.periodoTxt.get());
        
        # Calcular el interés acumulado en cada año
        deudas = [];
        anios = [];
        
        # Calcular el interés acumulado año a año (puedes ajustar los saltos de años si lo deseas)
        for anio in range(1, periodo - 1, 2):  # Calcula cada dos años
            deuda = OperacionesMF.AmortizacionGrafica_DeudaActual(self.DeudaInicTxt.get(),self.tasaTxt.get(),self.tasaTxtComboBox.get(),self.seleccion_boton_I.get(),anio,self.seleccion_boton_T.get());
            deudas.append(float(self.DeudaInicTxt.get()) - deuda);
            anios.append(anio);

        # Crear gráfico de líneas
        fig, ax = plt.subplots(figsize=(2.1, 1.5));
        ax.plot(anios, deudas, marker='o', linestyle='-', color='b');
        
        # Títulos y etiquetas
        ax.set_title("Desarrollo de la Deuda", fontsize=8);
        ax.set_xlabel(self.seleccion_boton_T.get(), fontsize=4);
        ax.set_ylabel("Deuda", fontsize=3);
        
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_lineas_frame);
        canvas.draw();
        canvas.get_tk_widget().pack(fill=BOTH, expand=True);
        
    def CrearTablaAmortizacion(self,datos):
        # Crear un frame
        self.tabla_frame = ttk.Frame(self.interfazAmort);
        self.tabla_frame.grid(column=0,row=7,columnspan=7,padx=10,pady=(0,5),sticky=(N,E,S,W));
        # Configurar la columna y fila para que se expandan
        self.tabla_frame.columnconfigure(0, weight=1);
        self.tabla_frame.rowconfigure(0, weight=1);
        
        # Crear el TreeView
        self.tabla = ttk.Treeview(self.tabla_frame, columns=("Fecha", "Cuota", "Interes", "Amortizacion", "Saldo Restante"), show='headings');
        
        # Definimos columnas
        formato_periodo = self.seleccion_boton_T.get();
        if formato_periodo == "Anual":
            formato_periodo = "Año";
        elif formato_periodo == "Mensual":
            formato_periodo = "Mes";
        elif formato_periodo == "Semanal":
            formato_periodo = "Semana";
        elif formato_periodo == "Diario":
            formato_periodo = "Dia";
        self.tabla.heading("Fecha",text=formato_periodo);
        self.tabla.heading("Cuota",text="Cuota");
        self.tabla.heading("Interes",text="Interes");
        self.tabla.heading("Amortizacion",text="Amortizacion");
        self.tabla.heading("Saldo Restante",text="Saldo Restante");
        
        # Configurar el ancho de las columnas
        self.tabla.column("Fecha",width=50,anchor="center");
        self.tabla.column("Cuota",width=100,anchor="e");
        self.tabla.column("Interes",width=100,anchor="e");
        self.tabla.column("Amortizacion",width=100,anchor="e");
        self.tabla.column("Saldo Restante",width=100,anchor="e");
        
        #Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tabla_frame, orient="vertical",command=self.tabla.yview);
        self.tabla.configure(yscrollcommand=self.scrollbar.set);
        
        #Ubicar el Treeview y la barra de desplazamiento en el frame
        self.tabla.grid(column=0,row=0,sticky=(N,E,S,W));
        self.scrollbar.grid(column=1,row=0,sticky=(N,S));
        
        #Insertar Datos
        for fila in datos:
            self.tabla.insert("","end",values=fila);
    
    def GenerarDatosAmortizacion(self,cuota,nuevaTasaInteres):
        deuda_inicial = float(OperacionesMF.Convertir_ComaPunto(self.DeudaInicTxt.get()));
        periodo = int(self.periodoTxt.get());
        tasa_interes = nuevaTasaInteres;
        datos = [];
        saldo_inicial = deuda_inicial;
        flag = False;
        for tiempo in range(1,periodo+1):
            interes = OperacionesMF.AmortizacionTabla_Interes(saldo_inicial,tasa_interes);
            amortizacion = OperacionesMF.AmortizacionTabla_Amortizacion(cuota,interes);
            saldo_restante = OperacionesMF.AmortizacionTabla_SaldoPendiente(saldo_inicial,amortizacion);
            if saldo_restante < amortizacion:
                cuota += saldo_inicial;
                amortizacion = OperacionesMF.AmortizacionTabla_Amortizacion(cuota,tasa_interes);
                flag = True;
            datos.append([
                tiempo,
                f"{cuota:.2f}",
                f"{interes:.2f}",
                f"{amortizacion:.2f}",
                f"{saldo_restante:.2f}"
            ]);
            saldo_inicial = saldo_restante;
            if flag == True:
                return datos;
        return datos;
    
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
        