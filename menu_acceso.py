## MENÚ DE ACCESO 

import csv
import os
import re
from dotenv import load_dotenv
from menu_principal import menu_principal
from seguridad import hashear_contrasena, verificar_contrasena

load_dotenv()

ARCHIVO_USUARIOS = os.path.join(os.path.dirname(__file__), 'usuarios_simulados.csv')

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

# ------------------ FUNCIONES DE ARCHIVO ------------------

def inicializar_archivo_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['username', 'password_hash']) 

def existe_usuario(username):
    username = username.lower()  
    if not os.path.exists(ARCHIVO_USUARIOS):
        return False
    with open(ARCHIVO_USUARIOS, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['username'].lower() == username:
                return True
    return False

def guardar_usuario(username, password_plano):
    username = username.lower()  
    password_hash = hashear_contrasena(password_plano)
    with open(ARCHIVO_USUARIOS, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([username, password_hash])

# ------------------ FLUJO DE ACCESO ------------------


def registrar_usuario():
    print("\n¡Hora de registrarte!")
    username = input("Elegí tu nombre de usuario: ").strip()

    if not username:
        print("⚠️ El nombre de usuario no puede estar vacío.")
        return
    if existe_usuario(username):
        print("Ups... ese nombre ya está en uso. Probá con otro.")
        return
    while True:
        print("🔐 Elegí una contraseña segura:")
        print("Debe tener al menos 8 caracteres, incluir mayúsculas, números y símbolos como ($%&!).")
        password = input("Ingresá tu contraseña: ")
        es_valida, errores = validar_contrasena(password)
        if es_valida:
            guardar_usuario(username, password)
            print(f"\n¡Listo, {username}! Tu cuenta fue creada con éxito.", flush=True)
            menu_principal(username.lower())  
            break
        else:
            print("\n❌ Tu contraseña no cumple con los siguientes criterios:")
            for error in errores:
                print(f" - Debe {error}")
            print("Recomendación: Usá una combinación de letras mayúsculas, minúsculas, números y símbolos.")

def iniciar_sesion():
    if not os.path.exists(ARCHIVO_USUARIOS):
        print("⚠️ No hay usuarios registrados aún.")
        return

    print("\n--- Iniciar Sesión ---")
    username = input("Usuario: ").strip().lower()

    with open(ARCHIVO_USUARIOS, mode='r', newline='', encoding='utf-8') as archivo:
        lector = list(csv.DictReader(archivo))
        for fila in lector:
            if fila['username'].lower() == username:
                for intento in range(2):
                    password = input("Contraseña: ")
                    if verificar_contrasena(password, fila['password_hash']):
                        print(f"Inicio de sesión exitoso. Bienvenido/a, {username}!", flush=True)
                        menu_principal(username)
                        return
                    else:
                        print("❌ Contraseña incorrecta.")
                        if intento == 0:
                            print("Intentá una vez más.")
                print("Demasiados intentos fallidos. Volviendo al menú de acceso...")
                return

    print("❌ No encontramos ese usuario.")
    print("¿Seguro que te registraste?")


def menu_acceso():
    inicializar_archivo_usuarios()
    while True:
        print("\n=== Accedé a GuardiánClima ITBA ☀️ ===")
        print("1. Iniciar sesión")
        print("2. Registrar nuevo usuario")
        print("3. Salir")
        opcion = input("Seleccioná una opción: ")
        if opcion == '1':
            iniciar_sesion()
        elif opcion == '2':
            registrar_usuario()
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta nuevamente con un número del 1 al 3.")

