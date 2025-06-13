# GuardianClimaITBA //
import csv
import os
import re
import requests
import pandas as pd
from datetime import datetime

ARCHIVO_USUARIOS = 'usuarios_simulados.csv'
ARCHIVO_HISTORIAL = 'historial_global.csv'

# ------------------ VALIDACIÓN DE CONTRASEÑAS ------------------

def validar_contrasena(password):
    errores = []
    if len(password) < 8:
        errores.append("tener al menos 8 caracteres")
    if not re.search(r'[A-Z]', password):
        errores.append("incluir al menos una letra mayúscula")
    if not re.search(r'[a-z]', password):
        errores.append("incluir al menos una letra minúscula")
    if not re.search(r'\d', password):
        errores.append("incluir al menos un número")
    if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]', password):
        errores.append("incluir al menos un carácter especial")

    return (False, errores) if errores else (True, [])

# ------------------ INICIALIZACIÓN DE ARCHIVOS ------------------

def inicializar_archivo_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, mode='w', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['username', 'password_simulada'])

# ------------------ FUNCIONES DE USUARIO ------------------

def existe_usuario(username):
    with open(ARCHIVO_USUARIOS, mode='r', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['username'] == username:
                return True
    return False

def guardar_usuario(username, password):
    with open(ARCHIVO_USUARIOS, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([username, password])

# ------------------ FUNCIONES CLIMA ------------------

def obtener_clima(ciudad, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': ciudad,
        'appid': api_key,
        'units': 'metric',
        'lang': 'es'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None

def guardar_en_historial(username, ciudad, datos):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperatura = datos['main']['temp']
    condicion = datos['weather'][0]['description']
    humedad = datos['main']['humidity']
    viento = datos['wind']['speed']
    nuevo = not os.path.exists(ARCHIVO_HISTORIAL)
    with open(ARCHIVO_HISTORIAL, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        if nuevo:
            escritor.writerow(['username', 'ciudad', 'fecha_hora', 'temperatura', 'condicion_clima', 'humedad', 'viento'])
        escritor.writerow([username, ciudad, fecha_hora, temperatura, condicion, humedad, viento])

def consultar_clima_y_guardar(username, api_key):
    ciudad = input("Ingresá el nombre de la ciudad: ").strip()
    datos = obtener_clima(ciudad, api_key)
    if datos:
        try:
            print("\n=== Clima Actual ===")
            print(f"Ciudad: {ciudad}")
            print(f"Temperatura: {datos['main']['temp']}°C")
            print(f"Sensación térmica: {datos['main']['feels_like']}°C")
            print(f"Humedad: {datos['main']['humidity']}%")
            print(f"Condición: {datos['weather'][0]['description'].capitalize()}")
            print(f"Viento: {datos['wind']['speed']} km/h")
            guardar_en_historial(username, ciudad, datos)
            print("✅ Consulta guardada en el historial.\n")
        except KeyError:
            print("❌ Error inesperado al procesar los datos de la API.")

# ------------------ FUNCIONES EXTRA ------------------

def ver_historial_personal(username):
    print(f"\n--- Historial de consultas de {username} ---")
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("Aún no hay historial disponible.")
        return
    encontrado = False
    with open(ARCHIVO_HISTORIAL, mode='r', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['username'] == username:
                print(f"{fila['fecha_hora']} | {fila['ciudad']} | {fila['temperatura']}°C | {fila['condicion_clima']}")
                encontrado = True
    if not encontrado:
        print("No se encontraron consultas guardadas para este usuario.")

def estadisticas_globales():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("No hay historial para analizar.")
        return
    df = pd.read_csv(ARCHIVO_HISTORIAL)
    print("\n--- Estadísticas Globales ---")
    print("Cantidad total de consultas:", len(df))
    print("Ciudades más consultadas:")
    print(df['ciudad'].value_counts().head(5))
    promedio_temp = df['temperatura'].mean()
    print(f"Temperatura promedio global: {promedio_temp:.1f}°C")
    if input("¿Querés exportar el historial completo a Excel? (s/n): ").lower() == 's':
        df.to_excel("historial_exportado.xlsx", index=False)
        print("Historial exportado como 'historial_exportado.xlsx'")

# ------------------ MENÚS ------------------

def menu_principal(username):
    print("DEBUG: ENTRANDO AL MENÚ PRINCIPAL")
    while True:
        print(f"\n=== Menú Principal - Bienvenido/a, {username} ===")
        print("1. Consultar clima actual y guardar en historial")
        print("2. Ver mi historial personal por ciudad")
        print("3. Ver estadísticas globales y exportar historial")
        print("4. Consejo IA: ¿Cómo me visto hoy?")
        print("5. Acerca de GuardiánClima ITBA")
        print("6. Cerrar sesión")
        opcion = input("Seleccioná una opción: ")
        if opcion == '1':
            consultar_clima_y_guardar(username, "TU_API_KEY")
        elif opcion == '2':
            ver_historial_personal(username)
        elif opcion == '3':
            estadisticas_globales()
        elif opcion == '4':
            print("[Opción 4] Consejo IA (a implementar)")
        elif opcion == '5':
            mostrar_info_aplicacion()
        elif opcion == '6':
            print("Cerrando sesión...\n")
            break
        else:
            print("Opción inválida. Intentá de nuevo.")

def mostrar_info_aplicacion():
    print("\n--- Acerca de GuardiánClima ITBA ---")
    print("GuardiánClima ITBA es una herramienta pensada para ayudarte a enfrentar el día con información precisa y relevante.")
    print("Permite consultar el clima en tiempo real, guardar tu historial de búsquedas, analizar patrones y obtener consejos útiles de vestimenta usando inteligencia artificial.")
    print("Diseñada con foco en la experiencia del usuario, combina programación, análisis de datos y tecnologías actuales para ofrecer una solución simple, funcional y con proyección real.")
    print()
    print("\n¿Cómo se usa?")
    print("- Menú de Acceso: podés iniciar sesión o registrarte.")
    print("- Menú Principal:")
    print("  1. Consulta del clima y guardado en historial global.")
    print("  2. Visualización del historial personal.")
    print("  3. Estadísticas globales y exportación del historial.")
    print("  4. Consejo de vestimenta basado en IA (próximamente).")
    print("  5. Información general de la aplicación.")
    print("  6. Cierre de sesión.")
    print()
    print("\n¿Cómo funciona por dentro?")
    print("- Gestión simulada de usuarios y contraseñas en CSV con fines exclusivamente educativos.")
    print("- Validación de contraseñas con criterios de ciberseguridad.")
    print("- Almacenamiento de consultas climáticas en historial global.")
    print("- Cálculo de estadísticas a partir del historial.")
    print("- Generación de reportes exportables para análisis externo.")
    print()
    print("\n🙋 Desarrolladores:")
    print("- Barbás Delfina")
    print("- Gastaminza Ámbar")
    print("- Lee Angulo Osmary")
    print("- López Antolin María")
    print("- Saldivia Ramiro")
    print("\n🫂 Equipo de desarrollo:")
    print("Nombre del grupo: [ELEGIR NOMBRE DEL GRUPO]")

# ------------------ FLUJO DE ACCESO ------------------

def registrar_usuario():
    print("\n--- Registro de Nuevo Usuario ---")
    username = input("Elegí un nombre de usuario: ")
    if existe_usuario(username):
        print("Ese nombre de usuario ya está registrado. Probá con otro.")
        return
    while True:
        password = input("Ingresá una contraseña segura: ")
        es_valida, errores = validar_contrasena(password)
        if es_valida:
            guardar_usuario(username, password)
            print(f"Usuario '{username}' registrado con éxito.")
            menu_principal(username)
            break
        else:
            print("\n❌ Tu contraseña no cumple con los siguientes criterios:")
            for error in errores:
                print(f" - Debe {error}")
            print("🔐 Recomendación: Usá una combinación de letras mayúsculas, minúsculas, números y símbolos.")

def iniciar_sesion():
    print("\n--- Iniciar Sesión ---")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    with open(ARCHIVO_USUARIOS, mode='r', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['username'] == username and fila['password_simulada'] == password:
                print(f"Inicio de sesión exitoso. Bienvenido, {username}!")
                menu_principal(username)
                return
    print("❌ Credenciales incorrectas. Intentá de nuevo.")

def menu_acceso():
    while True:
        print("\n=== GuardiánClima ITBA ===")
        print("1. Iniciar Sesión")
        print("2. Registrar Nuevo Usuario")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            iniciar_sesion()
        elif opcion == '2':
            registrar_usuario()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

# ------------------ MAIN ------------------

inicializar_archivo_usuarios()
menu_acceso()
