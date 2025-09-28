# cliente.py

import requests
import json

# URL base de tu API Flask (debe estar corriendo en el puerto 5000 por defecto)
API_URL = 'http://127.0.0.1:5000'

def registrar_usuario(usuario, contrasena):
    """Prueba el endpoint POST /registro"""
    print(f"\n--- 1. Probando REGISTRO de '{usuario}' ---")
    url = f'{API_URL}/registro'
    payload = {
        "usuario": usuario,
        "contraseña": contrasena
    }
    
    try:
        response = requests.post(url, json=payload)
        
        print(f"Estado: {response.status_code}")
        print(f"Respuesta del Servidor: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("ERROR: No se pudo conectar al servidor. Asegúrate de que 'servidor.py' esté corriendo.")

def iniciar_sesion(usuario, contrasena):
    """Prueba el endpoint POST /login"""
    print(f"\n--- 2. Probando LOGIN de '{usuario}' ---")
    url = f'{API_URL}/login'
    payload = {
        "usuario": usuario,
        "contraseña": contrasena
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Estado: {response.status_code}")
        print(f"Respuesta del Servidor: {response.json()}")
        
        # Devolvemos el estado de éxito para saber si intentar acceder a tareas
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("ERROR: No se pudo conectar al servidor.")
        return False

def acceder_tareas():
    """Prueba el endpoint GET /tareas"""
    print("\n--- 3. Probando ACCESO a TAREAS (GET /tareas) ---")
    url = f'{API_URL}/tareas'
    
    try:
        response = requests.get(url)
        print(f"Estado: {response.status_code}")
        
        if response.status_code == 200:
            # Imprimimos solo las primeras 200 caracteres del HTML para no saturar
            print(f"Contenido (HTML): {response.text[:200]}...")
        else:
             print("Acceso a tareas fallido.")

    except requests.exceptions.ConnectionError:
        print("ERROR: No se pudo conectar al servidor.")

# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    # --- EJECUCIÓN DE PRUEBA EXITOSA ---
    
    USER = "testuser"
    PASS = "SecurePFO2"
    
    # 1. Registrar un nuevo usuario
    registrar_usuario(USER, PASS)
    
    # 2. Intentar registrar el mismo usuario (debería fallar con 409)
    registrar_usuario(USER, PASS) 
    
    # 3. Iniciar sesión con credenciales correctas
    if iniciar_sesion(USER, PASS):
        # 4. Acceder al recurso protegido /tareas
        acceder_tareas()
        
    # --- PRUEBA DE FALLO DE LOGIN ---
    
    print("\n" + "="*50)
    iniciar_sesion(USER, "contraseña_incorrecta")
    print("="*50)
    
    print("\n>>> FIN DE PRUEBAS DEL CLIENTE <<<")