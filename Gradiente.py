from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

class InterfazFV:
    # Método Inicial
    def __init__(self, root):
        self.root = root
        self.interfazFV = Toplevel()
        self.interfazFV.geometry("400x400+250+25")
        self.interfazFV.title("Cálculo de Valor Futuro (FV)")
        self.timer_id = None
        self.datosBlancos = None

        # Inicializamos el frame para gráficos
        self.grafico_frame = ttk.Frame(self.interfazFV, borderwidth=5, relief="groove", width=300, height=200)
        self.grafico_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky=(N, E, S, W))
        self.grafico_frame.grid_propagate(False)

        self.MenuFV()

    # Interfaz Valor Futuro
    def MenuFV(self):
        self.datos_frame = ttk.Frame(self.interfazFV, borderwidth=5, relief="solid", width=300, height=300)
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10, padx=10, sticky=(N, E, S, W))
        self.datos_frame.grid_propagate(False)

        self.tituloLb = ttk.Label(self.datos_frame, text="CÁLCULO DE VALOR FUTURO", font=("Helvetica", 12, "bold"))
        self.tituloLb.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky=(N, S, W))

        # Lectura Valor Actual (PV)
        self.pvTxt = StringVar()
        self.pvLb = ttk.Label(self.datos_frame, text="Valor Actual (PV):")
        self.pvLb.grid(column=0, row=1, padx=5, pady=5, sticky=W)
        self.pv_leer = ttk.Entry(self.datos_frame, textvariable=self.pvTxt)
        self.pv_leer.grid(column=1, row=1, padx=5, pady=5, sticky=(W, E))

        # Lectura Tasa de Interés (r)
        self.tasaTxt = StringVar()
        self.tasaLb = ttk.Label(self.datos_frame, text="Tasa de Interés (r):")
        self.tasaLb.grid(column=0, row=2, padx=4, pady=4, sticky=W)
        self.tasa_leer = ttk.Entry(self.datos_frame, textvariable=self.tasaTxt)
        self.tasa_leer.grid(column=1, row=2, padx=5, pady=5, sticky=(W, E))

        # Lectura Número de Periodos (n)
        self.nTxt = StringVar()
        self.nLb = ttk.Label(self.datos_frame, text="Número de Periodos (n):")
        self.nLb.grid(column=0, row=3, padx=5, pady=5, sticky=W)
        self.n_leer = ttk.Entry(self.datos_frame, textvariable=self.nTxt)
        self.n_leer.grid(column=1, row=3, padx=5, pady=5, sticky=(W, E))

        # Botón Calcular
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular", command=self.CalcularResultados)
        self.resultadosBt.grid(column=0, row=4, padx=5, pady=(30, 10), sticky=(S))

        # Botón Volver al Menú Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menú", command=self.VolverMenu)
        self.volverMenuBt.grid(column=1, row=4, padx=5, pady=(30, 10), sticky=(S))

        # Evitar bugs y cerrando timers antes de un cerrado por el usuario
        self.interfazFV.protocol("WM_DELETE_WINDOW", self.Cerrado_manual)

    # Mostrar resultados
    def MostrarResultados(self, fv):
        self.resultados_frame = ttk.Frame(self.interfazFV, borderwidth=5, relief="groove", width=210, height=200)
        self.resultados_frame.grid(column=1, row=0, rowspan=7, padx=(0, 10), pady=10, sticky=(N, E, S, W))
        self.resultados_frame.grid_propagate(False)

        # Titulo
        self.tituloResultadosLb = ttk.Label(self.resultados_frame, text="RESULTADOS:", font=("Helvetica", 10, "bold"))
        self.tituloResultadosLb.grid(column=0, row=0, padx=5, pady=5, sticky=(W, N))

        # Valor Futuro
        self.resulFvLb = ttk.Label(self.resultados_frame, text="Valor Futuro (FV):", font=("Helvetica", 9, "bold"))
        self.resulFvLb.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
        self.fvText = StringVar()
        self.fvLb = ttk.Label(self.resultados_frame, textvariable=self.fvText)
        self.fvLb.grid(column=0, row=2, padx=5, pady=(0, 5), sticky=(W, N))

        # Mostrar resultado en pantalla
        self.fvText.set(f"{fv:.2f}")

    # Calcular resultado de FV
    def CalcularResultados(self):
        if (self.pvTxt.get() == "" or self.pvTxt.get() == None) or (self.tasaTxt.get() == "" or self.tasaTxt.get() == None) or (self.nTxt.get() == "" or self.nTxt.get() == None):
            # Si hay datos en blanco, solicitar los datos
            if self.datosBlancos is not None:
                self.datosBlancos.destroy()
            self.datosBlancos = ttk.Label(self.datos_frame, text="Por favor, rellena todos los espacios", font=("Helvetica", 9, "bold"), foreground="red")
            self.datosBlancos.grid(column=0, row=5, columnspan=2, sticky=(S, W))
            self.timer_id = self.datos_frame.after(5000, self.datosBlancos.destroy)
            return

        # Lógica para calcular el valor futuro
        pv = float(self.pvTxt.get())
        r = float(self.tasaTxt.get()) / 100  # Convertir a decimal
        n = int(self.nTxt.get())

        fv = pv * (1 + r) ** n
        self.MostrarResultados(fv)
        self.MostrarGrafico(pv, fv)

    # Mostrar gráfico de barras
    def MostrarGrafico(self, pv, fv):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        etiquetas = ['PV', 'FV']
        valores = [pv, fv]

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(etiquetas, valores, color=['blue', 'green'])
        ax.set_ylabel('Valor (S/.)')
        ax.set_title('Cálculo de Valor Futuro')

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    # Función de cerrar ventana manualmente
    def Cerrado_manual(self):
        self.interfazFV.destroy()

    # Función para volver al menú principal
    def VolverMenu(self):
        self.interfazFV.destroy();