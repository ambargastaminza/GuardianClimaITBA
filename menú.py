# GuardianClimaITBA //
import csv
import os
import re
from modulo_clima import obtener_clima, mostrar_clima, guardar_en_historial
load_dotenv()
api_key = os.getenv("API_KEY")

ARCHIVO_USUARIOS = 'usuarios_simulados.csv'
ARCHIVO_HISTORIAL = 'historial.csv'


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

# Historial personal por ciudad:

def ver_historial_personal(username):

    print(f"\n--- Historial de consultas de {username} ---")
    with open(ARCHIVO_HISTORIAL, mode='r', newline='') as archivo:
        lector = csv.DictReader(archivo)
        encontrado = False
        for fila in lector:
            if fila['username'] == username:
                print(f"{fila['fecha_hora']} | {fila['ciudad']} | {fila['temperatura']}°C | {fila['condicion_clima']}")
                encontrado = True
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("Aún no hay historial disponible.")
        return

    if not encontrado:
        print("No se encontraron consultas guardadas para este usuario.")

# Estadísticas globales y exportación:

import pandas as pd

def estadisticas_globales():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("No hay historial para analizar.")
        return
    with open(ARCHIVO_HISTORIAL, mode='w', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['username', 'ciudad', 'fecha_hora', 'temperatura', 'condicion_clima', 'humedad', 'viento'])

    df = pd.read_csv(ARCHIVO_HISTORIAL)
    print("\n--- Estadísticas Globales ---")
    print("Cantidad total de consultas:", len(df))
    print("Ciudades más consultadas:")
    print(df['ciudad'].value_counts().head(5))

    promedio_temp = df['temperatura'].mean()
    print(f"Temperatura promedio global: {promedio_temp:.1f}°C")

    exportar = input("¿Querés exportar el historial completo a Excel? (s/n): ").lower()
    if exportar == 's':
        df.to_excel("historial_exportado.xlsx", index=False)
        print("Historial exportado como 'historial_exportado.xlsx'")



# ------------------ MENÚ PRINCIPAL ------------------


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
           print("[Opción 1] Consultar clima (a implementar)")
           ciudad = input("Ingrese el nombre de la ciudad: ")
           datos = obtener_clima(ciudad, api_key)

           if datos:
               mostrar_clima(datos)
               guardar_en_historial(nombre_usuario, datos)
               print("Consulta guardada. ✅ ")
           else:
               print("No se pudo obtener el clima.")


       elif opcion == '2':
           print("[Opción 2] Ver historial personal (a implementar)")
           ver_historial_personal(username)
       elif opcion == '3':
           print("[Opción 3] Estadísticas globales (a implementar)")
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
           menu_principal(username)
           break
       else:
           print("\nTu contraseña no cumple con los siguientes criterios:")
           for error in errores:
               print(f" - Debe {error}")
           print("Recomendación: Usá una combinación de letras mayúsculas, minúsculas, números y símbolos.")


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

inicializar_archivo_usuarios()
menu_acceso()

# ------------------ MAIN ------------------