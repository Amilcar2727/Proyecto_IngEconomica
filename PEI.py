from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazPEI:
    def __init__(self, root):
        self.root = root
        self.interfazPEI = Toplevel()
        self.interfazPEI.geometry("400x400+250+25")
        self.interfazPEI.title("Calculando PEI")
        self.MenuPEI()

    def MenuPEI(self):
        self.datos_frame = ttk.Frame(self.interfazPEI, borderwidth=5, relief="solid", width=380, height=380)
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10, padx=10, sticky=(N, E, S, W))
        self.datos_frame.grid_propagate(False)

        self.tituloLb = ttk.Label(self.datos_frame, text="CALCULO DEL PEI", font=("Helvetica", 12, "bold"))
        self.tituloLb.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky=(N, S, W))

        # Lectura Inversión Inicial
        self.inversionInicialTxt = StringVar()
        self.inversionInicialLb = ttk.Label(self.datos_frame, text="Inversión Inicial:")
        self.inversionInicialLb.grid(column=0, row=1, padx=5, pady=5, sticky=W)
        self.inversionInicial_leer = ttk.Entry(self.datos_frame, textvariable=self.inversionInicialTxt)
        self.inversionInicial_leer.grid(column=1, row=1, padx=5, pady=5, sticky=(W, E))

        # Lectura Flujos de Efectivo
        self.flujosTxt = StringVar()
        self.flujosLb = ttk.Label(self.datos_frame, text="Flujos de Efectivo (separados por comas):")
        self.flujosLb.grid(column=0, row=2, padx=5, pady=5, sticky=W)
        self.flujos_leer = ttk.Entry(self.datos_frame, textvariable=self.flujosTxt)
        self.flujos_leer.grid(column=1, row=2, padx=5, pady=5, sticky=(W, E))

        # Botón Calcular PEI
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular", command=self.CalcularPEI)
        self.resultadosBt.grid(column=0, row=3, padx=5, pady=(30, 10), sticky=(S))

        # Botón Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu", command=self.VolverMenu)
        self.volverMenuBt.grid(column=1, row=3, padx=5, pady=(30, 10), sticky=(S))

        # Evitar bugs cerrando la ventana
        self.interfazPEI.protocol("WM_DELETE_WINDOW", self.Cerrado_manual)

    # Mostrar Resultados
    def MostrarResultados(self):
        # Frame para los resultados
        self.resultados_frame = ttk.Frame(self.interfazPEI, borderwidth=5, relief="groove", width=380, height=180)
        self.resultados_frame.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky=(N, E, S, W))
        self.resultados_frame.grid_propagate(False)

        # Título
        self.tituloResultadosLb = ttk.Label(self.resultados_frame, text="RESULTADOS:", font=("Helvetica", 10, "bold"))
        self.tituloResultadosLb.grid(column=0, row=0, padx=5, pady=5, sticky=(W, N))

        # PEI
        self.resulPEI_Lb = ttk.Label(self.resultados_frame, text="Periodo de Equilibrio de Inversión (PEI):", font=("Helvetica", 9, "bold"))
        self.resulPEI_Lb.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
        self.peiText = StringVar()
        self.pei_Lb = ttk.Label(self.resultados_frame, textvariable=self.peiText)
        self.pei_Lb.grid(column=0, row=2, padx=5, pady=(0, 5), sticky=(W, N))

        # Gráfico de flujos acumulados
        self.grafico_frame = ttk.Frame(self.resultados_frame)
        self.grafico_frame.grid(column=0, row=3, rowspan=2, pady=10, sticky=(N, E, S, W))

    # Calcular PEI
    def CalcularPEI(self):
        if not self.ValidarEntradas():
            return

        self.MostrarResultados()
        inversionInicial = float(self.inversionInicialTxt.get())
        flujos = list(map(float, self.flujosTxt.get().split(',')))
        pei, flujos_acumulados = self.CalcularPeriodoEquilibrio(inversionInicial, flujos)
        self.peiText.set(pei)
        self.MostrarGrafico(flujos_acumulados)

    # Validar Entradas
    def ValidarEntradas(self):
        if not all([self.inversionInicialTxt.get(), self.flujosTxt.get()]):
            ttk.Label(self.datos_frame, text="Rellena todos los campos", foreground="red").grid(column=0, row=4, columnspan=2)
            return False
        return True

    def MostrarGrafico(self, flujos_acumulados):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        n = len(flujos_acumulados)
        fig, ax = plt.subplots()
        ax.plot(range(n), flujos_acumulados, marker='o', label='Flujos Acumulados')
        ax.axhline(y=0, color='r', linestyle='--', label='Equilibrio')
        ax.set_title("Flujos de Efectivo Acumulados")
        ax.set_xlabel("Periodo")
        ax.set_ylabel("Flujos Acumulados")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.get_tk_widget().grid(row=0, column=0, pady=10)
        canvas.draw()

    def CalcularPeriodoEquilibrio(self, inversionInicial, flujos):
        flujos_acumulados = [0]
        acumulado = -inversionInicial
        for flujo in flujos:
            acumulado += flujo
            flujos_acumulados.append(acumulado)
            if acumulado >= 0:
                break
        pei = flujos.index(flujo) if acumulado >= 0 else "Inversión no recuperada"
        return pei, flujos_acumulados

    def VolverMenu(self):
        self.interfazPEI.destroy()

    def Cerrado_manual(self):
        self.interfazPEI.destroy()