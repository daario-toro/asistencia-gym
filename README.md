# Sistema de Control de Asistencia - Gimnasio Comunal

Sistema web de registro de asistencia para gimnasios municipales, desarrollado como migración desde Google Apps Script hacia una arquitectura Cliente-Servidor local con base de datos relacional.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3+-black?logo=flask)
![MariaDB](https://img.shields.io/badge/MariaDB-10.6+-003545?logo=mariadb)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0+-38bdf8?logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Objetivo del Proyecto

Desarrollar una solución robusta y escalable para el registro de asistencia de usuarios en un gimnasio comunal, permitiendo:
- Registro rápido de asistencia mediante RUT
- Gestión de participantes (nuevos y existentes)
- Visualización en tiempo real de asistentes por clase
- Dashboard para pantallas de TV con actualización automática

---

## Características Principales

### Registro de Asistencia (Frontend)
- **Búsqueda inteligente por RUT** con formateo automático (puntos y guion)
- **Detección automática** de usuarios nuevos vs existentes
- **Formulario dinámico** que se bloquea para usuarios registrados
- **Validación de datos** en tiempo real
- **Diseño responsive** optimizado para dispositivos móviles

###  Dashboard en Tiempo Real
- **Visualización para TV** (35" 1080p) con tema oscuro
- **Actualización automática** cada 30 segundos
- **Filtro por clase y profesor** con menús desplegables
- **Ventana de tiempo** de 50 minutos desde el primer registro
- **Contador en vivo** de participantes registrados
- **Reloj digital** con fecha actual

### 🔒 Seguridad
- **Variables de entorno** para credenciales de base de datos
- **CORS restringido** a localhost
- **Modo producción** con debug desactivado
- **Manejo seguro de errores** sin exposición de detalles técnicos
- **Git ignore** para archivos sensibles

### ⚡ Backend (API REST)
- **Endpoints RESTful** con Flask
- **Consultas SQL optimizadas** con MariaDB
- **Manejo de cursores** con buffered para evitar conflictos
- **Separación automática** de RUT y dígito verificador
- **Filtrado por fecha** para registros del día actual

---

## 🛠️ Stack Tecnológico

### Backend
- **Python 3.10+** - Lenguaje de programación
- **Flask 2.3+** - Framework web ligero
- **mysql-connector-python** - Conector de base de datos
- **python-dotenv** - Gestión de variables de entorno
- **Flask-CORS** - Manejo de Cross-Origin Resource Sharing

### Frontend
- **HTML5** - Estructura semántica
- **Tailwind CSS 3.0+** - Framework CSS utility-first
- **JavaScript (ES6+)** - Lógica del cliente
- **SweetAlert2** - Notificaciones y modales
- **Font Awesome 6.4** - Iconografía

### Base de Datos
- **MariaDB 10.6+** - Sistema de gestión de base de datos relacional
- **MySQL Workbench** - Herramienta de administración

### Control de Versiones
- **Git** - Sistema de control de versiones
- **GitHub** - Repositorio remoto

---

##  Estructura del Proyecto




---

## 🔧 Instalación y Configuración

### Requisitos Previos
- Python 3.10 o superior
- MariaDB 10.6 o superior
- Git

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/asistencia-gym.git
cd asistencia-gym

Paso 2: Configurar Entorno Virtual (Recomendado)

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Paso 3: Instalar Dependencias

pip install flask flask-cors mysql-connector-python python-dotenv

Paso 4: Configurar Base de Datos

Crear la base de datos en MariaDB:
    CREATE DATABASE asistencia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
Importar el esquema y datos:
    mysql -u root -p asistencia_db < respaldo_asistencia_total.sql

Paso 5: Configurar Variables de Entorno

Crear archivo .env en la raíz del proyecto:
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=asistencia_db

Paso 6: Ejecutar la Aplicación
   
    python app.py

Endpoints de la API
Buscar Usuario por RUT
    GET /api/buscar_rut?rut=12345678-9
        Respuesta:
        {
  "existe": true,
  "datos": {
    "rut": "12345678",
    "dv": "9",
    "nombres": "Juan",
    "apellido_paterno": "Pérez",
    "apellido_materno": "González",
    "fecha_nacimiento": "1990-01-01",
    "tipo_usuario": "ADULTO 19 A 59 AÑOS",
    "cesfam": "LVN",
    "telefono": "912345678",
    "direccion": "Av. Principal 123"
  }
}
Registrar Asistencia
    POST /api/registrar
Content-Type: application/json

{
  "rut_completo": "12345678-9",
  "nombres": "Juan",
  "apellidoPaterno": "Pérez",
  "apellidoMaterno": "González",
  "fechaNacimiento": "1990-01-01",
  "tipoUsuario": "ADULTO 19 A 59 AÑOS",
  "cesfam": "LVN",
  "telefono": "912345678",
  "direccion": "Av. Principal 123",
  "clase": "Full Core",
  "profesor": "Dario Toro"
}
    Respuesta:
    {
  "mensaje": "¡Asistencia registrada con éxito!"
}

Obtener Clases y Profesores:
    GET /api/obtener-clases-profesores
    Respuesta:
    {
  "clases": [
    {"id_clase": 1, "nombre_clase": "Full Core"},
    {"id_clase": 2, "nombre_clase": "Zumba"}
  ],
  "profesores": [
    {"id_profesor": 1, "nombre_completo": "Dario Toro"},
    {"id_profesor": 2, "nombre_completo": "Mario Bustamante"}
  ]
}

Estado de Asistencia en Tiempo Real
    Estado de Asistencia en Tiempo Real
    Respuesta: {
  "total": 5,
  "usuarios": [
    {
      "nombres": "Juan",
      "apellido_paterno": "Pérez",
      "apellido_materno": "González"
    },
    {
      "nombres": "María",
      "apellido_paterno": "López",
      "apellido_materno": "Sánchez"
    }
  ]
}

Seguridad
Medidas Implementadas
    Variables de Entorno: Credenciales de BD almacenadas en .env
    CORS Restringido: Solo permite peticiones desde localhost
    Modo Producción: Debug desactivado (debug=False)
    Host Local: Servidor vinculado a 127.0.0.1
    Manejo de Errores: Mensajes genéricos al cliente, logs detallados en servidor
    Git Ignore: Archivos sensibles excluidos del control de versiones

Archivos Sensibles
        .env
__pycache__/
*.pyc
venv/



Base de Datos
Tablas Principales
        participantes
    
    Almacena la información personal de los usuarios del gimnasio.

        rut (VARCHAR) - RUT sin dígito verificador (PK)
        dv (VARCHAR) - Dígito verificador
        nombres (VARCHAR)
        apellido_paterno (VARCHAR)
        apellido_materno (VARCHAR)
        fecha_nacimiento (DATE)
        tipo_usuario (VARCHAR)
        cesfam (VARCHAR)
        telefono (VARCHAR)
        direccion (VARCHAR)

clases
    Catálogo de clases disponibles en el gimnasio.
        id_clase (INT) - Identificador único (PK)
        nombre_clase (VARCHAR) - Nombre de la clase

profesores
    Registro de profesores del gimnasio.
        id_profesor (INT) - Identificador único (PK)
        nombre_completo (VARCHAR) - Nombre del profesor

asistencias
    Registro histórico de asistencias.
        id_asistencia (INT) - Identificador único (PK, AUTO_INCREMENT)
        rut (VARCHAR) - RUT del participante (FK)
        dv (VARCHAR) - Dígito verificador
        id_clase (INT) - Clase asistida (FK)
        id_profesor (INT) - Profesor de la clase (FK)
        fecha (DATE) - Fecha de la asistencia
        hora (TIME) - Hora del registro


Despliegue en Producción
    Servidor Windows 11 (Recomendado)
    Instalar Python desde python.org
    Instalar MariaDB desde mariadb.org
    Clonar el repositorio en el servidor
    Configurar el firewall para permitir conexiones en el puerto 5000
    Crear un servicio de Windows para auto-inicio
           pwshell: sc.exe create AsistenciaGym binPath= "C:\Python\python.exe C:\ruta\a\app.py" start= auto

Acceso desde la Red Local
    Cambiar en app.py:  app.run(debug=False, host='0.0.0.0', port=5000)

Mejoras Futuras

    Sistema de autenticación para administradores
    Exportación de reportes a Excel/PDF
    Gráficos estadísticos de asistencia
    Notificaciones por email/SMS
    Aplicación móvil nativa
    Integración con sistemas de pago
    Control de acceso por huella digital

Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

Autor
[Dario]
GitHub: @daario-toro
Email: prof.dario.toro@gmail.com


Agradecimientos
Flask - Framework web
Tailwind CSS - Framework CSS
MariaDB - Base de datos
SweetAlert2 - Notificaciones
Font Awesome - Iconos

<div align="center">
<p>Desarrollado con ❤️ para la comunidad</p>
<p>⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub</p>
</div>