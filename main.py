from tkinter import *;
from tkinter import ttk;
from InteresSimple import InterfazInteresSimple;
from InteresCompuesto import InterfazInteresCompuesto;
from Amortizacion import InterfazAmortizacion;
from Anualidad import InterfazAnualidadVencida;
from Gradiente import InterfazGradientes;
from Depreciacion import InterfazDepreciacion;
from VAN import InterfazVAN;
from TIR import InterfazTIR;
from PEI import InterfazPEI;

class MatematicasFinancieras:
    def __init__(self, root):
        # Titulo de la ventana
        root.title("Matemáticas Financieras")
        # Root principal
        self.root = root
        self.timer_id = None
        # Llamada a la interfaz Principal
        self.MenuPrincipal(root)

    def IngresarOpcion(self):
        # Obtener el valor actual del combobox
        op = self.combobox.get();
        # Si se selecciona la opcion que solo sirve de guia
        if op == "-Seleccionar-" or op == "" or op==None:
            # Arrojar un pequeño error
            opIncorrecta = ttk.Label(self.root, text="Por favor, selecciona una opción válida",font=("Helvetica", 7, "bold"), foreground="red");
            opIncorrecta.grid(column=2, row=5, columnspan=2, sticky=(N, W));
            self.timer_id = self.root.after(5000, opIncorrecta.destroy);
        else:
            # Ocultar la ventana principal
            self.root.withdraw();
            # Llamar al Método de las otras interfaces
            if op == "Interes Simple":
                self.ventanaIS = InterfazInteresSimple(self.root);
            elif op == "Interes Compuesto":
                self.ventanaIC = InterfazInteresCompuesto(self.root);
            elif op == "Amortizaciones":
                self.ventanaAmort = InterfazAmortizacion(self.root);
            elif op == "Anualidad Vencida":
                self.ventanaAV = InterfazAnualidadVencida(self.root);
            elif op == "Gradiente Aritmetica":
                self.ventanaGA = InterfazGradientes(self.root);
            elif op == "Depreciacion Linea Recta":
                self.ventanaDL = InterfazDepreciacion(self.root);
            elif op == "VAN":
                self.ventanaVAN = InterfazVAN(self.root);
            elif op == "TIR":
                self.ventanaTIR = InterfazTIR(self.root);
            elif op == "PEI":
                self.ventanaPEI = InterfazPEI(self.root);
    # Salir del Programa
    def SalirPrograma(self):
        # Destruye el root principal
        self.root.destroy();

    # Operaciones de apoyo para evitar bugs
    def Cerrado_manual(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id);
        self.root.destroy();
        print("El programa se ha cerrado correctamente.");

    # Interfaz principal
    def MenuPrincipal(self, root):
        # Grid
        root.columnconfigure([0, 1, 2, 3, 4], weight=1);
        root.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1);

        # Textos Principales
        self.lb1 = ttk.Label(root, text="MATEMATICAS FINANCIERAS", font=("Helvetica", 10, "bold"));
        self.lb1.grid(column=2, row=1, columnspan=2, sticky=N);
        self.lb2 = ttk.Label(root, text="Seleccione una opción:");
        self.lb2.grid(column=2, row=2, columnspan=2, sticky=(N, S), padx=4);

        # Menú Desplegable
        self.textoComboBox = StringVar(value="-Seleccionar-");
        self.opciones = ["Interes Simple", "Interes Compuesto", "Amortizaciones", "Anualidad Vencida", "Gradiente Aritmetica", "Depreciacion Linea Recta", "VAN", "TIR", "PEI"];
        self.combobox = ttk.Combobox(root, textvariable=self.textoComboBox, values=self.opciones);
        self.combobox["state"] = "readonly";
        self.combobox.grid(column=2, row=3, padx=5, pady=1, sticky=(E, W));

        # Botones
        selB = ttk.Button(root, text="Seleccionar", command=self.IngresarOpcion);
        selB.grid(column=1, row=3, padx=10, sticky=(E, W));
        exitB = ttk.Button(root, text="Salir", command=self.SalirPrograma);
        exitB.grid(column=4, row=3, padx=10, sticky=(E, W));

        # =================================================== 
        # Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.root.protocol("WM_DELETE_WINDOW", self.Cerrado_manual);
        # Evento
        root.mainloop();

# Main Interfaz
root = Tk();
# Tamaño y posición de la ventana
root.geometry("400x250+250+150");
# Llamar al método principal
MatematicasFinancieras(root);