from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazVAN:
    def __init__(self, root):
        self.root = root
        self.interfazVAN = Toplevel()
        self.interfazVAN.geometry("320x400+250+25")
        self.interfazVAN.title("Cálculo de VAN")
        self.MenuVAN()

    def MenuVAN(self):
        # Frame principal
        self.datos_frame = ttk.Frame(self.interfazVAN, borderwidth=5, relief="solid", width=300, height=400)
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10, padx=10, sticky=(N, E, S, W))
        self.datos_frame.grid_propagate(False)

        # Título
        self.tituloLb = ttk.Label(self.datos_frame, text="CÁLCULO DE VAN", font=("Helvetica", 12, "bold"))
        self.tituloLb.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky=(N, S, W))

        # Ingreso de flujos de caja
        self.flujosTxt = StringVar()
        self.flujosLb = ttk.Label(self.datos_frame, text="Flujos de caja (separados por comas):")
        self.flujosLb.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky=W)
        self.flujos_leer = ttk.Entry(self.datos_frame, textvariable=self.flujosTxt, width=40)
        self.flujos_leer.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=(W, E))

        # Ingreso de tasa de descuento
        self.tasaTxt = StringVar()
        self.tasaLb = ttk.Label(self.datos_frame, text="Tasa de descuento (%):")
        self.tasaLb.grid(column=0, row=3, padx=5, pady=5, sticky=W)
        self.tasa_leer = ttk.Entry(self.datos_frame, textvariable=self.tasaTxt)
        self.tasa_leer.grid(column=1, row=3, padx=5, pady=5, sticky=(W, E))

        # Botón para calcular el VAN
        self.calcularBt = ttk.Button(self.datos_frame, text="Calcular", command=self.CalcularVAN)
        self.calcularBt.grid(column=0, row=4, padx=5, pady=20, sticky=(N, S, W, E))

        # Botón Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu", command=self.VolverMenu)
        self.volverMenuBt.grid(column=1, row=4, padx=5, pady=10)
        
        # Evitar cerrar incorrectamente la ventana
        self.interfazVAN.protocol("WM_DELETE_WINDOW", self.Cerrado_manual)

    def CalcularVAN(self):
        # Validar entradas
        if not self.flujosTxt.get() or not self.tasaTxt.get():
            self.MostrarMensaje("Por favor, ingresa todos los datos.", "red")
            return

        try:
            # Parsear entradas
            flujos = list(map(float, self.flujosTxt.get().split(',')))
            tasa_descuento = float(self.tasaTxt.get()) / 100

            # Calcular VAN
            van, flujos_descontados = self.calcular_van(flujos, tasa_descuento)
            self.MostrarResultados(van, flujos_descontados)

        except ValueError:
            self.MostrarMensaje("Por favor, ingresa datos válidos.", "red")

    def calcular_van(self, flujos, tasa_descuento):
        """
        Calcula el VAN y los flujos descontados.
        """
        flujos_descontados = [flujo / (1 + tasa_descuento) ** i for i, flujo in enumerate(flujos)]
        van = sum(flujos_descontados)
        return round(van, 2), flujos_descontados

    def MostrarResultados(self, van, flujos_descontados):
        # Crear una nueva ventana de resultados
        resultados_frame = ttk.Frame(self.interfazVAN, borderwidth=5, relief="groove", width=300, height=400)
        resultados_frame.grid(column=0, row=5, rowspan=7, padx=10, pady=10, sticky=(N, E, S, W))
        resultados_frame.grid_propagate(False)

        # Mostrar VAN
        vanLb = ttk.Label(resultados_frame, text=f"VAN Calculado: {van}", font=("Helvetica", 10, "bold"))
        vanLb.grid(column=0, row=0, padx=5, pady=10, sticky=W)

        # Mostrar gráfico
        self.MostrarGrafico(flujos_descontados)

    def MostrarGrafico(self, flujos_descontados):
        # Crear gráfico de barras
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(range(len(flujos_descontados)), flujos_descontados, color='skyblue', edgecolor='black')
        ax.set_title("Flujos de caja descontados")
        ax.set_xlabel("Periodo")
        ax.set_ylabel("Valor descontado")
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.interfazVAN)
        canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)
        canvas.draw()

    def MostrarMensaje(self, mensaje, color):
        # Mostrar mensaje de error o información
        mensajeLb = ttk.Label(self.datos_frame, text=mensaje, foreground=color)
        mensajeLb.grid(column=0, row=5, columnspan=2, pady=5, sticky=W)

    def VolverMenu(self):
        if self.interfazVAN.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazVAN.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();

    def Cerrado_manual(self):
        self.interfazVAN.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");