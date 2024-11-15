from ConexionBD import ConexionBD  # Importa la clase ConexionBD

class Socio:

    @staticmethod
    def mostrar_socios():
        try:
            # Establece la conexión a la base de datos
            db = ConexionBD()
            if not db.conexionBaseDatos():  # Verifica si la conexión fue exitosa
                return []

            # Ejecuta la consulta
            query = "SELECT * FROM socios;"
            miresultado = db.ejecutar_consulta(query)
            db.cerrar()  # Cierra la conexión

            return miresultado

        except mysql.connector.Error as error:
            print(f"Error al mostrar datos: {error}")
            return []

    @staticmethod
    def Ingresar_Socios(Apellido, Nombre, DNI, Domicilio, FechadePago, Teléfono, Sexo):
        try:
            # Establece la conexión a la base de datos
            db = ConexionBD()
            if not db.conexionBaseDatos():  # Verifica si la conexión fue exitosa
                return

            # Inserta los datos del nuevo socio
            sql = "INSERT INTO socios (Apellido, Nombre, DNI, Domicilio, FechadePago, Teléfono, Sexo) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            valores = (Apellido, Nombre, DNI, Domicilio, FechadePago, Teléfono, Sexo)
            db.ejecutar_cambio(sql, valores)  # Ejecuta el cambio (INSERT)
            db.cerrar()  # Cierra la conexión
            print("Registro ingresado correctamente.")

        except mysql.connector.Error as error:
            print(f"Error al ingresar datos: {error}")

    @staticmethod
    def Modificar_Socios(ID, Apellido, Nombre, DNI, Domicilio, FechadePago, Teléfono, Sexo):
        try:
            # Establece la conexión a la base de datos
            db = ConexionBD()
            if not db.conexionBaseDatos():  # Verifica si la conexión fue exitosa
                return

            # Modifica los datos del socio
            sql = """UPDATE socios SET 
                     Apellido = %s, 
                     Nombre = %s, 
                     DNI = %s, 
                     Domicilio = %s, 
                     FechadePago = %s, 
                     Teléfono = %s, 
                     Sexo = %s 
                     WHERE ID = %s;"""
            valores = (Apellido, Nombre, DNI, Domicilio, FechadePago, Teléfono, Sexo, ID)
            db.ejecutar_cambio(sql, valores)  # Ejecuta el cambio (UPDATE)
            db.cerrar()  # Cierra la conexión
            print("Registro actualizado correctamente.")

        except mysql.connector.Error as error:
            print(f"Error al modificar datos: {error}")
