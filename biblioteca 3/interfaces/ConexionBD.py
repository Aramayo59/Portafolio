import mysql.connector
from mysql.connector import Error

class ConexionBD:
    def __init__(self):
        self.connection = None

    def conexionBaseDatos(self):
        try:
            # Establecer la conexión con la base de datos
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
                return cursor.fetchall()  # Retorna los resultados de la consulta SELECT
            self.connection.commit()  # Aplica cambios si es una consulta de modificación
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            cursor.close()

    def ejecutar_cambio(self, consulta, parametros):
        cursor = self.connection.cursor()
        try:
            cursor.execute(consulta, parametros)
            self.connection.commit()  # Aplica los cambios
        except Error as e:
            print(f"Error al ejecutar el cambio: {e}")
        finally:
            cursor.close()

    def cerrar(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")
