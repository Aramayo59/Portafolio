import tkinter as tk
from tkinter import ttk, messagebox

class BookForm:
    def __init__(self, root, color_naranja, color_marron, color_rojo, callback_agregar, callback_eliminar, callback_volver):
        # Frame con fondo naranja y centrado en la parte inferior
        frame = tk.Frame(root, bg=color_naranja)
        frame.pack(pady=20, padx=20, fill="both", expand=True)  # Centrar el frame

        # Configuración del grid para que los elementos se centren
        frame.grid_rowconfigure(0, weight=1)  # Dejar la primera fila vacía para empujar hacia abajo
        frame.grid_rowconfigure(1, weight=2)  # Agregar peso para que el frame se estire
        frame.grid_rowconfigure(7, weight=1)  # Configuración de peso para la última fila
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        labels = ["Título:", "Autor:", "Editorial:", "ISBN:", "Categoría:", "Subcategoría:", "Descripción:"]
        self.entries = {}
        for i, label in enumerate(labels):
            # Etiquetas centradas
            tk.Label(frame, text=label, bg=color_naranja, fg="black").grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            if i == 6:  # Descripción (usar Text)
                self.entries[label] = tk.Text(frame, height=4, width=30, bg="white", fg="black")
                self.entries[label].grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
            else:
                entry = tk.Entry(frame, bg="white", fg="black") if i != 4 and i != 5 else ttk.Combobox(frame)
                entry.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
                self.entries[label] = entry

        self.entries["Categoría:"].bind("<<ComboboxSelected>>", callback_agregar)

        # Botones centrados
        tk.Button(frame, text="Agregar Libro", bg=color_marron, fg="white", command=callback_agregar).grid(row=8, column=0, padx=10, pady=10, sticky="nsew")
        tk.Button(frame, text="Eliminar Libro", bg=color_marron, fg="white", command=callback_eliminar).grid(row=8, column=1, padx=10, pady=10, sticky="nsew")
        
        # Botón Volver en color rojo
        tk.Button(frame, text="Volver", bg=color_rojo, fg="white", command=callback_volver).grid(row=8, column=2, padx=10, pady=10, sticky="nsew")

    def obtener_valores(self):
        valores = {label: self.entries[label].get() if label != "Descripción:" else self.entries[label].get("1.0", tk.END).strip() for label in self.entries}
        return valores

    def limpiar_campos(self):
        for label, widget in self.entries.items():
            if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
