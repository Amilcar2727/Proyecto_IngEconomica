from tkinter import *
from tkinter import ttk
from Operaciones import OperacionesMF
#Grafico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Verificacion
import re;

class InterfazInteresCompuesto:
    #Metodo Inicial
    def __init__(self,root):
        self.root = root;
        self.interfazIC = Toplevel();
        self.interfazIC.geometry("320x300+250+150");
        self.interfazIC.title("Calculando Interes Compuesto");
        self.timer_id = None;
        self.datosBlancos = None;
        self.MenuInteresC();
    
    #Interfaz Interes Compuesto
    def MenuInteresC(self):
        ##Frame
        self.datos_frame = ttk.Frame(self.interfazIC,borderwidth=5,relief="solid",width=300, height=300);
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10,padx=10, sticky=(N,E,S,W));
        self.datos_frame.grid_propagate(False);
        
        self.tituloLb = ttk.Label(self.datos_frame, text="CALCULO INTERÉS COMPUESTO",font=("Helvetica", 12, "bold"));
        self.tituloLb.grid(column=0,row=0,columnspan=2,padx=5,pady=10,sticky=(N,S,W));
        self.check_cap_wrapper = (self.datos_frame.register(self.Check_Cap),"%P");
        self.check_num_wrapper = (self.datos_frame.register(self.Check_Num),"%P");
        #Lectura Capital
        self.capitalInicTxt = StringVar();
        self.capitalLb = ttk.Label(self.datos_frame, text="Capital en Soles (S/.):");
        self.capitalLb.grid(column=0,row=1,padx=5,pady=5,sticky=W);
        self.capital_leer = ttk.Entry(self.datos_frame,textvariable=self.capitalInicTxt,validate="key",validatecommand=self.check_cap_wrapper);
        self.capital_leer.grid(column=1,row=1,padx=5,pady=5,sticky=(W,E));
        
        #Lectura Tasa de Interez:
        self.tasaTxt = StringVar();
        self.tasaIntLb = ttk.Label(self.datos_frame, text="Tasa de Interés (%):");
        self.tasaIntLb.grid(column=0,row=2,padx=5,pady=5,sticky=W);
        self.tasaInt_leer = ttk.Entry(self.datos_frame,textvariable=self.tasaTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.tasaInt_leer.grid(column=1,row=2,padx=5,pady=5,sticky=(W,E));
        ## => Botones Seleccionables
        #Lectura Periodo:
        self.periodoTxt = StringVar();
        self.periodoLb = ttk.Label(self.datos_frame, text="Periodo/Tiempo (años):");
        self.periodoLb.grid(column=0,row=3,padx=5,pady=5,sticky=W);
        self.periodo_leer = ttk.Entry(self.datos_frame,textvariable=self.periodoTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.periodo_leer.grid(column=1,row=3,padx=5,pady=5,sticky=(W,E));
        ## => Botones Seleccionables
        
        #Boton Interés Acumulado y Capital Futuro
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=0,row=4,padx=5,pady=10,sticky=(S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=1,row=4,padx=5,pady=10,sticky=(S));
        
        #Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.interfazIC.protocol("WM_DELETE_WINDOW",self.Cerrado_manual);
    
    #Validar solo entrada numerica
    def Check_Cap(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=10;
    def Check_Num(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=2;
    
    def MostrarResultados(self):
        #Mostrar Resultado en Pantalla
        ## Frame para la columna derecha (resultados)
        self.resultados_frame = ttk.Frame(self.interfazIC,borderwidth=5,relief="groove",width=210, height=300);
        self.resultados_frame.grid(column=1, row=0, rowspan=7, padx=(0,10), pady=10, sticky=(N,E,S,W));
        self.resultados_frame.grid_propagate(False);
        ##Titulo
        self.tituloResultadosLb = ttk.Label(self.resultados_frame,text="RESULTADOS:",font=("Helvetica",10,"bold"));
        self.tituloResultadosLb.grid(column=0,row=0,padx=5,pady=5,sticky=(W,N))
        ##Interes
        self.resulIntLb = ttk.Label(self.resultados_frame,text="Interés Acumulado TOTAL:",font=("Helvetica", 8, "bold"));
        self.resulIntLb.grid(column=0,row=1,padx=5,pady=5,sticky=(W));
        self.interesText = StringVar();
        self.interesLb = ttk.Label(self.resultados_frame,textvariable=self.interesText);
        self.interesLb.grid(column=0,row=2,padx=5,pady=(0,5),sticky=(W,N));
        ##Capital Futuro
        self.resulCapFutLb = ttk.Label(self.resultados_frame,text="Capital Futuro TOTAL:",font=("Helvetica", 8, "bold"));
        self.resulCapFutLb.grid(column=0,row=3,padx=5,pady=5,sticky=(W));
        self.capitalFText = StringVar();
        self.capitalFLb = ttk.Label(self.resultados_frame,textvariable=self.capitalFText);
        self.capitalFLb.grid(column=0,row=4,padx=5,sticky=(W,N));
        #Grafico pie
        self.grafico_frame = ttk.Frame(self.resultados_frame);
        self.grafico_frame.grid(column=0, row=5, rowspan=2, pady=10, sticky=(N,E,S,W));
    #Llamado a las Operaciones
    def CalcularResultados(self):
        #Si se da textos en blancos o vacios
        if((self.capitalInicTxt.get()=="" or self.capitalInicTxt == None) or
           (self.tasaTxt.get()=="" or self.tasaTxt == None) or
           (self.periodoTxt.get()=="" or self.periodoTxt == None)):
            #Si hay datos previos, limpiarlos
            if self.datosBlancos is not None:
                self.datosBlancos.destroy();
            #Solicitar datos
            self.datosBlancos = ttk.Label(self.datos_frame, text="Por favor, rellena todos los espacios",font=("Helvetica", 9, "bold"),foreground="red");
            self.datosBlancos.grid(column=0,row=5,columnspan=2,sticky=(S,W));
            #Timer
            self.timer_id = self.interfazIC.after(5000,self.datosBlancos.destroy);
            return;
        #Caso contrario 
         ##Aumentar tamaño de ventana
        self.interfazIC.geometry("540x500+250+150");
        self.MostrarResultados();
        ##calcular Interes y Capital Futuro
        interesT = self.CalcularInteresCompuesto();
        capitalFuturo = self.CalcularCapitalFuturo(interesT);
        self.interesText.set(interesT);
        self.capitalFText.set(capitalFuturo);
        #Mostrar Grafico
        self.MostrarGrafico(self.capitalInicTxt.get(),interesT);
    
    def MostrarGrafico(self, capitalInicial, interesT):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_frame.winfo_children():
            widget.destroy();
        
        # Datos para el gráfico
        etiquetas = ['C', 'I'];
        valores = [float(capitalInicial), float(interesT)];
        
        # Crear gráfico de pie
        fig, ax = plt.subplots(figsize=(2,1.5)); #Escala del grafico
        ax.set_title("Capital Inicial (C) VS Interés (I)").set_fontsize(7);
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90,textprops={"fontsize":8});
        ax.axis('equal')  # Verificar grafico es circulo cerrado.
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame);
        canvas.draw();
        canvas.get_tk_widget().pack(fill=BOTH, expand=True);
    
    def CalcularInteresCompuesto(self):
        resultado = OperacionesMF.InteresCompuestoAcumulado(self.capitalInicTxt.get(),self.tasaTxt.get(),self.periodoTxt.get());
        return resultado;
    def CalcularCapitalFuturo(self,interesT):
        resultado = OperacionesMF.CapitalCompuestoFuturo(self.capitalInicTxt.get(),self.tasaTxt.get(),self.periodoTxt.get());
        return resultado;
    # Operaciones de apoyo para evitar bugs
    def Cerrado_manual(self):
        if self.timer_id is not None:
            self.interfazIC.after_cancel(self.timer_id);
        self.interfazIC.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");
        
    def VolverMenu(self):
        if self.interfazIC.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazIC.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();
        