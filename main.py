from tkinter import *;
from tkinter import ttk;
from InteresSimple import InterfazInteresSimple;

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
    
    def IngresarOpcion(self):
        op = self.combobox.get();
        #Si no se seleccionó ninguna opcion, marca error:
        if(op=="-Seleccionar-"):
            opIncorrecta = ttk.Label(self.root, text="Por favor, selecciona una opción valida");
            opIncorrecta.grid(column=2,row=4,columnspan=3,sticky=N);
            self.root.after(5000,opIncorrecta.destroy);
        elif(op == "Interes Simple"):
            # Ocultar la ventana principal
            self.root.withdraw()
            self.ventanaIS = InterfazInteresSimple(self.root);
            
    def SalirPrograma(self):
        self.root.destroy();
    def MenuPrincipal(self,root):
        #Grid
        root.columnconfigure([0,1,2,3,4],weight=1);
        root.rowconfigure([0,1,2,3,4],weight=1); 
        
        #Textos
        self.lb1 = ttk.Label(root, text="MATEMATICAS FINANCIERAS",font=("Helvetica", 10, "bold"))
        self.lb1.grid(column=2,row=1,columnspan=2,sticky=N);
        self.lb2 = ttk.Label(root, text="Seleccione una opcion:")
        self.lb2.grid(column=2,row=2,columnspan=2,sticky=(N,S),padx=4);
        
        #Menu Desplegable
        self.textoComboBox = StringVar(value="-Seleccionar-");
        self.opciones = ['Interes Simple'];
        self.combobox = ttk.Combobox(root, textvariable=self.textoComboBox,values=self.opciones);
        self.combobox["state"]="readonly";
        self.combobox.grid(column=2,row=3,padx=5,pady=1,sticky=(E,W));
        
        #Botones
        selB = ttk.Button(root, text="Seleccionar",command=self.IngresarOpcion)
        selB.grid(column=1,row=3,padx=10,sticky=(E,W));
        exitB = ttk.Button(root, text="Salir",command=self.SalirPrograma)
        exitB.grid(column=4,row=3,padx=10,sticky=(E,W));
        #Evento
        root.mainloop();

#Main Interfaz
root = Tk();
root.geometry("400x250+250+150");
MatematicasFinancieras(root);