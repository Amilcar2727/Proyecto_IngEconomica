from tkinter import *
from tkinter import ttk
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Operaciones import OperacionesMF  # Asegúrate de tener estas operaciones definidas

class InterfazAnualidadVencida:
    def __init__(self, root):
        self.root = root
        self.interfazAV = Toplevel()
        self.interfazAV.geometry("320x300+250+25")
        self.interfazAV.title("Calculando Anualidad Vencida")
        self.timer_id = None
        self.datosBlancos = None
        self.MenuAnualidadVencida()

    def MenuAnualidadVencida(self):
        self.datos_frame = ttk.Frame(self.interfazAV, borderwidth=5, relief="solid", width=300, height=300)
        self.datos_frame.grid(column=0, row=0, rowspan=7, pady=10, padx=10, sticky=(N, E, S, W))
        self.datos_frame.grid_propagate(False)

        self.tituloLb = ttk.Label(self.datos_frame, text="CALCULO DE ANUALIDAD VENCIDA", font=("Helvetica", 12, "bold"))
        self.tituloLb.grid(column=0, row=0, columnspan=2, padx=5, pady=10, sticky=(N, S, W))

        # Lectura Monto de Pago
        self.montoPagoTxt = StringVar()
        self.montoPagoLb = ttk.Label(self.datos_frame, text="Monto de Pago (A):")
        self.montoPagoLb.grid(column=0, row=1, padx=5, pady=5, sticky=W)
        self.montoPago_leer = ttk.Entry(self.datos_frame, textvariable=self.montoPagoTxt)
        self.montoPago_leer.grid(column=1, row=1, padx=5, pady=5, sticky=(W, E))

        # Lectura Tasa de Interés
        self.tasaTxt = StringVar()
        self.tasaIntLb = ttk.Label(self.datos_frame, text="Tasa de Interés (i):")
        self.tasaIntLb.grid(column=0, row=2, padx=4, pady=4, sticky=W)
        self.tasaInput_frame = ttk.Frame(self.datos_frame, width=140, height=25)
        self.tasaInput_frame.grid(column=1, row=2, sticky=(N, E, S, W))
        self.tasaInput_frame.grid_propagate(False)
        self.tasaInt_leer = ttk.Entry(self.tasaInput_frame, textvariable=self.tasaTxt, width=9)
        self.tasaInt_leer.grid(column=0, row=0, padx=(5, 0), pady=5, sticky=(W, E))

        # Lectura Periodo
        self.periodoTxt = StringVar()
        self.periodoLb = ttk.Label(self.datos_frame, text="Periodo/Tiempo (n):")
        self.periodoLb.grid(column=0, row=3, padx=5, pady=5, sticky=W)
        self.periodo_leer = ttk.Entry(self.datos_frame, textvariable=self.periodoTxt)
        self.periodo_leer.grid(column=1, row=3, padx=5, pady=5, sticky=(W, E))

        # Botón Calcular Resultados
        self.resultadosBt = ttk.Button(self.datos_frame, text="Calcular", command=self.CalcularResultados)
        self.resultadosBt.grid(column=0, row=4, padx=5, pady=(30, 10), sticky=(S))

        # Botón Volver Menu Principal
        self.volverMenuBt = ttk.Button(self.datos_frame, text="Volver Menu", command=self.VolverMenu)
        self.volverMenuBt.grid(column=1, row=4, padx=5, pady=(30, 10), sticky=(S))

        # Evitar bugs cerrando la ventana
        self.interfazAV.protocol("WM_DELETE_WINDOW", self.Cerrado_manual)

    # Validar solo entrada numérica
    def Check_Entrada(self, newval):
        return re.match(r'^[0-9][.,]?[0-9]$', newval) is not None and newval.count('.') <= 1 and newval.count(',') <= 1 and len(newval) <= 12

    # Mostrar Resultados
    def MostrarResultados(self):
        # Frame para los resultados
        self.resultados_frame = ttk.Frame(self.interfazAV, borderwidth=5, relief="groove", width=210, height=300)
        self.resultados_frame.grid(column=1, row=0, rowspan=7, padx=(0, 10), pady=10, sticky=(N, E, S, W))
        self.resultados_frame.grid_propagate(False)

        # Título
        self.tituloResultadosLb = ttk.Label(self.resultados_frame, text="RESULTADOS:", font=("Helvetica", 10, "bold"))
        self.tituloResultadosLb.grid(column=0, row=0, padx=5, pady=5, sticky=(W, N))

        # Valor presente
        self.resulVP_Lb = ttk.Label(self.resultados_frame, text="Valor Presente:", font=("Helvetica", 9, "bold"))
        self.resulVP_Lb.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
        self.valorPText = StringVar()
        self.valorP_Lb = ttk.Label(self.resultados_frame, textvariable=self.valorPText)
        self.valorP_Lb.grid(column=0, row=2, padx=5, pady=(0, 5), sticky=(W, N))

        # Valor futuro
        self.resulVF_Lb = ttk.Label(self.resultados_frame, text="Valor Futuro:", font=("Helvetica", 9, "bold"))
        self.resulVF_Lb.grid(column=0, row=3, padx=5, pady=5, sticky=(W))
        self.valorFText = StringVar()
        self.valorF_Lb = ttk.Label(self.resultados_frame, textvariable=self.valorFText)
        self.valorF_Lb.grid(column=0, row=4, padx=5, sticky=(W, N))

        # Gráfico de pie
        self.grafico_frame = ttk.Frame(self.resultados_frame)
        self.grafico_frame.grid(column=0, row=5, rowspan=2, pady=10, sticky=(N, E, S, W))

    # Llamado a las Operaciones
    def CalcularResultados(self):
        # Limpiar gráficos anteriores
        plt.close('all')

        # Validar entradas vacías
        if ((self.montoPagoTxt.get() == "" or self.montoPagoTxt == None) or
            (self.tasaTxt.get() == "" or self.tasaTxt == None) or
            (self.tasaTxtComboBox.get() == "--" or self.tasaTxtComboBox == None) or
            (self.periodoTxt.get() == "" or self.periodoTxt == None)):

            # Mostrar mensaje de error
            if self.datosBlancos is not None:
                self.datosBlancos.destroy()

            self.datosBlancos = ttk.Label(self.datos_frame, text="Por favor, rellena todos los espacios", font=("Helvetica", 9, "bold"), foreground="red")
            self.datosBlancos.grid(column=0, row=5, columnspan=2, sticky=(S, W))
            self.timer_id = self.datos_frame.after(5000, self.datosBlancos.destroy)
            return

        # Mostrar resultados
        self.interfazAV.geometry("540x700+250+25")
        self.MostrarResultados()

        # Calcular valor presente y futuro
        valorPresente = self.CalcularValorPresente()
        valorFuturo = self.CalcularValorFuturo(valorPresente)
        self.valorPText.set(valorPresente)
        self.valorFText.set(valorFuturo)

        # Mostrar gráficos
        self.MostrarGrafico(self.montoPagoTxt.get(), valorPresente)

    def MostrarGrafico(self, montoPago, valorPresente):
        # Limpiar el área del gráfico
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        # Datos para el gráfico
        etiquetas = ['Pago Anual (A)', 'Valor Presente (PV)']
        valores = [float(OperacionesMF.Convertir_ComaPunto(montoPago)), float(valorPresente)]

        # Crear gráfico de pie
        fig, ax = plt.subplots(figsize=(2, 1.5))
        ax.set_title("Pago Anual vs Valor Presente").set_fontsize(7)
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        # Mostrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.get_tk_widget().grid(row=0, column=0, pady=10)
        canvas.draw()

    # Calcular valor presente (fórmula estándar para anualidad vencida)
    def CalcularValorPresente(self):
        A = float(self.montoPagoTxt.get())
        tasa = float(self.tasaTxt.get())
        n = int(self.periodoTxt.get())
        valorPresente = A * ((1 - (1 + tasa)**-n) / tasa)
        return round(valorPresente, 2)

    # Calcular valor futuro (fórmula estándar para anualidad vencida)
    def CalcularValorFuturo(self, valorPresente):
        tasa = float(self.tasaTxt.get())
        n = int(self.periodoTxt.get())
        valorFuturo = valorPresente * (1 + tasa)**n
        return round(valorFuturo, 2)

    # Volver al menú anterior
    def VolverMenu(self):
        self.interfazAV.destroy()

    # Cerrar manualmente
    def Cerrado_manual(self):
        self.interfazAV.destroy()
