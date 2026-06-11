import mysql.connector

# Datos de tu base de datos
configuracion = {
    'host': 'localhost',
    'user': 'root',
    'password': 'a1b2c3d4e5',
    'database': 'asistencia_db'
}

def probar_conexion():
    try:
        # Intentamos la conexión
        conexion = mysql.connector.connect(**configuracion)
        
        if conexion.is_connected():
            print("¡Éxito! Conexión establecida con la base de datos.")
            # Obtenemos información de la conexión
            cursor = conexion.cursor()
            cursor.execute("SELECT DATABASE();")
            registro = cursor.fetchone()
            print("Estás conectado a la base de datos:", registro[0])
            
            # Siempre cerramos la conexión al terminar
            cursor.close()
            conexion.close()
            
    except mysql.connector.Error as error:
        print(f"Ups, ocurrió un error: {error}")

if __name__ == "__main__":
    probar_conexion()