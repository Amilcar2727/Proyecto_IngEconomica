from tkinter import *
from tkinter import ttk
from Operaciones import OperacionesMF
#Grafico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Verificacion
import re;

class InterfazInteresSimple:
    #Metodo Inicial
    def __init__(self,root):
        self.root = root;
        self.interfazIS = Toplevel();
        self.interfazIS.geometry("320x300+250+25");
        self.interfazIS.title("Calculando Interes Simple");
        self.timer_id = None;
        self.datosBlancos = None;
        self.MenuInteresS();
    
    #Interfaz Interes Simple
    def MenuInteresS(self):
        self.datos_frame = ttk.Frame(self.interfazIS,borderwidth=5,relief="solid",width=300, height=300);
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10,padx=10, sticky=(N,E,S,W));
        self.datos_frame.grid_propagate(False);
        
        self.tituloLb = ttk.Label(self.datos_frame, text="CALCULO DE INTERÉS SIMPLE",font=("Helvetica", 12, "bold"));
        self.tituloLb.grid(column=0,row=0,columnspan=2,padx=5,pady=10,sticky=(N,S,W));
        self.Check_Capital_wrapper = (self.datos_frame.register(self.Check_Capital),"%P");
        self.Check_Interes_wrapper = (self.datos_frame.register(self.Check_Interes),"%P");
        self.Check_Periodo_wrapper = (self.datos_frame.register(self.Check_Periodo),"%P");
        #Lectura Capital
        self.capitalInicTxt = StringVar();
        self.capitalLb = ttk.Label(self.datos_frame, text="Capital en Soles (P):");
        self.capitalLb.grid(column=0,row=1,padx=5,pady=5,sticky=W);
        self.capital_leer = ttk.Entry(self.datos_frame,textvariable=self.capitalInicTxt,validate="key",validatecommand=self.Check_Capital_wrapper);
        self.capital_leer.grid(column=1,row=1,padx=5,pady=5,sticky=(W,E));
        
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
        
        #Boton Interés Acumulado y Capital Futuro
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=0,row=6,padx=5,pady=(30,10),sticky=(S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=1,row=6,padx=5,pady=(30,10),sticky=(S));
        
        #Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.interfazIS.protocol("WM_DELETE_WINDOW",self.Cerrado_manual);
    
    #Validar solo entrada numerica
    def Check_Capital(self,newval):
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
        self.resultados_frame = ttk.Frame(self.interfazIS,borderwidth=5,relief="groove",width=210, height=300);
        self.resultados_frame.grid(column=1, row=0, rowspan=7, padx=(0,10), pady=10, sticky=(N,E,S,W));
        self.resultados_frame.grid_propagate(False);
        ##Titulo
        self.tituloResultadosLb = ttk.Label(self.resultados_frame,text="RESULTADOS:",font=("Helvetica",10,"bold"));
        self.tituloResultadosLb.grid(column=0,row=0,padx=5,pady=5,sticky=(W,N))
        ##Interes
        self.resulIntLb = ttk.Label(self.resultados_frame,text="Interés Acumulado TOTAL:",font=("Helvetica", 9, "bold"));
        self.resulIntLb.grid(column=0,row=1,padx=5,pady=5,sticky=(W));
        self.interesText = StringVar();
        self.interesLb = ttk.Label(self.resultados_frame,textvariable=self.interesText);
        self.interesLb.grid(column=0,row=2,padx=5,pady=(0,5),sticky=(W,N));
        ##Capital Futuro
        self.resulCapFutLb = ttk.Label(self.resultados_frame,text="Capital Futuro TOTAL:",font=("Helvetica", 9, "bold"));
        self.resulCapFutLb.grid(column=0,row=3,padx=5,pady=5,sticky=(W));
        self.capitalFText = StringVar();
        self.capitalFLb = ttk.Label(self.resultados_frame,textvariable=self.capitalFText);
        self.capitalFLb.grid(column=0,row=4,padx=5,sticky=(W,N));
        #Grafico pie
        self.grafico_frame = ttk.Frame(self.resultados_frame);
        self.grafico_frame.grid(column=0, row=5, rowspan=2,pady=10, sticky=(N,E,S,W));
        
        #Grafico lineas
        self.resultados_lineas_frame = ttk.Frame(self.interfazIS,borderwidth=5,relief="groove",width=210, height=350);
        self.resultados_lineas_frame.grid(column=0, row=7, columnspan=7, padx=10, sticky=(N,E,S,W));
        self.grafico_lineas_frame = ttk.Frame(self.resultados_lineas_frame);
        self.grafico_lineas_frame.grid(column=0, row=0, rowspan=3,pady=5, sticky=(N,E,S,W));
    
    #Llamado a las Operaciones
    def CalcularResultados(self):
        #ELiminamos graficos anteriores
        plt.close('all');
        #Si se da textos en blancos o vacios
        if((self.capitalInicTxt.get()=="" or self.capitalInicTxt == None) or
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
        self.interfazIS.geometry("540x700+250+25");
        self.MostrarResultados();
        
        ##calcular Interes y Capital Futuro
        ##Logica para porcentaje 
        interesT = self.CalcularInteresSimple();
        capitalFuturo = self.CalcularCapitalFuturo(interesT);
        self.interesText.set(interesT);
        self.capitalFText.set(capitalFuturo);
        #Mostrar Grafico
        self.MostrarGrafico(self.capitalInicTxt.get(),interesT);
        #Mostrar Grafico Lineas
        self.MostrarGraficoLineas();
    
    def MostrarGrafico(self, capitalInicial, interesT):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_frame.winfo_children():
            widget.destroy();
        
        # Datos para el gráfico
        etiquetas = ['C', 'I'];
        valores = [float(OperacionesMF.Convertir_ComaPunto(capitalInicial)), float(interesT)];
        
        # Crear gráfico de pie
        fig, ax = plt.subplots(figsize=(2,1.5)); #Escala del grafico
        ax.set_title("Capital Inicial (C) VS Interés (I)").set_fontsize(7);
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90,textprops={"fontsize":8});
        ax.axis('equal')  # Verificar grafico es circulo cerrado.
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame);
        canvas.draw();
        canvas.get_tk_widget().pack(fill=BOTH, expand=True);
        
    def MostrarGraficoLineas(self):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_lineas_frame.winfo_children():
            widget.destroy();
        
        # Convertir los valores ingresados
        capital_inicial = float(OperacionesMF.Convertir_ComaPunto(self.capitalInicTxt.get()));
        tasa_interes = float(OperacionesMF.Convertir_ComaPunto(self.tasaTxt.get())) / 100;
        periodo = int(self.periodoTxt.get());
        
        # Calcular el interés acumulado en cada año
        intereses_acumulados = [];
        anios = [];
        
        # Calcular el interés acumulado año a año (puedes ajustar los saltos de años si lo deseas)
        for anio in range(1, periodo + 1, 2):  # Calcula cada dos años
            interes_acumulado = capital_inicial * tasa_interes * anio;
            intereses_acumulados.append(interes_acumulado);
            anios.append(anio);

        # Crear gráfico de líneas
        fig, ax = plt.subplots(figsize=(5, 3.5));
        ax.plot(anios, intereses_acumulados, marker='o', linestyle='-', color='b');
        
        # Títulos y etiquetas
        ax.set_title("Incremento del Interés Simple", fontsize=8);
        ax.set_xlabel(self.seleccion_boton_T.get(), fontsize=8);
        ax.set_ylabel("Interés Acumulado", fontsize=8);
        
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_lineas_frame);
        canvas.draw();
        canvas.get_tk_widget().pack(fill=BOTH, expand=True);
    
    def CalcularInteresSimple(self):
        resultado = OperacionesMF.InteresSimpleAcumulado(self.capitalInicTxt.get(),self.tasaTxt.get(),self.tasaTxtComboBox.get(),self.seleccion_boton_I.get(),self.periodoTxt.get(),self.seleccion_boton_T.get());
        return resultado;
    def CalcularCapitalFuturo(self,interesT):
        resultado = OperacionesMF.CapitalSimpleFuturo(self.capitalInicTxt.get(),interesT);
        return resultado;
    # Operaciones de apoyo para evitar bugs
    def Cerrado_manual(self):
        if self.timer_id is not None:
            self.interfazIS.after_cancel(self.timer_id);
        self.interfazIS.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");
        
    def VolverMenu(self):
        if self.interfazIS.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazIS.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();
        