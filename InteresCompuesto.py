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
        self.interfazIS = Toplevel();
        self.interfazIS.geometry("550x400+250+150");
        self.interfazIS.title("Calculando Interes Compuesto");
        self.timer_id = None;
        self.datosBlancos = None;
        self.MenuInteresC();
    
    #Interfaz Interes Compuesto
    def MenuInteresC(self):
        self.tituloLb = ttk.Label(self.interfazIS, text="CALCULO DE INTERÉS COMPUESTO",font=("Helvetica", 10, "bold"));
        self.tituloLb.grid(column=0,row=0,columnspan=3,pady=10,sticky=(N,W));
        self.check_cap_wrapper = (self.interfazIS.register(self.Check_Cap),"%P");
        self.check_num_wrapper = (self.interfazIS.register(self.Check_Num),"%P");
        #Lectura Capital
        self.capitalInicTxt = StringVar();
        self.capitalLb = ttk.Label(self.interfazIS, text="Capital en Soles (S/.):");
        self.capitalLb.grid(column=0,row=1,padx=5,pady=5,sticky=W);
        self.capital_leer = ttk.Entry(self.interfazIS,textvariable=self.capitalInicTxt,validate="key",validatecommand=self.check_cap_wrapper);
        self.capital_leer.grid(column=1,row=1,padx=5,pady=5,sticky=(W,E));
        
        #Lectura Tasa de Interez:
        self.tasaTxt = StringVar();
        self.tasaIntLb = ttk.Label(self.interfazIS, text="Tasa de Interés (%):");
        self.tasaIntLb.grid(column=0,row=2,padx=5,pady=5,sticky=W);
        self.tasaInt_leer = ttk.Entry(self.interfazIS,textvariable=self.tasaTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.tasaInt_leer.grid(column=1,row=2,padx=5,pady=5,sticky=(W,E));
        ## => Botones Seleccionables
        #Lectura Periodo:
        self.periodoTxt = StringVar();
        self.periodoLb = ttk.Label(self.interfazIS, text="Periodo/Tiempo (años):");
        self.periodoLb.grid(column=0,row=3,padx=5,pady=5,sticky=W);
        self.periodo_leer = ttk.Entry(self.interfazIS,textvariable=self.periodoTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.periodo_leer.grid(column=1,row=3,padx=5,pady=5,sticky=(W,E));
        ## => Botones Seleccionables
        
        #Mostrar Resultado en Pantalla
        ##Interes
        self.resulIntLb = ttk.Label(self.interfazIS,text="Interés Acumulado TOTAL:");
        self.resulIntLb.grid(column=2,row=0,padx=5,pady=5,sticky=(W));
        self.interesText = StringVar();
        self.interesLb = ttk.Label(self.interfazIS,textvariable=self.interesText);
        self.interesLb.grid(column=2,row=1,padx=5,sticky=(W,N));
        ##Capital Futuro
        self.resulCapFutLb = ttk.Label(self.interfazIS,text="Capital Futuro TOTAL:");
        self.resulCapFutLb.grid(column=2,row=2,padx=5,pady=5,sticky=(W));
        self.capitalFText = StringVar();
        self.capitalFLb = ttk.Label(self.interfazIS,textvariable=self.capitalFText);
        self.capitalFLb.grid(column=2,row=3,padx=5,sticky=(W,N));
        
        #Boton Interés Acumulado y Capital Futuro
        self.resultadosBt = ttk.Button(self.interfazIS, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=0,row=4,padx=5,pady=10,sticky=(S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.interfazIS, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=1,row=4,padx=5,pady=10,sticky=(S));
        #Grafico pie
        self.grafico_frame = ttk.Frame(self.interfazIS);
        self.grafico_frame.grid(column=2, row=4, rowspan=6, padx=1, pady=1, sticky=(N,E,S,W));
        #Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.interfazIS.protocol("WM_DELETE_WINDOW",self.Cerrado_manual);
    
    #Validar solo entrada numerica
    def Check_Cap(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=10;
    def Check_Num(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=2;
    
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
            self.datosBlancos = ttk.Label(self.interfazIS, text="Por favor, rellena todos los espacios",font=("Helvetica", 9, "bold"),foreground="red");
            self.datosBlancos.grid(column=0,row=6,columnspan=2,sticky=(S,W));
            #Timer
            self.timer_id = self.interfazIS.after(5000,self.datosBlancos.destroy);
            return;
        #Caso contrario calcular Interes y Capital Futuro
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
        etiquetas = ['Capital Inicial', 'Interés'];
        valores = [float(capitalInicial), float(interesT)];
        
        # Crear gráfico de pie
        fig, ax = plt.subplots(figsize=(3,2)); #Escala del grafico
        ax.set_title("Capital VS Interes");
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90);
        ax.axis('equal')  # Verificar grafico es circulo cerrado.
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame);
        canvas.draw();
        canvas.get_tk_widget().pack(fill=BOTH, expand=True);
    
    def CalcularInteresCompuesto(self):
        resultado = OperacionesMF.InteresCompuestoAcumulado(self.capitalInicTxt.get(),self.tasaTxt.get(),self.periodoTxt.get());
        return resultado;
    def CalcularCapitalFuturo(self,interesT):
        resultado = OperacionesMF.CapitalCompuestoFuturo(self.capitalInicTxt.get(),interesT,self.periodoTxt.get());
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
        