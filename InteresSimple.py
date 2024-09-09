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
        self.capitalLb = ttk.Label(self.root, text="Capital en Soles (S/.):");
        self.capitalLb.grid();
        self.capital_leer = ttk.Entry(self.root);
        self.capital_leer.grid();
        
        #Lectura Tasa de Interez:
        self.tasaIntLb = ttk.Label(self.root, text="Tasa de Interés (%):");
        self.tasaIntLb.grid();
        self.tasaInt_leer = ttk.Entry(self.root);
        self.tasaInt_leer.grid();
        
        #Lectura Periodo:
        self.periodoLb = ttk.Label(self.root, text="Periodo/Tiempo (años):");
        self.periodoLb.grid();
        self.periodo_leer = ttk.Entry(self.root);
        self.periodo_leer.grid();
        
        #Boton Interés Acumulado y Capital Futuro
        self.resultadosBt = ttk.Button(self.root, text="Calcular",command=self.CalcularResultados)
        self.resultadosBt.grid();
        
        #Boton Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.root, text="Volver Menu",command=self.VolverMenu)
        self.volverMenuBt.grid();
        
    def CalcularResultados():
        return;
    def VolverMenu():
        return;
    def LimpiarPantalla():
        return;
        