# servidor.py

import sqlite3
from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Configuración de la Aplicación y la Base de Datos (SQLite)

app = Flask(__name__)
DB_NAME = 'tareas.db'

# Función auxiliar para conectar a la DB
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return conn

# Función para inicializar la base de datos y crear la tabla de usuarios
def init_db():
    conn = get_db_connection()
    # Creamos la tabla 'usuarios' para almacenar credenciales
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Inicializamos la DB al inicio
init_db()

# 2. Endpoint: Registro de Usuarios

@app.route('/registro', methods=['POST'])
def registro():
    """
    Endpoint: POST /registro
    Recibe {"usuario": "nombre", "contraseña": "1234"} y almacena al usuario con contraseña hasheada.
    """
    data = request.get_json()

    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"mensaje": "Datos de usuario y/o contraseña faltantes"}), 400

    usuario = data['usuario']
    contrasena = data['contraseña']

    # Hasheamos la contraseña antes de almacenarla (¡Nunca en texto plano!) [cite: 12, 19]
    contrasena_hash = generate_password_hash(contrasena)

    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)",
            (usuario, contrasena_hash)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

    except sqlite3.IntegrityError:
        # Se activa si el usuario ya existe (UNIQUE NOT NULL)
        return jsonify({"mensaje": "Error: El usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"mensaje": f"Error interno del servidor: {e}"}), 500

# 3. Endpoint: Inicio de Sesión (Login)

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint: POST /login
    Verifica credenciales.
    """
    data = request.get_json()

    if not data or 'usuario' not in data or 'contraseña' not in data:
        return jsonify({"mensaje": "Datos de usuario y/o contraseña faltantes"}), 400

    usuario = data['usuario']
    contrasena = data['contraseña']

    conn = get_db_connection()
    user_record = conn.execute(
        "SELECT contrasena_hash FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    conn.close()

    if user_record:
        # Verificamos la contraseña hasheada [cite: 15]
        stored_hash = user_record['contrasena_hash']
        if check_password_hash(stored_hash, contrasena):
            return jsonify({"mensaje": "Inicio de sesión exitoso. Acceso a /tareas permitido."}), 200
        else:
            return jsonify({"mensaje": "Contraseña incorrecta"}), 401
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

# 4. Endpoint: Gestión de Tareas (Bienvenida)

@app.route('/tareas', methods=['GET'])
def tareas():
    """
    Endpoint: GET /tareas
    Muestra un html de bienvenida (simulando acceso a recursos protegidos).
    """
    # Nota: Para una implementación real, aquí se debería verificar la autenticación
    # (por ejemplo, con un token o sesión) antes de renderizar la plantilla.

    # Usaremos una plantilla simple (o simplemente retornar un HTML) [cite: 17]
    return render_template('tareas_bienvenida.html', usuario='Usuario Autenticado')


if __name__ == '__main__':
    # Necesitas instalar flask y werkzeug si aún no lo has hecho:
    # pip install Flask werkzeug
    app.run(debug=True)

# ----------------------------------------------------------------------
# PASOS SIGUIENTES:
# 1. Crear la plantilla HTML: 'tareas_bienvenida.html'
# 2. Crear el cliente en consola: 'cliente.py' (para probar los endpoints) 
# 3. Crear el README.md con las instrucciones [cite: 25]