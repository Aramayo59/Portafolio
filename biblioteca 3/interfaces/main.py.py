import tkinter as tk
from login import Login
from dashboard import Dashboard

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar la ventana principal inicialmente
        self.show_login()  # Mostrar el formulario de login primero

    def show_login(self):
        # Crear una instancia de la ventana de login
        self.login_window = Login(self.root, self.on_login_success)
        self.login_window.show()  # Mostrar la ventana de login

    def on_login_success(self):
        # Si el login es exitoso, ocultar la ventana de login y abrir el dashboard
        self.login_window.window.destroy()  # Cerrar la ventana de login
        self.show_dashboard()  # Mostrar el dashboard

    def show_dashboard(self):
        # Crear y mostrar la ventana del dashboard
        self.dashboard_window = Dashboard(self.root)

    def run(self):
        # Ejecutar el loop de la aplicación
        self.root.mainloop()

if __name__ == '__main__':
    app = MainApp()
    app.run()