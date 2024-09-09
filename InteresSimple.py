from tkinter import *
from tkinter import ttk
from Operaciones import OperacionesMF
#Grafico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#Verificacion
import re;

class InterfazInteresSimple:
    def __init__(self,root):
        self.root = root;
        self.interfazIS = Toplevel();
        self.interfazIS.geometry("600x400+250+150");
        self.interfazIS.title("Calculando Interes Simple");
        self.timer_id = None;
        self.datosBlancos = None;
        self.MenuInteresS();
        
    def MenuInteresS(self):
        self.tituloLb = ttk.Label(self.interfazIS, text="-> Calculo de Interés Simple <-");
        self.tituloLb.grid(column=1,row=1,columnspan=2,sticky=(N,W));
        self.check_cap_wrapper = (self.interfazIS.register(self.Check_Cap),"%P");
        self.check_num_wrapper = (self.interfazIS.register(self.Check_Num),"%P");
        #Lectura Capital
        self.capitalInicTxt = StringVar();
        self.capitalLb = ttk.Label(self.interfazIS, text="Capital en Soles (S/.):");
        self.capitalLb.grid(column=1,row=2,columnspan=2,sticky=W);
        self.capital_leer = ttk.Entry(self.interfazIS,textvariable=self.capitalInicTxt,validate="key",validatecommand=self.check_cap_wrapper);
        self.capital_leer.grid(column=1,row=3,columnspan=2,sticky=W);
        
        #Lectura Tasa de Interez:
        self.tasaTxt = StringVar();
        self.tasaIntLb = ttk.Label(self.interfazIS, text="Tasa de Interés (%):");
        self.tasaIntLb.grid(column=1,row=4,columnspan=2,sticky=W);
        self.tasaInt_leer = ttk.Entry(self.interfazIS,textvariable=self.tasaTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.tasaInt_leer.grid(column=1,row=5,columnspan=2,sticky=W);
        ## => Botones Seleccionables
        #Lectura Periodo:
        self.periodoTxt = StringVar();
        self.periodoLb = ttk.Label(self.interfazIS, text="Periodo/Tiempo (años):");
        self.periodoLb.grid(column=1,row=7,columnspan=2,sticky=W);
        self.periodo_leer = ttk.Entry(self.interfazIS,textvariable=self.periodoTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.periodo_leer.grid(column=1,row=8,columnspan=2,sticky=W);
        ## => Botones Seleccionables
        
        #Mostrar Resultado en Pantalla
        ##Interes
        self.resulIntLb = ttk.Label(self.interfazIS,text="Interés Acumulado TOTAL:");
        self.resulIntLb.grid(column=3,row=2,columnspan=2,sticky=(N,E));
        self.interesText = StringVar();
        self.interesLb = ttk.Label(self.interfazIS,textvariable=self.interesText);
        self.interesLb.grid(column=3,row=3,columnspan=2,sticky=(N,E));
        ##Capital Futuro
        self.resulCapFutLb = ttk.Label(self.interfazIS,text="Capital Futuro TOTAL:");
        self.resulCapFutLb.grid(column=3,row=4,columnspan=2,sticky=(N,E));
        self.capitalFText = StringVar();
        self.capitalFLb = ttk.Label(self.interfazIS,textvariable=self.capitalFText);
        self.capitalFLb.grid(column=3,row=5,columnspan=2,sticky=(N,E));
        
        #Boton Interés Acumulado y Capital Futuro
        self.resultadosBt = ttk.Button(self.interfazIS, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=1,row=10,columnspan=1,sticky=(W,S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.interfazIS, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=2,row=10,columnspan=1,sticky=(W,S));
        #Grafico pie
        self.grafico_frame = ttk.Frame(self.interfazIS);
        self.grafico_frame.grid(column=3, row=1, rowspan=9, padx=10, pady=10, sticky=(N,E,S,W));
        #Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.interfazIS.protocol("WM_DELETE_WINDOW",self.Cerrado_manual);
    
    def Cerrado_manual(self):
        if self.timer_id is not None:
            self.interfazIS.after_cancel(self.timer_id);
        self.interfazIS.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");
    #Validar solo entrada numerica
    def Check_Cap(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=5;
    def Check_Num(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=2;
    
    def CalcularResultados(self):
        if((self.capitalInicTxt.get()=="" or self.capitalInicTxt == None) or
           (self.tasaTxt.get()=="" or self.tasaTxt == None) or
           (self.periodoTxt.get()=="" or self.periodoTxt == None)):
            if self.datosBlancos is not None:
                self.datosBlancos.destroy();
            self.datosBlancos = ttk.Label(self.interfazIS, text="Por favor, rellena todos los espacios");
            self.datosBlancos.grid(column=1,row=11,columnspan=2,sticky=S);
            self.timer_id = self.interfazIS.after(5000,self.datosBlancos.destroy);
            return;
        interesT = self.CalcularInteresSimple();
        capitalFuturo = self.CalcularCapitalFuturo(interesT);
        self.interesText.set(interesT);
        self.capitalFText.set(capitalFuturo);
        #Mostrar Grafico
        self.MostrarGrafico(self.capitalInicTxt.get(),interesT,capitalFuturo);
    
    def MostrarGrafico(self, capitalInicial, interesT, capitalFuturo):
        # Limpiar el área del gráfico antes de dibujar uno nuevo
        for widget in self.grafico_frame.winfo_children():
            widget.destroy();
        
        # Datos para el gráfico
        etiquetas = ['Capital Inicial', 'Interés'];
        valores = [float(capitalInicial), float(interesT)];
        
        # Crear gráfico de pie
        fig, ax = plt.subplots(figsize=(4,3));
        ax.set_title("Capital VS Interes");
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90);
        ax.axis('equal')  # Verificar grafico es circulo cerrado.
        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame);
        canvas.draw();
        canvas.get_tk_widget().pack(fill=BOTH, expand=True);
    
    def CalcularInteresSimple(self):
        resultado = OperacionesMF.InteresAcumulado(self,self.capitalInicTxt.get(),self.tasaTxt.get(),self.periodoTxt.get());
        return resultado;
    def CalcularCapitalFuturo(self,interesT):
        resultado = OperacionesMF.CapitalFuturo(self,self.capitalInicTxt.get(),interesT);
        return resultado;
    
    def VolverMenu(self):
        if self.interfazIS.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazIS.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();
        