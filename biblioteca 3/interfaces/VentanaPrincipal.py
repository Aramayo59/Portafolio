import tkinter as tk
from tkinter import ttk
from ventana_nuevo_prestamo import VentanaNuevoPrestamo
from ventana_modificar_prestamo import VentanaModificarPrestamo
from ConexionBD import ConexionBD  # Asegúrate de importar la clase de conexión correctamente

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión De Préstamos")
        self.root.geometry("1266x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#ff9933")  # Fondo naranja

        # Inicializar la conexión con la base de datos
        self.conexion = ConexionBD()
        if not self.conexion.conexionBaseDatos():
            print("Error al conectar a la base de datos")
            return  # Sale de la función si no se conecta

        # Marco para la tabla de préstamos
        self.marco_tabla = tk.Frame(self.root, bg="#4d2600")  # Fondo marrón oscuro
        self.marco_tabla.pack(pady=10, padx=10, fill="both", expand=True)

        # Tabla de préstamos registrados con columna ID
        self.columnas = ("ID", "Nombre", "Apellido", "DNI", "ISBN", "Fecha de devolución", "Estado")
        self.tabla = ttk.Treeview(self.marco_tabla, columns=self.columnas, show="headings", height=5)

        # Definir encabezados
        for col in self.columnas:
            self.tabla.heading(col, text=col)

        self.tabla.pack(fill="both", expand=True)

        # Cargar los datos en la tabla
        self.cargar_datos()

        # Marco para los botones
        self.marco_botones = tk.Frame(self.root, bg="#4d2600")  # Fondo marrón oscuro
        self.marco_botones.pack(pady=10)

        # Botones con color marrón oscuro
        boton_modificar = tk.Button(self.marco_botones, text="Modificar Préstamo", bg="#4d2600", fg="white", width=15, command=self.abrir_modificar_prestamo)
        boton_nuevo = tk.Button(self.marco_botones, text="Nuevo Préstamo", bg="#4d2600", fg="white", width=15, command=self.abrir_nuevo_prestamo)
        boton_eliminar = tk.Button(self.marco_botones, text="Eliminar Préstamo", bg="#4d2600", fg="white", width=15)

        boton_modificar.grid(row=0, column=0, padx=5)
        boton_nuevo.grid(row=0, column=1, padx=5)
        boton_eliminar.grid(row=0, column=2, padx=5)

        # Hover effects for buttons
        for button in [boton_modificar, boton_nuevo, boton_eliminar]:
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#3513ff"))  # Azul vibrante al pasar el ratón
            button.bind("<Leave>", lambda e, b=button: b.config(bg="#4d2600"))  # Vuelve a marrón oscuro

    def cargar_datos(self):
        # Consulta para obtener los préstamos
        query = "SELECT id, nombre, apellido, dni, isbn, fecha_devolucion, estado FROM prestamos"
        
        # Ejecutar la consulta usando la conexión y obtener los datos
        prestamos = self.conexion.ejecutar_consulta(query)
        
        if prestamos:  # Verifica si la lista no está vacía
            print(f"Datos cargados: {prestamos}")  # Depuración para ver los datos
            for prestamo in prestamos:
                self.tabla.insert("", "end", values=prestamo)
        else:
            print("No se pudieron cargar los datos")

    def abrir_nuevo_prestamo(self):
        VentanaNuevoPrestamo(self.root)

    def abrir_modificar_prestamo(self):
        VentanaModificarPrestamo(self.root)

    def __del__(self):
        # Cerrar la conexión al cerrar la ventana principal
        self.conexion.cerrar()

# Ejecutar la aplicación principal
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()
