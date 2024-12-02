from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
#from TIR import calcular_tir  # Usamos la función calcular_tir desarrollada
class InterfazTIR:
    def __init__(self, root):
        self.root = root
        self.root.title("Cálculo de TIR")
        
        # Configuración de la ventana
        self.frame = Frame(self.root, padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)
        
        # Etiqueta y entrada para los flujos de caja
        Label(self.frame, text="Flujos de caja (separados por comas):").grid(row=0, column=0, sticky=W)
        self.entry_flujos = Entry(self.frame, width=40)
        self.entry_flujos.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón para calcular la TIR
        self.btn_calcular = Button(self.frame, text="Calcular TIR", command=self.calcular_tir)
        self.btn_calcular.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Resultado
        self.label_resultado = Label(self.frame, text="", fg="blue", font=("Arial", 12))
        self.label_resultado.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Área de gráficos
        self.figura, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=3, column=0, columnspan=2, pady=10)

    def calcular_tir(self):
        flujos_texto = self.entry_flujos.get()
        # Validar la entrada de los flujos de caja
        try:
            flujos = list(map(float, re.split(r'\s*,\s*', flujos_texto)))
            #tir = calcular_tir(flujos)
            #self.label_resultado.config(text=f"La TIR es: {tir:.2%}")
            
            # Crear un gráfico del flujo de caja
            self.ax.clear()
            self.ax.bar(range(len(flujos)), flujos, color="skyblue", label="Flujos de caja")
            self.ax.axhline(0, color="red", linestyle="--")
            self.ax.legend()
            self.ax.set_title("Flujos de Caja")
            self.ax.set_xlabel("Períodos")
            self.ax.set_ylabel("Valor")
            self.canvas.draw()
        except ValueError as e:
            self.label_resultado.config(text=f"Error: {e}")
        except Exception as e:
            self.label_resultado.config(text="Error al procesar los flujos de caja.")