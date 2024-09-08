from tkinter import *
from tkinter import ttk;

class MatematicasFinancieras:
    def __init__(self,root):
        #Titulo de la ventana
        root.title("Matemáticas Financieras");
        self.MenuPrincipal(root);
    
    def IngresarOpcion(self,op):
        return print(f"Se ha seleccionado: {op}");
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
        opciones = ["Interés Simple","N.A"];
        #Menu Desplegable
        listDesplegable = OptionMenu(mainframe,op_Seleccionada,*opciones,command=self.IngresarOpcion);
        listDesplegable.grid(column=2,row=3,padx=10,pady=10);

        #Botones
        ttk.Button(mainframe, text="Seleccionar",command=self.IngresarOpcion(op_Seleccionada.get())).grid(column=1,row=3,sticky=W);
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