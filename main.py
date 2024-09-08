from tkinter import *
from tkinter import ttk;
from Operaciones import OperacionesMF;

class MatematicasFinancieras:
    """
    Valor Presente/Capital (Ci/Co o P)
    Tasa de Interés (r o i %)
    Periodo/Tiempo (n)
    Interés (I) = P*i*n
    Valor Futuro/Capital Futuro (Cf o F) = P+I
    """
    #Menu
    #Matematicas Financieras
    #Seleccione el Proceso a realizar:
    #Apartado desglosable ->
    #Seleccionar
    #Salir
    ### Interés Simple
    ## -> Ingrese Capital (S./1000 por defecto)
    ## -> Ingrese Tasa de Interés (0% por defecto)
    ## -> Ingrese Periodo (1 año por defecto)
    ## -> Apartado para mostrar Interés Acumulado
    ## -> Apartado para mostrar Capital Futuro
    ## -> Apartado para mostrar talvez gráficas
    def __init__(self,root):
        #Titulo de la ventana
        root.title("Matemáticas Financieras");
        self.root = root
        self.MenuPrincipal(root);
    
    def IngresarOpcion(self,op):
        print(f"Se ha seleccionado: {op}");
        if(op == "Interes Simple"):
            self.MenuInteresS();
    def SalirPrograma(self):
        root.destroy();
    def MenuInteresS(self):
        
        return;
    def MenuPrincipal(self,root):
        #Creamos el frame de la ventana
        mainframe = ttk.Frame(root,padding="12 3 12 10");
        mainframe.grid(column=0,row=0,sticky=(N,W,E,S));
        root.columnconfigure(0,weight=1);
        root.rowconfigure(0,weight=1);
        #Textos
        ttk.Label(mainframe, text="MATEMATICAS FINANCIERAS").grid(column=2,row=1,sticky=N);
        ttk.Label(mainframe, text="Seleccione una opcion:").grid(column=2,row=2,sticky=W);
        
        #Barra de Seleccion
        op_Seleccionada = StringVar();
        op_Seleccionada.set("-Seleccionar-");
        opciones = ["Interés Simple"];
        #Menu Desplegable
        listDesplegable = OptionMenu(mainframe,op_Seleccionada,*opciones,command=self.IngresarOpcion);
        listDesplegable.grid(column=2,row=3,padx=10,pady=10);

        #Botones
        ttk.Button(mainframe, text="Seleccionar",command=lambda: self.IngresarOpcion(op_Seleccionada.get())).grid(column=1,row=3,sticky=W);
        ttk.Button(mainframe, text="Salir",command=self.SalirPrograma).grid(column=4,row=3,sticky=E);
        #Padding
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5);
        #Evento
        root.mainloop();

#Main Interfaz
root = Tk();
root.geometry("400x300+250+150");
MatematicasFinancieras(root);