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

        # Gráfico
        self.grafico_frame = ttk.Frame(self.interfazAV)
        self.grafico_frame.grid(column=0, row=7, rowspan=2, padx=10,pady=10, sticky=(N, E, S, W))

    def CalcularResultados(self):
        # Validar entradas vacías
        if ((self.montoPagoTxt.get() == "" or self.montoPagoTxt == None) or
            (self.tasaTxt.get() == "" or self.tasaTxt == None) or
            (self.periodoTxt.get() == "" or self.periodoTxt == None)):

            if self.datosBlancos is not None:
                self.datosBlancos.destroy()

            self.datosBlancos = ttk.Label(self.datos_frame, text="Por favor, rellena todos los espacios", font=("Helvetica", 9, "bold"), foreground="red")
            self.datosBlancos.grid(column=0, row=5, columnspan=2, sticky=(S, W))
            self.timer_id = self.datos_frame.after(5000, self.datosBlancos.destroy)
            return

        # Mostrar resultados
        self.interfazAV.geometry("650x800+250+25")
        self.MostrarResultados()

        # Calcular valor presente y futuro
        valorPresente = self.CalcularValorPresente()
        valorFuturo = self.CalcularValorFuturo(valorPresente)
        self.valorPText.set(valorPresente)
        self.valorFText.set(valorFuturo)

        # Mostrar gráficos
        self.MostrarGrafico(self.montoPagoTxt.get(), valorPresente)

    def MostrarGrafico(self, montoPago, valorPresente):
        # Limpiar el área del gráfico antes de generar uno nuevo
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        # Convertir valores de entrada y calcular los datos necesarios
        montoPago = float(OperacionesMF.Convertir_ComaPunto(montoPago))
        valorPresente = float(valorPresente)
        tasa = float(self.tasaTxt.get())
        n = int(self.periodoTxt.get())

        # Generar los datos para los periodos y el valor presente acumulado
        periodos = list(range(1, n + 1))
        valores_presente = [montoPago * ((1 - (1 + tasa) ** -t) / tasa) for t in periodos]

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=100)  # Ajustar tamaño y resolución
        ax.plot(periodos, valores_presente, marker='o', linestyle='-', label="Valor Presente Acumulado")
        ax.set_title("Anualidad Vencida: Valor Presente por Periodo", fontsize=12)
        ax.set_xlabel("Periodo", fontsize=10)
        ax.set_ylabel("Valor Presente ($)", fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.6)

        # Ajustar los límites del eje para mejorar la visualización
        ax.set_xlim(1, n)
        ax.set_ylim(0, max(valores_presente) * 1.1)

        # Mostrar el gráfico dentro del frame de la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky=(N, S, E, W))

        # Asegurar que el frame de gráficos se expanda correctamente
        self.grafico_frame.columnconfigure(0, weight=1)
        self.grafico_frame.rowconfigure(0, weight=1)

        # Dibujar el gráfico
        canvas.draw()

    def CalcularValorPresente(self):
        A = float(self.montoPagoTxt.get())
        tasa = float(self.tasaTxt.get())
        n = int(self.periodoTxt.get())
        valorPresente = A * ((1 - (1 + tasa)**-n) / tasa)
        return round(valorPresente, 2)

    def CalcularValorFuturo(self, valorPresente):
        tasa = float(self.tasaTxt.get())
        n = int(self.periodoTxt.get())
        valorFuturo = valorPresente * (1 + tasa)**n
        return round(valorFuturo, 2)

    def VolverMenu(self):
        if self.interfazAV.winfo_exists():
            #Eliminamos la segunda ventana
            self.interfazAV.destroy();
            #ELiminamos grafico
            plt.close('all');
            #Llamamos de nuevo a la interfaz principal
            self.root.deiconify();

    def Cerrado_manual(self):
        if self.timer_id is not None:
            self.interfazAV.after_cancel(self.timer_id);
        self.interfazAV.destroy();
        self.root.destroy();
        #ELiminamos grafico
        plt.close('all');
        print("El programa se ha cerrado correctamente.");