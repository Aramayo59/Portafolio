import tkinter as tk
from tkinter import ttk

class BookTable:
    def __init__(self, root, columnas, estilo):
        self.tabla = ttk.Treeview(root, columns=columnas, show="headings", style=estilo)
        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Definir encabezados de columnas
        for columna in columnas:
            self.tabla.heading(columna, text=columna.title())  # El texto de los encabezados será el nombre de la columna

    def configurar_tabla(self, color_naranja, color_marron):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Color de fondo de la tabla y los encabezados
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")  # Fondo blanco para las filas
        style.configure("Treeview.Heading", background=color_marron, foreground="white", font=('Arial', 10, 'bold'))  # Encabezados marrones
        style.map('Treeview', background=[('selected', color_naranja)])  # Color de fondo cuando una fila está seleccionada

    def cargar_datos(self, datos):
        self.tabla.delete(*self.tabla.get_children())
        for fila in datos:
            self.tabla.insert("", "end", values=fila)

    def obtener_seleccion(self):
        selected_item = self.tabla.selection()
        if selected_item:
            return self.tabla.item(selected_item)['values'][0]
        return None

