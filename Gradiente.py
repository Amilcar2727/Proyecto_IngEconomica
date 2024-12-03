from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazGradientes:
    def __init__(self, root):
        self.root = root
        self.interfazGradientes = Toplevel()
        self.interfazGradientes.geometry("600x500+250+50")
        self.interfazGradientes.title("Cálculo de Gradientes")
        self.datosBlancos = None
        self.crearMenu()

    def crearMenu(self):
        # Frame principal
        self.datos_frame = ttk.Frame(self.interfazGradientes, borderwidth=5, relief="solid", width=580, height=240)
        self.datos_frame.grid(column=0, row=0, pady=10, padx=10, sticky=(N, E, S, W))
        self.datos_frame.grid_propagate(False)

        # Título
        self.tituloLb = ttk.Label(self.datos_frame, text="CÁLCULO DE GRADIENTES", font=("Helvetica", 14, "bold"))
        self.tituloLb.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky=W)

        # Selección de tipo de gradiente
        self.tipoGradiente = StringVar(value="Valor Presente Creciente")
        self.tipoGradienteLb = ttk.Label(self.datos_frame, text="Selecciona el tipo de gradiente:")
        self.tipoGradienteLb.grid(column=0, row=1, padx=5, pady=5, sticky=W)

        self.gradienteOpciones = ttk.Combobox(self.datos_frame, textvariable=self.tipoGradiente, state="readonly")
        self.gradienteOpciones['values'] = [
            "Valor Presente Creciente",
            "Valor Futuro Creciente",
            "Valor Presente Decreciente",
            "Cuota N-ésima"
        ]
        self.gradienteOpciones.grid(column=1, row=1, padx=5, pady=5, sticky=(W, E))

        # Entrada de datos
        self.entrada_frame = ttk.Frame(self.datos_frame)
        self.entrada_frame.grid(column=0, row=2, columnspan=2, pady=10, sticky=(N, E, S, W))

        self.entradas = {
            "Monto Inicial (A)": StringVar(),
            "Tasa de Interés (i)": StringVar(),
            "Gradiente (G)": StringVar(),
            "Número de Períodos (n)": StringVar()
        }
        self.entradas_widgets = {}

        for i, (label, var) in enumerate(self.entradas.items()):
            lb = ttk.Label(self.entrada_frame, text=label)
            lb.grid(column=0, row=i, padx=5, pady=5, sticky=W)

            entry = ttk.Entry(self.entrada_frame, textvariable=var)
            entry.grid(column=1, row=i, padx=5, pady=5, sticky=(W, E))
            self.entradas_widgets[label] = entry

        # Botón Calcular
        self.calcularBt = ttk.Button(self.datos_frame, text="Calcular", command=self.calcularGradiente)
        self.calcularBt.grid(column=0, row=3, columnspan=2, pady=10)

        # Frame para el gráfico
        self.grafico_frame = ttk.Frame(self.interfazGradientes, borderwidth=5, relief="groove", width=580, height=240)
        self.grafico_frame.grid(column=0, row=1, padx=10, pady=10, sticky=(N, E, S, W))

    def calcularGradiente(self):
        # Leer los valores de entrada
        try:
            A = float(self.entradas["Monto Inicial (A)"].get())
            i = float(self.entradas["Tasa de Interés (i)"].get())
            G = float(self.entradas["Gradiente (G)"].get())
            n = int(self.entradas["Número de Períodos (n)"].get())
        except ValueError:
            self.mostrarError("Por favor, ingresa valores válidos.")
            return

        # Determinar el tipo de gradiente seleccionado
        tipo = self.tipoGradiente.get()

        if tipo == "Valor Presente Creciente":
            resultado = self.valorPresenteCreciente(A, G, i, n)
        elif tipo == "Valor Futuro Creciente":
            resultado = self.valorFuturoCreciente(A, G, i, n)
        elif tipo == "Valor Presente Decreciente":
            resultado = self.valorPresenteDecreciente(A, G, i, n)
        elif tipo == "Cuota N-ésima":
            resultado = self.cuotaNesima(A, G, i, n)
        else:
            self.mostrarError("Selecciona un tipo de gradiente válido.")
            return

        # Mostrar los resultados en un gráfico
        self.mostrarGrafico(tipo, resultado, n)

    def valorPresenteCreciente(self, A, G, i, n):
        return [A + G * t for t in range(n + 1)]

    def valorFuturoCreciente(self, A, G, i, n):
        return [A * (1 + i)**t + G * t for t in range(n + 1)]

    def valorPresenteDecreciente(self, A, G, i, n):
        return [A - G * t for t in range(n + 1)]

    def cuotaNesima(self, A, G, i, n):
        return [A + G * t * (1 + i)**t for t in range(n + 1)]

    def mostrarGrafico(self, tipo, valores, n):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        # Crear gráfico de líneas
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(range(n + 1), valores, marker='o', linestyle='-', label=tipo)
        ax.set_title(f"Gradiente: {tipo}", fontsize=12)
        ax.set_xlabel("Período (n)", fontsize=10)
        ax.set_ylabel("Valor", fontsize=10)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)

        # Integrar gráfico con Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky=(N, S, E, W))

        # Asegurar que el gráfico se ajuste correctamente
        self.grafico_frame.columnconfigure(0, weight=1)
        self.grafico_frame.rowconfigure(0, weight=1)
        canvas.draw()

    def mostrarError(self, mensaje):
        if self.datosBlancos is not None:
            self.datosBlancos.destroy()

        self.datosBlancos = ttk.Label(self.datos_frame, text=mensaje, font=("Helvetica", 9, "bold"), foreground="red")
        self.datosBlancos.grid(column=0, row=4, columnspan=2, pady=10)
    
    def VolverMenu(self):
        if self.interfazGradientes.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazGradientes.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();

    def Cerrado_manual(self):
        self.interfazGradientes.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");