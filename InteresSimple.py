from tkinter import *
from tkinter import ttk
from Operaciones import OperacionesMF

class InterfazInteresSimple:
    def __init__(self,root):
        self.root = root;
        self.MenuInteresS();
    def MenuInteresS(self):
        self.tituloLb = ttk.Label(self.root, text="-> Calculo de Interés Simple <-");
        self.tituloLb.grid();
        
        #Lectura Capital
        self.capitalInicTxt = StringVar();
        self.capitalLb = ttk.Label(self.root, text="Capital en Soles (S/.):");
        self.capitalLb.grid();
        self.capital_leer = ttk.Entry(self.root,textvariable=self.capitalInicTxt);
        self.capital_leer.grid();
        
        #Lectura Tasa de Interez:
        self.tasaTxt = StringVar();
        self.tasaIntLb = ttk.Label(self.root, text="Tasa de Interés (%):");
        self.tasaIntLb.grid();
        self.tasaInt_leer = ttk.Entry(self.root,textvariable=self.tasaTxt);
        self.tasaInt_leer.grid();
        
        #Lectura Periodo:
        self.periodoTxt = StringVar();
        self.periodoLb = ttk.Label(self.root, text="Periodo/Tiempo (años):");
        self.periodoLb.grid();
        self.periodo_leer = ttk.Entry(self.root,textvariable=self.periodoTxt);
        self.periodo_leer.grid();
        
        #Mostrar Resultado en Pantalla
        ##Interes
        self.interesText = StringVar();
        self.interesLb = ttk.Label(self.root,textvariable=self.interesText);
        self.interesLb.grid();
        ##Capital Futuro
        self.capitalFText = StringVar();
        self.capitalFLb = ttk.Label(self.root,textvariable=self.capitalFText);
        self.capitalFLb.grid();
        
        #Boton Interés Acumulado y Capital Futuro
        self.resultadosBt = ttk.Button(self.root, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid();
        
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.root, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid();
        
    def CalcularResultados(self):
        self.interesText.set(self.CalcularInteresSimple());
        self.capitalFText.set(self.CalcularCapitalFuturo());
        
    def CalcularInteresSimple(self):
        resultado = OperacionesMF.InteresAcumulado(self,self.capitalInicTxt.get(),self.tasaTxt.get(),self.periodoTxt.get());
        return resultado;
    def CalcularCapitalFuturo(self):
        resultado = OperacionesMF.CapitalFuturo(self,self.capitalInicTxt.get(),self.interesText.get());
        return resultado;
    
    def VolverMenu(self):
        return;
    def LimpiarPantalla(self):
        return;
        