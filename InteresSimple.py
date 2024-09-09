from tkinter import *
from tkinter import ttk
from Operaciones import OperacionesMF
import time;
#Verificacion
import re;

class InterfazInteresSimple:
    def __init__(self,root):
        self.root = root;
        self.MenuInteresS();
        
    def MenuInteresS(self):
        self.tituloLb = ttk.Label(self.root, text="-> Calculo de Interés Simple <-");
        self.tituloLb.grid(column=1,row=1,columnspan=2,sticky=(N,W));
        
        self.check_cap_wrapper = (self.root.register(self.Check_Cap),"%P");
        self.check_num_wrapper = (self.root.register(self.Check_Num),"%P");
        #Lectura Capital
        self.capitalInicTxt = StringVar();
        self.capitalLb = ttk.Label(self.root, text="Capital en Soles (S/.):");
        self.capitalLb.grid(column=1,row=2,columnspan=2,sticky=W);
        self.capital_leer = ttk.Entry(self.root,textvariable=self.capitalInicTxt,validate="key",validatecommand=self.check_cap_wrapper);
        self.capital_leer.grid(column=1,row=3,columnspan=2,sticky=W);
        
        #Lectura Tasa de Interez:
        self.tasaTxt = StringVar();
        self.tasaIntLb = ttk.Label(self.root, text="Tasa de Interés (%):");
        self.tasaIntLb.grid(column=1,row=4,columnspan=2,sticky=W);
        self.tasaInt_leer = ttk.Entry(self.root,textvariable=self.tasaTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.tasaInt_leer.grid(column=1,row=5,columnspan=2,sticky=W);
        ## => Botones Seleccionables
        #Lectura Periodo:
        self.periodoTxt = StringVar();
        self.periodoLb = ttk.Label(self.root, text="Periodo/Tiempo (años):");
        self.periodoLb.grid(column=1,row=7,columnspan=2,sticky=W);
        self.periodo_leer = ttk.Entry(self.root,textvariable=self.periodoTxt,validate="key",validatecommand=self.check_num_wrapper);
        self.periodo_leer.grid(column=1,row=8,columnspan=2,sticky=W);
        ## => Botones Seleccionables
        
        #Mostrar Resultado en Pantalla
        ##Interes
        self.resulIntLb = ttk.Label(self.root,text="Interés Acumulado TOTAL:");
        self.resulIntLb.grid(column=3,row=2,columnspan=2,sticky=(N,E));
        self.interesText = StringVar();
        self.interesLb = ttk.Label(self.root,textvariable=self.interesText);
        self.interesLb.grid(column=3,row=3,columnspan=2,sticky=(N,E));
        ##Capital Futuro
        self.resulCapFutLb = ttk.Label(self.root,text="Capital Futuro TOTAL:");
        self.resulCapFutLb.grid(column=3,row=4,columnspan=2,sticky=(N,E));
        self.capitalFText = StringVar();
        self.capitalFLb = ttk.Label(self.root,textvariable=self.capitalFText);
        self.capitalFLb.grid(column=3,row=5,columnspan=2,sticky=(N,E));
        
        #Boton Interés Acumulado y Capital Futuro
        self.resultadosBt = ttk.Button(self.root, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid(column=1,row=10,columnspan=1,sticky=(W,S));
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.root, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid(column=2,row=10,columnspan=1,sticky=(W,S));
        
    #Validar solo entrada numerica
    def Check_Cap(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=5;
    def Check_Num(self,newval):
        return re.match('^[0-9]*$', newval) is not None and len(newval)<=2;
    
    def CalcularResultados(self):
        print(f"->{self.capitalInicTxt.get()},{self.tasaTxt.get()},{self.periodoTxt.get()}");
        print(f"{type(self.capitalInicTxt)}");
        if((self.capitalInicTxt.get()=="" or self.capitalInicTxt == None) or
           (self.tasaTxt.get()=="" or self.tasaTxt == None) or
           (self.periodoTxt.get()=="" or self.periodoTxt == None)):
            datosBlancos = ttk.Label(self.root, text="Por favor, rellena todos los espacios");
            datosBlancos.grid(column=1,row=11,columnspan=2,sticky=S);
            self.root.after(5000,datosBlancos.destroy);
            return;
        interesT = self.CalcularInteresSimple();
        self.interesText.set(interesT);
        self.capitalFText.set(self.CalcularCapitalFuturo(interesT));
        
    def CalcularInteresSimple(self):
        resultado = OperacionesMF.InteresAcumulado(self,self.capitalInicTxt.get(),self.tasaTxt.get(),self.periodoTxt.get());
        return resultado;
    def CalcularCapitalFuturo(self,interesT):
        resultado = OperacionesMF.CapitalFuturo(self,self.capitalInicTxt.get(),interesT);
        return resultado;
    
    def VolverMenu(self):
        #Limpiamos la pantalla antes de regresar
        self.LimpiarPantalla();
        #Importamos el main.py para poder llamar de nuevo a la interfaz principal
        from main import MatematicasFinancieras;
        MatematicasFinancieras(self.root);
        return;
    def LimpiarPantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy();
        