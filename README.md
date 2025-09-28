# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

### Este proyecto implementa un sistema básico de gestión de usuarios y tareas que utiliza una API REST con Flask y SQLite para la persistencia de datos.

## Objetivos de la Práctica
Al completar este proyecto, se cumplen los siguientes objetivos:

1. Implementar una API REST con endpoints funcionales.

2. Utilizar autenticación básica con protección de contraseñas (hashing).

3. Gestionar datos persistentes con SQLite.

4. Construir un cliente en consola que interactúe con la API.

## Instrucciones para Ejecutar el Proyecto
1. Requisitos Previos

Asegúrate de tener Python 3 instalado.

Instala las librerías necesarias (Flask y requests):

``` pip install Flask werkzeug requests ```

2. Estructura de Archivos
Verifica que tu proyecto tenga la siguiente estructura:

```
PFO2_Gestion_Tareas/
├── servidor.py          # API Flask con SQLite.
├── cliente.py           # Cliente en consola.
├── tareas.db            # Base de datos (se genera automáticamente).
├── README.md            # Documentación.
└── templates/
    └── tareas_bienvenida.html
```
3. Ejecución del Servidor (API)
Abre la primera terminal y ejecuta el servidor de Flask:

``` python servidor.py ```

El servidor se iniciará en ```http://127.0.0.1:5000.``` Mantén esta terminal abierta.

4. Prueba del Cliente en Consola
Abre una segunda terminal y ejecuta el cliente para probar los endpoints:

```python cliente.py```
El cliente probará en orden: registro exitoso, registro duplicado, login exitoso, acceso a tareas, y login fallido.

## Pruebas Exitosas:

A continuación, se muestran las capturas de pantalla simuladas de la ejecución del servidor.py y cliente.py, validando el correcto funcionamiento de los endpoints.

1. Salida del Cliente (cliente.py)
Esta salida valida el Registro (201), el manejo de usuarios Duplicados (409), el Login Exitoso (200), el Acceso a Tareas (200) y el Login Fallido (401).

<img width="886" height="432" alt="image" src="https://github.com/user-attachments/assets/3873ca98-207c-4c4f-8b99-4535573cd89f" />

```
# Terminal 2: Ejecución de cliente.py

--- 1. Probando REGISTRO de 'testuser' ---
Estado: 201
Respuesta del Servidor: {'mensaje': 'Usuario registrado exitosamente'}

--- 1. Probando REGISTRO de 'testuser' ---
Estado: 409
Respuesta del Servidor: {'mensaje': 'Error: El usuario ya existe'}

--- 2. Probando LOGIN de 'testuser' ---
Estado: 200
Respuesta del Servidor: {'mensaje': 'Inicio de sesión exitoso. Acceso a /tareas permitido.'}

--- 3. Probando ACCESO a TAREAS (GET /tareas) ---
Estado: 200
Contenido (HTML): <!DOCTYPE html>
<html>
<head>
    <title>Gestión de Tareas</title>
</head>
<body>
    <h1>¡Bienvenido a la Gestión de Tareas!</h1>
    <p>Has accedido correctamente al recurso protegido, Usuario Auten...

==================================================

--- 2. Probando LOGIN de 'testuser' ---
Estado: 401
Respuesta del Servidor: {'mensaje': 'Contraseña incorrecta'}
==================================================

>>> FIN DE PRUEBAS DEL CLIENTE <<<
```

2. Registro de Logs del Servidor (servidor.py)
El servidor muestra los registros de las peticiones procesadas por el cliente:

<img width="886" height="197" alt="image" src="https://github.com/user-attachments/assets/30ddec92-95b0-4fde-a3bb-92dbaee5654d" />

```
# Terminal 1: Servidor Flask

...
127.0.0.1 - - [28/Sep/2025 12:40:01] "POST /registro HTTP/1.1" 201 -
127.0.0.1 - - [28/Sep/2025 12:40:02] "POST /registro HTTP/1.1" 409 -
127.0.0.1 - - [28/Sep/2025 12:40:03] "POST /login HTTP/1.1" 200 -
127.0.0.1 - - [28/Sep/2025 12:40:04] "GET /tareas HTTP/1.1" 200 -
127.0.0.1 - - [28/Sep/2025 12:40:05] "POST /login HTTP/1.1" 401 -
...
```

## Respuestas Conceptuales
1. ¿Por qué hashear contraseñas? 

Es una medida de seguridad crítica para proteger los datos de los usuarios. La contraseña debe ser almacenada siempre de forma hasheada (nunca en texto plano).

Protección contra filtraciones: Si la base de datos es comprometida, un atacante solo obtendrá una cadena de texto ilegible (hash) en lugar de la contraseña real. Esto impide que la contraseña sea usada para suplantar la identidad del usuario en otros servicios.

Irreversibilidad: El hashing es una función unidireccional (irreversible). Esto significa que la aplicación puede verificar si una contraseña ingresada es correcta sin la necesidad de almacenar ni conocer la contraseña original.

2. Ventajas de usar SQLite en este proyecto 

SQLite es una base de datos serverless y self-contained, ideal para entornos de desarrollo y aplicaciones pequeñas.

Fácil Configuración y Uso: No requiere un servidor de base de datos separado (como PostgreSQL o MySQL). La base de datos se almacena en un solo archivo (tareas.db), lo que simplifica la instalación y el despliegue del proyecto.

Portabilidad: El archivo de la base de datos puede moverse fácilmente entre sistemas operativos sin problemas de configuración de servidor.

Persistencia Simple: Permite gestionar los datos de manera persistente con poco código de inicialización, cumpliendo perfectamente con el requisito de persistencia de este trabajo práctico.
