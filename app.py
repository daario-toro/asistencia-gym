import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

# --- 🚨 PRUEBA DE FUEGO: Si ves esto en la terminal, el archivo es el nuevo 🚨 ---
print("🚨 🚨 🚨 ESTE ES EL CÓDIGO NUEVO Y ACTUALIZADO 🚨 🚨 🚨")
# -------------------------------------------------------------------------------

load_dotenv()
# ... (el resto de tu código sigue igual) ...

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1", "http://localhost"]}})

# 2. Configuración SEGURA de la Base de Datos
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'), # Sin valor por defecto. Obligatorio tener el .env
    'database': os.getenv('DB_NAME', 'asistencia_db')
}
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 3. FUNCIÓN AUXILIAR: SEPARA Y LIMPIA EL RUT
def procesar_rut(rut_completo):
    if not rut_completo:
        return None, None
    rut_limpio = rut_completo.replace('.', '').replace(' ', '').replace('-', '').upper()
    if len(rut_limpio) < 2:
        return None, None
    dv = rut_limpio[-1]
    rut_base = rut_limpio[:-1]
    return rut_base, dv

# --- RUTA 1: BUSCAR RUT ---
@app.route('/api/buscar_rut', methods=['GET'])
def buscar_rut():
    rut_completo = request.args.get('rut_completo') or request.args.get('rut')
    rut_base, dv = procesar_rut(rut_completo)
    
    if not rut_base:
        return jsonify({"error": "Formato de RUT inválido"}), 400

    try:
        conn = get_db_connection()
        # buffered=True EVITA CUALQUIER error de "Unread result"
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM participantes WHERE rut = %s", (rut_base,))
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({"existe": usuario is not None, "datos": usuario}), 200
    except Exception as e:
        print(f"Error en buscar_rut: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

# --- RUTA 2: REGISTRAR ASISTENCIA ---
@app.route('/api/registrar', methods=['POST'])
def registrar_asistencia():
    datos = request.json
    
    rut_completo = datos.get('rut_completo') or datos.get('rut')
    rut_base, dv = procesar_rut(rut_completo)
    
    if not rut_base:
        return jsonify({"error": "El RUT ingresado no es válido"}), 400

    try:
        conn = get_db_connection()
        # buffered=True ES LA CLAVE: descarga todo el resultado inmediatamente
        cursor = conn.cursor(buffered=True)
        
        # 1. Verificar si el participante ya existe
        cursor.execute("SELECT rut FROM participantes WHERE rut = %s", (rut_base,))
        usuario_existente = cursor.fetchone()
        
        if not usuario_existente:
            nombre_participante = datos.get('nombres') or datos.get('nombre')
            sql_user = """
                INSERT INTO participantes (rut, dv, nombres, apellido_paterno, apellido_materno, 
                                           fecha_nacimiento, tipo_usuario, cesfam, telefono, direccion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_user, (
                rut_base, dv, nombre_participante, datos.get('apellidoPaterno'), 
                datos.get('apellidoMaterno'), datos.get('fechaNacimiento'), datos.get('tipoUsuario'), 
                datos.get('cesfam'), datos.get('telefono'), datos.get('direccion')
            ))
        
        # 2. BUSCAR IDs (USANDO LOS NOMBRES REALES DE TU BD: nombre_clase y nombre_completo)
        cursor.execute("SELECT id_clase FROM clases WHERE nombre_clase = %s", (datos.get('clase'),))
        res_c = cursor.fetchone()
        
        cursor.execute("SELECT id_profesor FROM profesores WHERE nombre_completo = %s", (datos.get('profesor'),))
        res_p = cursor.fetchone()

        if not res_c or not res_p:
            return jsonify({"error": "La clase o el profesor seleccionados no son válidos en la base de datos."}), 400
        
        id_clase = res_c[0]
        id_profesor = res_p[0]
        
        # 3. Registrar la asistencia
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        hora_actual = datetime.now().strftime('%H:%M:%S')
        
        sql_asist = """
            INSERT INTO asistencias (rut, dv, id_clase, id_profesor, fecha, hora) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_asist, (rut_base, dv, id_clase, id_profesor, fecha_actual, hora_actual))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "¡Asistencia registrada con éxito!"}), 200

    except Exception as e:
        print(f"Error técnico detallado: {e}") # Esto lo ves TÚ en la terminal del servidor
        return jsonify({"error": "Ocurrió un error interno al procesar la solicitud."}), 500 # Esto ve el USUARIO en el navegador

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)