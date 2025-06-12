# GuardianClimaITBA // 
import csv
import os
import re

ARCHIVO_USUARIOS = 'usuarios_simulados.csv'

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

    if errores:
        return False, errores
    else:
        return True, []

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

# ------------------ MENÚ PRINCIPAL ------------------

def menu_principal(username):
    print("DEBUG: ENTRANDO AL MENÚ PRINCIPAL")  # ← Para comprobar que entra
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
            print("[Opción 1] Consultar clima (a implementar)")
        elif opcion == '2':
            print("[Opción 2] Ver historial personal (a implementar)")
        elif opcion == '3':
            print("[Opción 3] Estadísticas globales (a implementar)")
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
    print("Esta aplicación permite consultar el clima, guardar un historial,")
    print("ver estadísticas globales y recibir consejos de vestimenta con IA.")
    print("Creada por el equipo [NOMBRE_DEL_GRUPO].")

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
            menu_principal(username)  # ← ACCEDE DIRECTO AL MENÚ
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
                menu_principal(username)  # ← ACCEDE DIRECTO AL MENÚ
    print("Credenciales incorrectas. Intentá de nuevo.")

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







