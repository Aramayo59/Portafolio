# ventana_modificar_prestamo.py
import tkinter as tk

class VentanaModificarPrestamo:
    def __init__(self, root):
        self.ventana = tk.Toplevel(root)
        self.ventana.title("Modificar Préstamo")
        self.ventana.geometry("1260x600")
        self.ventana.configure(bg="#ff9933")

        # Etiqueta y selección de fecha de préstamo
        etiqueta_fecha_prestamo = tk.Label(self.ventana, text="Fecha Préstamo", bg="#ff9933", fg="#4d2600", font=("Arial", 10, "bold"))
        etiqueta_fecha_prestamo.pack(pady=5)
        entrada_fecha_prestamo = tk.Entry(self.ventana, width=20)
        entrada_fecha_prestamo.pack()

        # Etiqueta y selección de fecha de devolución
        etiqueta_fecha_devolucion = tk.Label(self.ventana, text="Fecha Devolución", bg="#ff9933", fg="#4d2600", font=("Arial", 10, "bold"))
        etiqueta_fecha_devolucion.pack(pady=5)
        entrada_fecha_devolucion = tk.Entry(self.ventana, width=20)
        entrada_fecha_devolucion.pack()

        # Botones de Modificar y Cancelar
        boton_modificar = tk.Button(self.ventana, text="Modificar", bg="#4d2600", fg="white", width=10)
        boton_modificar.pack(pady=10)
        boton_cancelar = tk.Button(self.ventana, text="Cancelar", bg="#4d2600", fg="white", width=10)
        boton_cancelar.pack(pady=5)
