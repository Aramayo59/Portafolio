import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class DatabaseConnector:
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def conectar(self):
        if self.conexion and self.conexion.is_connected():
            return True
        try:
            self.conexion = mysql.connector.connect(
                user='root',
                password='',
                host='127.0.0.1',
                database='bibliodb',
                port='3306'
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
            return False
        return True

    def ejecutar_consulta(self, consulta, parametros=()):
        try:
            self.cursor.execute(consulta, parametros)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Error en la consulta", f"Se produjo un error al ejecutar la consulta: {err}")
            return []

    def ejecutar_cambio(self, consulta, parametros=()):
        try:
            self.cursor.execute(consulta, parametros)
            self.conexion.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Error en la consulta", f"Se produjo un error al ejecutar el cambio: {err}")

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()

class AltaLibros:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Biblioteca")
        self.root.geometry("1266x768")
        self.root.resizable(False, False)
        self.color_naranja = "#ff9933"
        self.color_marron = "#4d2600"
        self.root.configure(bg=self.color_marron)

        self.db = DatabaseConnector()
        if not self.db.conectar():
            self.root.destroy()
            return

        # Crear las secciones
        self.crear_tabla_libros()
        self.crear_formulario_libros()

        self.cargar_libros()

    def crear_tabla_libros(self):
        # Frame para la tabla de libros
        frame_tabla = tk.Frame(self.root, bg=self.color_marron)
        frame_tabla.pack(fill=tk.X, padx=10, pady=10)

        # Crear el Treeview para la tabla
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("ID", "ISBN", "Título", "Categoría", "Subcategoría", "Autor", "Editorial", "Descripción"),
            show="headings",
            height=8
        )
        
        # Configurar las cabeceras de la tabla
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white")  # Fondo blanco para las filas
        style.configure("Treeview.Heading", background=self.color_marron, foreground="white", font=("Verdana", 10, "bold"))  # Encabezados marrones
        style.map("Treeview", background=[('selected', self.color_naranja)], foreground=[('selected', 'black')])

        self.tabla.pack(fill=tk.X)

    def crear_formulario_libros(self):
        # Frame para el formulario
        frame_formulario = tk.Frame(self.root, bg=self.color_naranja)
        frame_formulario.pack(fill=tk.BOTH, padx=20, pady=20)

        # Configurar el grid para centrar los elementos
        frame_formulario.grid_rowconfigure(0, weight=1)
        frame_formulario.grid_rowconfigure(1, weight=1)
        frame_formulario.grid_rowconfigure(2, weight=1)
        frame_formulario.grid_rowconfigure(3, weight=1)
        frame_formulario.grid_rowconfigure(4, weight=1)
        frame_formulario.grid_rowconfigure(5, weight=1)
        frame_formulario.grid_rowconfigure(6, weight=1)
        frame_formulario.grid_rowconfigure(7, weight=2)  # Para los botones
        frame_formulario.grid_columnconfigure(0, weight=1)
        frame_formulario.grid_columnconfigure(1, weight=2)

        labels = ["Título:", "Autor:", "Editorial:", "ISBN:", "Categoría:", "Subcategoría:", "Descripción:"]
        self.entries = {}

        # Crear etiquetas y campos de entrada
        for i, label in enumerate(labels):
            tk.Label(frame_formulario, text=label, bg=self.color_naranja, fg="white").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = tk.Entry(frame_formulario, width=50)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[label] = entry

        # Área de texto para la descripción
        self.entries["Descripción:"].grid_forget()  # Eliminar el Entry estándar de descripción
        self.entries["Descripción:"] = tk.Text(frame_formulario, height=4, width=38)
        self.entries["Descripción:"].grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Ajustar las entradas a la posición más baja (dos filas hacia abajo)
        for i in range(6, 1, -1):  # Cambiar filas hacia abajo
            frame_formulario.grid_rowconfigure(i, weight=1)  # Ajustar filas

        # Botones
        button_frame = tk.Frame(frame_formulario, bg=self.color_naranja)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Agregar Libro", command=self.agregar_libro, bg=self.color_marron, fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Eliminar Libro", command=self.eliminar_libro, bg=self.color_marron, fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Volver", command=self.volver, bg=self.color_marron, fg="white", width=15).pack(side=tk.LEFT, padx=5)

    def cargar_libros(self):
        # Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Cargar datos de la base de datos
        datos = self.db.ejecutar_consulta("SELECT * FROM libros")
        for libro in datos:
            self.tabla.insert("", "end", values=libro)

    def agregar_libro(self):
        # Obtener los valores de los campos de entrada
        valores = [self.entries[label].get() if label != "Descripción:" else self.entries[label].get("1.0", tk.END).strip() for label in self.entries]
        
        # Verificar si todos los campos tienen valor
        if not all(valores):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos requeridos.")
            return
        
        # Comprobar si el libro ya existe verificando el ISBN
        isbn = valores[3]  # El ISBN está en la posición 3 de la lista de valores
        
        # Consultar si el ISBN ya está registrado
        existe_libro = self.db.ejecutar_consulta("SELECT COUNT(*) FROM libros WHERE ISBN = %s", (isbn,))
        
        if existe_libro[0][0] > 0:
            # Si el ISBN ya existe, mostrar un mensaje de advertencia
            messagebox.showwarning("Libro duplicado", "Este libro ya está registrado en la base de datos.")
            return
        
        try:
            # Obtener el nuevo ID del libro
            nuevo_id = self.db.ejecutar_consulta("SELECT IFNULL(MAX(libro_id), 0) + 1 FROM libros")[0][0]
            
            # Insertar el nuevo libro en la base de datos
            self.db.ejecutar_cambio(
                "INSERT INTO libros (libro_id, Titulo, ISBN, Categoria, Subcategoria, Autor, Editorial, Descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (nuevo_id, valores[0], valores[3], valores[4], valores[5], valores[1], valores[2], valores[6])
            )
            
            # Confirmar que el libro fue agregado correctamente
            messagebox.showinfo("Éxito", "Libro agregado correctamente.")
            
            # Recargar la lista de libros
            self.cargar_libros()
        
        except Exception as e:
            # Si hay un error al agregar el libro, mostrar un mensaje de error
            messagebox.showerror("Error al agregar libro", f"Hubo un error al agregar el libro: {e}")

    def eliminar_libro(self):
        # Obtener el ID del libro seleccionado
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección inválida", "Seleccione un libro para eliminar.")
            return

        libro_id = self.tabla.item(seleccion, "values")[0]

        try:
            # Eliminar el libro de la base de datos
            self.db.ejecutar_cambio("DELETE FROM libros WHERE libro_id = %s", (libro_id,))
            messagebox.showinfo("Éxito", "Libro eliminado correctamente.")
            
            # Recargar la lista de libros
            self.cargar_libros()

        except Exception as e:
            # Si hay un error al eliminar el libro, mostrar un mensaje de error
            messagebox.showerror("Error al eliminar libro", f"Hubo un error al eliminar el libro: {e}")

    def volver(self):
        self.root.quit()

def main():
    root = tk.Tk()
    app = AltaLibros(root)
    root.mainloop()

if __name__ == "__main__":
    main()
