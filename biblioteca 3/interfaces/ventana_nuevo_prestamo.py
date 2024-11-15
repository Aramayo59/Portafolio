import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
from mysql.connector import Error
import datetime

class ConexionBD:
    def __init__(self):
        self.connection = None

    def conexionBaseDatos(self):
        try:
            self.connection = mysql.connector.connect(
                user='root',
                password='',
                host='127.0.0.1',
                database='bibliodb',
                port='3306'
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos.")
                return True
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False

    def ejecutar_consulta(self, consulta, parametros=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(consulta, parametros)
            if consulta.lower().startswith("select"):
                return cursor.fetchall()
            self.connection.commit()
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            cursor.close()

    def cerrar(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")

class VentanaNuevoPrestamo:
    def __init__(self, root):
        self.ventana = tk.Toplevel(root)
        self.ventana.title("Nuevo Préstamo")
        self.ventana.geometry("1266x600")
        self.ventana.configure(bg="#ff9933")

        # Crear instancia de la clase ConexionBD
        self.conexion = ConexionBD()

        # Etiquetas y entradas
        self.etiquetas = ["DNI", "Nombre completo", "ISBN del libro", "Fecha Préstamo", "Fecha Devolución"]
        self.entradas = {}
        for i, texto in enumerate(self.etiquetas[:-1]):  # Excluir la fecha de devolución
            etiqueta = tk.Label(self.ventana, text=texto, bg="#ff9933", fg="#4d2600", font=("Arial", 10, "bold"))
            etiqueta.pack(pady=5)
            entrada = tk.Entry(self.ventana, width=30)
            entrada.pack()
            self.entradas[texto] = entrada  # Guardar las referencias a las entradas

        # Obtener la fecha actual y asignarla a la entrada de la fecha de préstamo
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        self.entradas["Fecha Préstamo"].insert(0, fecha_actual)  # Insertar fecha en el campo
        self.entradas["Fecha Préstamo"].config(state="readonly")

        # Crear el campo de entrada para la "Fecha Devolución"
        self.entrada_fecha_devolucion = tk.Entry(self.ventana, width=30)
        self.entrada_fecha_devolucion.pack(pady=5)

        # Crear el calendario (inicialmente oculto)
        self.calendario = Calendar(self.ventana, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendario.place(x=-1000, y=-1000)  # Colocarlo fuera de la vista

        # Configurar evento para mostrar el calendario cuando el campo de "Fecha Devolución" sea clickeado
        self.entrada_fecha_devolucion.bind("<Button-1>", self.mostrar_calendario)

        # Botones de buscar y aceptar
        boton_buscar_socio = tk.Button(self.ventana, text="Buscar Socio", width=15, bg="#4d2600", fg="white", command=self.buscar_socio)
        boton_buscar_socio.pack(pady=5)
        
        boton_buscar_libro = tk.Button(self.ventana, text="Buscar Libro", width=15, bg="#4d2600", fg="white", command=self.buscar_libro)
        boton_buscar_libro.pack(pady=5)

        # Botón para registrar préstamo
        boton_registrar_prestamo = tk.Button(self.ventana, text="Registrar Préstamo", width=15, bg="#4d2600", fg="white", command=self.realizar_prestamo)
        boton_registrar_prestamo.pack(pady=5)

    def mostrar_calendario(self, event):
        """Mostrar el calendario cuando se haga clic en el campo de fecha de devolución."""
        # Mostrar el calendario justo debajo del campo de entrada
        x = self.entrada_fecha_devolucion.winfo_rootx()
        y = self.entrada_fecha_devolucion.winfo_rooty() + self.entrada_fecha_devolucion.winfo_height()

        self.calendario.place(x=x, y=y)  # Colocar el calendario en la posición deseada

        # Configurar el evento para que al seleccionar una fecha se cierre el calendario y se muestre en la entrada
        self.calendario.bind("<<CalendarSelected>>", self.seleccionar_fecha)

    def seleccionar_fecha(self, event):
        """Actualizar la entrada de la fecha con la fecha seleccionada en el calendario."""
        fecha_seleccionada = self.calendario.get_date()
        self.entrada_fecha_devolucion.delete(0, tk.END)
        self.entrada_fecha_devolucion.insert(0, fecha_seleccionada)
        self.calendario.place(x=-1000, y=-1000)  # Ocultar el calendario

    def buscar_socio(self):
        """Buscar socio por DNI"""
        dni = self.entradas["DNI"].get()
        if not dni:
            messagebox.showwarning("Advertencia", "Por favor ingrese un DNI.")
            return

        # Conectar a la base de datos
        if self.conexion.conexionBaseDatos():
            consulta = "SELECT nombre, apellido FROM socios WHERE dni = %s"
            resultado = self.conexion.ejecutar_consulta(consulta, (dni,))
            if resultado:
                nombre, apellido = resultado[0]
                messagebox.showinfo("Socio encontrado", f"Socio: {nombre} {apellido}")
            else:
                messagebox.showwarning("No encontrado", "No se encontró un socio con ese DNI.")
            self.conexion.cerrar()

    def buscar_libro(self):
        """Buscar libro por ISBN"""
        isbn = self.entradas["ISBN del libro"].get()
        if not isbn:
            messagebox.showwarning("Advertencia", "Por favor ingrese un ISBN.")
            return

        # Conectar a la base de datos
        if self.conexion.conexionBaseDatos():
            consulta = "SELECT titulo FROM libros WHERE isbn = %s"
            resultado = self.conexion.ejecutar_consulta(consulta, (isbn,))
            if resultado:
                titulo = resultado[0][0]
                messagebox.showinfo("Libro encontrado", f"Libro: {titulo}")
            else:
                messagebox.showwarning("No encontrado", "No se encontró un libro con ese ISBN.")
            self.conexion.cerrar()

    def realizar_prestamo(self):
        """Registrar un nuevo préstamo en la base de datos."""
        dni = self.entradas["DNI"].get()
        isbn = self.entradas["ISBN del libro"].get()
        fecha_prestamo = self.entradas["Fecha Préstamo"].get()
        fecha_devolucion = self.entrada_fecha_devolucion.get()

        if not dni or not isbn or not fecha_devolucion:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Validar que la fecha de devolución sea posterior a la fecha de préstamo
        if fecha_devolucion <= fecha_prestamo:
            messagebox.showwarning("Advertencia", "La fecha de devolución debe ser posterior a la fecha de préstamo.")
            return

        # Conectar a la base de datos
        if self.conexion.conexionBaseDatos():
            consulta = """INSERT INTO prestamos (dni_socio, isbn_libro, fecha_prestamo, fecha_devolucion) 
                          VALUES (%s, %s, %s, %s)"""
            parametros = (dni, isbn, fecha_prestamo, fecha_devolucion)
            resultado = self.conexion.ejecutar_consulta(consulta, parametros)
            if resultado is not None:
                messagebox.showinfo("Éxito", "El préstamo ha sido registrado exitosamente.")
            self.conexion.cerrar()

# Código para ejecutar la ventana
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal (no se necesita)
    app = VentanaNuevoPrestamo(root)
    root.mainloop()
