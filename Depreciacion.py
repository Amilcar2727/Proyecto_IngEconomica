from tkinter import *
from tkinter import ttk
from Operaciones import OperacionesMF
#Grafico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Verificacion
import re;

class InterfazDepreciacion:
    #Metodo Inicial
    def __init__(self,root):
        self.root = root;
        self.interfazDeprec = Toplevel();
        self.interfazDeprec.geometry("320x300+250+25");
        self.interfazDeprec.title("Calculando Depreciacion");
        self.timer_id = None;
        self.datosBlancos = None;
        self.MenuDepreciacion();
    
    #Interfaz Interes Simple
    def MenuDepreciacion(self):
        self.datos_frame = ttk.Frame(self.interfazDeprec,borderwidth=5,relief="solid",width=300, height=300);
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10,padx=10, sticky=(N,E,S,W));
        self.datos_frame.grid_propagate(False);
        
        self.tituloLb = ttk.Label(self.datos_frame, text="CALCULO DE DEPRECIACION",font=("Helvetica", 12, "bold"));
        self.tituloLb.grid(column=0,row=0,columnspan=2,padx=5,pady=10,sticky=(N,S,W));
        self.Check_Depreciacion_wrapper = (self.datos_frame.register(self.Check_Depreciacion),"%P");
        self.Check_Periodo_wrapper = (self.datos_frame.register(self.Check_Periodo),"%P");
        #Lectura CostoActivo
        self.CostoAFTxt = StringVar();
        self.CostoALbl = ttk.Label(self.datos_frame, text="Costo Activo en Soles (P):");
        self.CostoALbl.grid(column=0,row=1,padx=5,pady=5,sticky=W);
        self.CostoA_leer = ttk.Entry(self.datos_frame,textvariable=self.CostoAFTxt,validate="key",validatecommand=self.Check_Depreciacion_wrapper);
        self.CostoA_leer.grid(column=1,row=1,padx=(0,14),pady=5,sticky=(W,E));
        
        #Lectura Valor de Rescate
        self.ValorRescateTxt = StringVar();
        self.ValorRLbl = ttk.Label(self.datos_frame, text="Valor de Rescate en Soles (P):");
        self.ValorRLbl.grid(column=0,row=2,padx=5,pady=5,sticky=W);
        self.ValorR_leer = ttk.Entry(self.datos_frame,textvariable=self.ValorRescateTxt,validate="key",validatecommand=self.Check_Depreciacion_wrapper);
        self.ValorR_leer.grid(column=1,row=2,padx=(0,14),pady=5,sticky=(W,E));
        
        #Lectura Periodo:
        self.periodoTxt = StringVar();
        self.periodoLb = ttk.Label(self.datos_frame, text="Vida Util (años):");
        self.periodoLb.grid(column=0,row=3,padx=5,pady=5,sticky=W);
        self.periodo_leer = ttk.Entry(self.datos_frame,textvariable=self.periodoTxt,validate="key",validatecommand=self.Check_Periodo_wrapper);
        self.periodo_leer.grid(column=1,row=3,padx=(0,14),pady=5,sticky=(W,E));
        
        #Boton Calcular
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=0,row=4,padx=5,pady=(30,10),sticky=(S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=1,row=4,padx=5,pady=(30,10),sticky=(S));
        #Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.interfazDeprec.protocol("WM_DELETE_WINDOW",self.Cerrado_manual);
    
    #Validar solo entrada numerica
    def Check_Depreciacion(self,newval):
        return re.match(r'^[0-9]*[.,]?[0-9]*$', newval) is not None and newval.count('.') <= 1 and newval.count(',') <= 1 and len(newval) <= 12;
    
    def Check_Periodo(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=5;
    
    def MostrarResultados(self):
        #Mostrar Resultado en Pantalla
        ## Frame para la columna derecha (resultados)
        self.resultados_frame = ttk.Frame(self.interfazDeprec,borderwidth=5,relief="groove",width=325, height=300);
        self.resultados_frame.grid(column=1, row=0, rowspan=7, padx=(0,10), pady=10, sticky=(N,E,S,W));
        self.resultados_frame.grid_propagate(False);
        ##Titulo
        self.tituloResultadosLb = ttk.Label(self.resultados_frame,text="RESULTADOS:",font=("Helvetica",10,"bold"));
        self.tituloResultadosLb.grid(column=0,row=0,padx=5,pady=5,sticky=(W,N))
        ##Depreciación
        self.DepreciacionLb = ttk.Label(self.resultados_frame,text="Depreciación Generada:",font=("Helvetica", 9, "bold"));
        self.DepreciacionLb.grid(column=0,row=1,padx=5,pady=5,sticky=(W));
        self.DepreciacionText = StringVar();
        self.DepreciacionLbl = ttk.Label(self.resultados_frame,textvariable=self.DepreciacionText);
        self.DepreciacionLbl.grid(column=0,row=2,padx=5,pady=(0,5),sticky=(W,N));
        
        #GRAFICO LINEAS
        self.resultados_lineas_frame = ttk.Frame(self.resultados_frame,width=300, height=200);
        self.resultados_lineas_frame.grid(column=0, row=3, columnspan=3,padx=1, sticky=(N,E,S,W));
        self.resultados_lineas_frame.grid_propagate(False);
        self.grafico_lineas_frame = ttk.Frame(self.resultados_lineas_frame);
        self.grafico_lineas_frame.grid(column=0, row=0, rowspan=2, padx=(2,0),pady=2, sticky=(N,E,S,W));
        self.grafico_lineas_frame.grid_propagate(True);
        #GRAFICO TABLA
        self.tabla_frame = ttk.Frame(self.interfazDeprec, width=300, height=150);
        self.tabla_frame.grid(column=0, row=7, padx=10, pady=5, sticky=(N, E, S, W));
        
    #Llamado a las Operaciones
    def CalcularResultados(self):
        #ELiminamos graficos anteriores
        plt.close('all');
        #Si se da textos en blancos o vacios
        if((self.CostoAFTxt.get()=="" or self.CostoAFTxt == None) or
           (self.periodoTxt.get()=="" or self.periodoTxt == None)):
            #Si hay datos previos, limpiarlos
            if self.datosBlancos is not None:
                self.datosBlancos.destroy();
            #Solicitar datos
            self.datosBlancos = ttk.Label(self.datos_frame, text="Por favor, rellena todos los espacios",font=("Helvetica", 9, "bold"),foreground="red");
            self.datosBlancos.grid(column=0,row=5,columnspan=2,sticky=(S,W));
            #Timer
            self.timer_id = self.datos_frame.after(5000,self.datosBlancos.destroy);
            return;
        #Caso contrario
        ##Aumentar tamaño de ventana
        self.interfazDeprec.geometry("650x525+250+25");
        self.MostrarResultados();
        
        #Mostrar Grafico Lineas
        self.MostrarGraficoLineas();
        ##Calcular Depreciacion
        DepreciacionT = self.CalcularDepreciacion();
        self.DepreciacionText.set(DepreciacionT);
        #Mostrar Tablas
        #datos_Depreciacion = self.GenerarDatosDepreciacion(cuotaPago,nuevaTasaInteres);
        self.CrearTablaDepreciacion();
        
    def MostrarGraficoLineas(self):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_lineas_frame.winfo_children():
            widget.destroy();
        
        # Convertir los valores ingresados
        costo_inicial = float(OperacionesMF.Convertir_ComaPunto(self.CostoAFTxt.get()))
        valor_rescate = float(OperacionesMF.Convertir_ComaPunto(self.ValorRescateTxt.get()))
        periodo = int(self.periodoTxt.get())
        
        # Calcular la depreciación anual
        depreciacion_anual = (costo_inicial - valor_rescate) / periodo
        # Generar datos para el gráfico
        depreciaciones = []
        anios = []
        saldo_restante = costo_inicial

        for anio in range(1, periodo + 1):
            depreciaciones.append(saldo_restante)
            anios.append(anio)
            saldo_restante -= depreciacion_anual
        
        # Asegurar que el último valor llegue al valor de rescate
        depreciaciones.append(valor_rescate)
        anios.append(periodo + 1)
        
        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(3, 2))
        ax.plot(anios, depreciaciones, marker='o', linestyle='-', color='b')
        
        # Títulos y etiquetas
        ax.set_title("Desarrollo de la Depreciación", fontsize=7)
        ax.set_xlabel("Años", fontsize=7)
        ax.set_ylabel("Valor del Activo (S/)", fontsize=7)
        ax.tick_params(axis='both', labelsize=7)
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Ajustar el margen para mover el gráfico
        plt.subplots_adjust(left=0.2, right=0.9, top=0.85, bottom=0.2)  # Reducir el margen izquierdo
    
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_lineas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
    def CrearTablaDepreciacion(self):
        # Limpiar cualquier tabla existente en el frame
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        # Obtener los datos de depreciación
        datos = self.GenerarDatosDepreciacion()

        # Crear encabezados de la tabla
        encabezados = ["Año", "Costo Actual", "Depreciación Acumulada"]
        for col, encabezado in enumerate(encabezados):
            lbl = ttk.Label(self.tabla_frame, text=encabezado, borderwidth=1, relief="solid")
            lbl.grid(row=0, column=col, sticky="nsew")

        # Crear las filas de datos
        for fila, datos_fila in enumerate(datos, start=1):
            for col, valor in enumerate(datos_fila):
                lbl = ttk.Label(self.tabla_frame, text=str(valor), borderwidth=1, relief="solid")
                lbl.grid(row=fila, column=col, sticky="nsew")

        # Ajustar las columnas para que se expandan uniformemente
        for col in range(3):  # Tres columnas
            self.tabla_frame.grid_columnconfigure(col, weight=1)
    
    def GenerarDatosDepreciacion(self):
        # Obtener valores de entrada
        Costo_inicial = float(OperacionesMF.Convertir_ComaPunto(self.CostoAFTxt.get()))
        Valor_rescate = float(OperacionesMF.Convertir_ComaPunto(self.ValorRescateTxt.get()))
        periodo = int(self.periodoTxt.get())

        # Calcular depreciación anual
        Depreciacion_anual = OperacionesMF.DepreciacionLR(
            self.CostoAFTxt.get(), self.ValorRescateTxt.get(), self.periodoTxt.get()
        )

        # Inicializar listas para los datos
        datos = []
        depreciacion_acumulada = 0

        for anio in range(periodo + 1):  # Incluye el año 0 hasta el periodo
            if anio == 0:
                costo_actual = Costo_inicial
            else:
                costo_actual -= Depreciacion_anual

            # Acumular la depreciación
            depreciacion_acumulada += Depreciacion_anual if anio > 0 else 0

            # Asegurarse de que el costo actual no sea menor que el valor de rescate
            costo_actual = max(costo_actual, Valor_rescate)

            # Agregar datos a la tabla (Año, Costo Actual, Depreciación Acumulada)
            datos.append([anio, round(costo_actual, 2), round(depreciacion_acumulada, 2)])

        return datos
    
    def CalcularDepreciacion(self):
        resultado = OperacionesMF.DepreciacionLR(self.CostoAFTxt.get(),self.ValorRescateTxt.get(),self.periodoTxt.get());
        return resultado;
    
    # Operaciones de apoyo para evitar bugs
    def Cerrado_manual(self):
        if self.timer_id is not None:
            self.interfazDeprec.after_cancel(self.timer_id);
        self.interfazDeprec.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");
        
    def VolverMenu(self):
        if self.interfazDeprec.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazDeprec.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();
        