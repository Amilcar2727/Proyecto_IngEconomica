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
        
        #Metodo para amortizacion
        self.textoComboBox = StringVar(value="Sistema Frances");
        self.opcionesSistema = ["Sistema Americano","Sistema Frances","Sistema Aleman"];
        self.comboboxS = ttk.Combobox(self.datos_frame, textvariable=self.textoComboBox,values=self.opcionesSistema);
        self.comboboxS["state"]="readonly";
        self.comboboxS.grid(column=0,row=6,columnspan=2,pady=1,sticky=(N,S));
        #Boton Calcular
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=0,row=7,padx=5,pady=(30,10),sticky=(S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=1,row=7,padx=5,pady=(30,10),sticky=(S));
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
        self.result1Lb = ttk.Label(self.resultados_frame,text="Pago Total:",font=("Helvetica", 9, "bold"));
        self.result1Lb.grid(column=0,row=1,padx=5,pady=5,sticky=(W));
        self.result1Text = StringVar();
        self.resultTotal1Lb = ttk.Label(self.resultados_frame,textvariable=self.result1Text);
        self.resultTotal1Lb.grid(column=0,row=2,padx=5,pady=(0,5),sticky=(W,N));
        ##Deuda Futuro
        self.result2 = StringVar();
        self.result2Lb = ttk.Label(self.resultados_frame,textvariable=self.result2,text="Cuota RECOMENDADA:",font=("Helvetica", 9, "bold"));
        self.result2Lb.grid(column=0,row=3,padx=5,pady=5,sticky=(W));
        self.result2Text = StringVar();
        self.resultTotal2Lb = ttk.Label(self.resultados_frame,textvariable=self.result2Text);
        self.resultTotal2Lb.grid(column=0,row=4,padx=5,sticky=(W,N));
        
        
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
        #self.MostrarGraficoLineas();
        #Obtener el sistema de amortizacion
        op = self.comboboxS.get();
        if op == "Sistema Frances":
            self.result2.set("Cuota RECOMENDADA:");
            cuotaPago = self.CalcularCuotaFrances();
            deudaT = self.CalcularDeudaTotalFrances(cuotaPago);
            self.result1Text.set(deudaT);
            self.result2Text.set(cuotaPago);
        elif op == "Sistema Aleman":
            self.result2.set("Amortización RECOMENDADA:");
            amortizacion = self.CalcularAmortizacionAleman();
            interesesTotales = self.CalcularInteresesTAleman();
            deudaT = self.CalcularDeudaTotalAleman(interesesTotales);
            self.result1Text.set(deudaT);
            self.result2Text.set(amortizacion);
        elif op == "Sistema Americano":
            self.result2.set("Intereses RECOMENDADOS:");
            intereses = self.CalcularInteresesAmericanos();
            interesesTotales = self.CalcularInteresesTAmericanos(intereses);
            deudaT = self.CalcularDeudaTotalAmericano(interesesTotales);
            self.result1Text.set(deudaT);
            self.result2Text.set(intereses);
        ##calcular Cuota y Deuda Futuro
        
        
        #Mostrar Tablas
        #datos_amortizacion = self.GenerarDatosAmortizacion(cuotaPago);
        #self.CrearTablaAmortizacion(datos_amortizacion);
        
    def MostrarGraficoLineas(self):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_lineas_frame.winfo_children():
            widget.destroy();
        
        if self.textoComboBox.get() == "Sistema Frances":
            deuda_inicial = float(self.DeudaInicTxt.get())
            tasa_interes = float(self.tasaTxt.get()) / 100 if self.seleccion_boton_I.get() == "porcentaje" else float(self.tasaTxt.get())
            n_periodos = int(self.periodoTxt.get())

            # Llamar a la lógica para calcular amortización francesa
            datos_amortizacion = OperacionesMF().calcularAmortizacionFrancesa(deuda_inicial, tasa_interes, n_periodos)

            saldo_restante = [dato['saldo_restante'] for dato in datos_amortizacion]
            intereses = [dato['interes'] for dato in datos_amortizacion]
            amortizaciones = [dato['amortizacion'] for dato in datos_amortizacion]
            periodos = list(range(1, n_periodos + 1))

            # Crear el gráfico
            figura = plt.Figure(figsize=(5, 4), dpi=100)
            ax = figura.add_subplot(111)
            ax.plot(periodos, saldo_restante, label="Saldo Restante", marker="o")
            ax.plot(periodos, intereses, label="Interés", marker="x")
            ax.plot(periodos, amortizaciones, label="Amortización", marker="s")
            ax.set_title("Amortización Francesa")
            ax.set_xlabel("Tiempo (Períodos)")
            ax.set_ylabel("Dinero")
            ax.legend()
            ax.grid(True)

            # Mostrar el gráfico en la interfaz
            canvas = FigureCanvasTkAgg(figura, self.grafico_lineas_frame)
            canvas.get_tk_widget().grid(column=0, row=0, sticky=(N, S, E, W))
            canvas.draw()
        
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

    """->>>>>>>>>>>>> METODOS DE CALCULO DE OPERACIONES EXTRAS >>>>>>>>>>>>>>"""    
    ## CALCULO DE CUOTAS:
    def CalcularCuotaFrances(self):
        return OperacionesMF.CalcularCuotaFrances(self.DeudaInicTxt.get(),self.tasaTxt.get(),self.tasaTxtComboBox.get(),self.seleccion_boton_I.get(),self.periodoTxt.get(),self.seleccion_boton_T.get());
    def CalcularAmortizacionAleman(self):
        return OperacionesMF.CalcularAmortizacionAleman(self.DeudaInicTxt.get(),self.periodoTxt.get());
    def CalcularInteresesTAleman(self):
        return OperacionesMF.InteresTotalesAleman(self.DeudaInicTxt.get(),self.tasaTxt.get(),self.tasaTxtComboBox.get(),self.seleccion_boton_I.get(),self.periodoTxt.get(),self.seleccion_boton_T.get());
    def CalcularInteresesAmericanos(self):
        return OperacionesMF.CalcularInteresesAmericano(self.DeudaInicTxt.get(),self.tasaTxt.get(),self.tasaTxtComboBox.get(),self.seleccion_boton_I.get(),self.periodoTxt.get(),self.seleccion_boton_T.get());
    def CalcularInteresesTAmericanos(self,intereses):
        return OperacionesMF.InteresTotalesAmericano(intereses,self.periodoTxt.get());
    ## CALCULO DE DEUDA TOTAL
    def CalcularDeudaTotalFrances(self,cuota):
        return OperacionesMF.PagoTotalFrances(cuota,self.periodoTxt.get());
    def CalcularDeudaTotalAleman(self,interesesTotales):
        return OperacionesMF.PagoTotalAleman(self.DeudaInicTxt.get(),interesesTotales);
    def CalcularDeudaTotalAmericano(self,interesesTotales):
        return OperacionesMF.PagoTotalAmericano(self.DeudaInicTxt.get(),interesesTotales);
    
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