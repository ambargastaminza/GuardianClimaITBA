# MENU PRINCIPAL #

import pandas as pd
import csv
import os
from obtener_clima import obtener_clima, guardar_en_historial, mostrar_clima, ARCHIVO_HISTORIAL
import matplotlib.pyplot as plt
from generativeIA import obtener_consejo_ia_gemini
import datetime

def consultar_clima_y_guardar(username):
    while True:
        ciudad = input("Ingresá el nombre de la ciudad: ").strip()
        datos = obtener_clima(ciudad)

        if datos:
            mostrar_clima(datos)
            guardar_en_historial(username, datos)
            print("Consulta guardada en el historial.")
        else:
            print("No se pudo obtener el clima. Volvé a intentarlo.")

        if not preguntar_repetir_accion():
            break

def ver_historial_personal(username):
    while True:
        print(f"\n🗂️ Este es tu historial, {username}. Mirá todas tus consultas anteriores:")
        if not os.path.exists(ARCHIVO_HISTORIAL):
            print("No hay historial disponible.")
            return

        encontrado = False
        with open(ARCHIVO_HISTORIAL, mode='r', newline='') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila['username'] == username:
                    print(f"{fila['fecha_hora']} | {fila['ciudad']} | {fila['temperatura']}°C | {fila['descripcion'].capitalize()}")
                    encontrado = True

        if not encontrado:
            print("No se encontraron consultas para este usuario.")

        if not preguntar_repetir_accion():
            break

def ver_historial_por_fecha(username):
    while True:
        if not os.path.exists(ARCHIVO_HISTORIAL):
            print("No hay historial disponible.")
            return

        fecha_inicio = input("Ingresá una fecha de inicio (YYYY-MM-DD): ").strip()
        fecha_fin = input("Ingresá una fecha de fin (YYYY-MM-DD): ").strip()

        try:
            inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            print("⚠️ Formato de fecha inválido. Usá YYYY-MM-DD.")
            continue

        if inicio > fin:
            print("⚠️ La fecha de inicio debe ser menor o igual a la fecha de fin.")
            continue

        encontrado = False
        with open(ARCHIVO_HISTORIAL, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila['username'] == username:
                    try:
                        fecha_consulta = datetime.datetime.strptime(fila['fecha_hora'], "%Y-%m-%d %H:%M:%S").date()
                    except ValueError:
                        continue
                    if inicio <= fecha_consulta <= fin:
                        print(f"{fila['fecha_hora']} | {fila['ciudad']} | {fila['temperatura']}°C | {fila['descripcion'].capitalize()}")
                        encontrado = True

        if not encontrado:
            print("Ups! No se encontraron consultas para ese rango de fechas.")

        if not preguntar_repetir_accion():
            break

def estadisticas_globales():
    while True:
        if not os.path.exists(ARCHIVO_HISTORIAL):
            print("No hay historial para analizar.")
            return

        df = pd.read_csv(ARCHIVO_HISTORIAL)
        print("\nEstadísticas Globales")
        print("Cantidad total de consultas:", len(df))
        print("Ciudades más consultadas:")
        print(df['ciudad'].value_counts().head(5))
        print(f"Temperatura promedio global: {df['temperatura'].mean():.1f}°C")

        usuarios_top = df['username'].value_counts().head(5)
        print("\nUsuarios más activos:")
        print(usuarios_top)

        while True:
            respuesta = input("\n¿Exportar historial completo a Excel? (s/n): ").strip().lower()
            if respuesta == 's':
                df.to_excel("historial_exportado.xlsx", index=False)
                print("Historial exportado como 'historial_exportado.xlsx'")
                break
            elif respuesta == 'n':
                break
            else:
                print("Respuesta inválida. Escribí 's' para sí o 'n' para no.")

        while True:
            respuesta = input("\n¿Generar gráficos globales? (s/n): ").strip().lower()
            if respuesta == 's':
                plt.figure(figsize=(10, 5))
                df['ciudad'].value_counts().plot(kind='bar')
                plt.title('Consultas por Ciudad')
                plt.xlabel('Ciudad')
                plt.ylabel('Cantidad de consultas')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

                ciudad_elegida = input("Ingresá una para generar un gráfico de temperatura en el tiempo: ").strip()
                df_ciudad = df[df['ciudad'].str.lower() == ciudad_elegida.lower()]
                if not df_ciudad.empty:
                    df_ciudad['fecha_hora'] = pd.to_datetime(df_ciudad['fecha_hora'])
                    df_ciudad = df_ciudad.sort_values('fecha_hora')
                    plt.figure(figsize=(10, 5))
                    plt.plot(df_ciudad['fecha_hora'], df_ciudad['temperatura'], marker='o')
                    plt.title(f"Tendencia de Temperatura en {ciudad_elegida.capitalize()}")
                    plt.xlabel('Fecha y Hora')
                    plt.ylabel('Temperatura (°C)')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.show()
                else:
                    print("No hay suficientes datos para esa ciudad.")

                condiciones = df['descripcion'].str.capitalize().value_counts()
                plt.figure(figsize=(6, 6))
                condiciones.plot(kind='pie', autopct='%1.1f%%', startangle=90)
                plt.title("Distribución de Condiciones Climáticas")
                plt.ylabel('')
                plt.tight_layout()
                plt.show()
                break
            elif respuesta == 'n':
                break
            else:
                print("Respuesta inválida. Por favor, escribí 's' para sí o 'n' para no.")

        if not preguntar_repetir_accion():
            break

def mostrar_consejo_ia(username):
    api_key = os.getenv("API_KEY_GEMINI")
    if not api_key:
        print("Ups! Ocurrió un error con la API KEY de Gemini.")
        return

    while True:
        print("¡Hola! Soy tu asistente personal de moda.✨")
        print("Decime dónde estás y te ayudo a vestirte según el clima")
        ciudad = input("Ingresá una ciudad: ").strip()
        datos = obtener_clima(ciudad)

        if not datos:
            print("🤖 No pude generar un consejo. Asegurate de que el clima se pueda consultar.")
        else:
            temperatura = datos['temperatura']
            condicion = datos['descripcion']
            viento = datos['viento']
            humedad = datos['humedad']

            consejo = obtener_consejo_ia_gemini(api_key, temperatura, condicion, viento, humedad)
            print(f"\nConsejo de vestimenta para {ciudad.capitalize()}:\n{consejo}")

        if not preguntar_repetir_accion("¿Querés pedir otro consejo?"):
            break

def mostrar_info_aplicacion():
    print("\n--- Acerca de GuardiánClima ITBA ---")
    print("GuardiánClima ITBA es una herramienta pensada para ayudarte\n a enfrentar el día con información precisa y relevante.")
    print("Permite consultar el clima en tiempo real, guardar un historial de búsquedas,\n analizar patrones y obtener consejos útiles de vestimenta con inteligencia artificial.")
    print("Diseñada con foco en la experiencia del usuario, combina programación, análisis de datos\n y tecnologías actuales para ofrecer una solución simple, funcional y con proyección real.")
    print("\n¿Cómo se usa?")
    print("1. EN EL MENÚ DE ACCESO podés iniciar sesión o registrarte.")
    print("2. EN EL MENÚ PRINCIPAL SE LOGRA:")
    print("  - Consultar el clima y guardado en historial global.")
    print("  - Visualizar el historial personal.")
    print("  - Generar stadísticas globales y exportar del historial.")
    print("  - Recibir un consejo de vestimenta basado en IA.")
    print("  - Obtener información general de la aplicación.")
    print("  - Cerrar de sesión.")
    print("\n🫂 Equipo de desarrollo:")
    print("IAQ (Inteligencia Ambiental de Calidad)🧬")
    print("\n🙋 Desarrolladores:")
    print("- Barbás Delfina\n- Gastaminza Ámbar\n- Lee Angulo Osmary\n- López Antolin María\n- Saldivia Ramiro")

def exportar_historial_usuario(username):
    while True:
        if not os.path.exists(ARCHIVO_HISTORIAL):
            print("No hay historial para exportar.")
            return

        df = pd.read_csv(ARCHIVO_HISTORIAL)
        df_usuario = df[df['username'] == username]

        if df_usuario.empty:
            print("No hay datos para exportar.")
            return

        nombre_archivo = f"historial_{username}.xlsx"
        df_usuario.to_excel(nombre_archivo, index=False)
        print(f"📦 Tu historial fue exportado con éxito a {nombre_archivo} 🎉")


        if not preguntar_repetir_accion():
            break

def preguntar_volver_o_salir():
    while True:
        volver = input("\n¿Deseás volver al menú principal? (s/n): ").strip().lower()
        if volver == 's':
            return
        elif volver == 'n':
            print("Cerrando sesión...")
            exit()
        else:
            print("Respuesta inválida. Escribí 's' para sí o 'n' para no.")

def preguntar_repetir_accion(pregunta="¿Querés repetir esta acción?"):
    while True:
        respuesta = input(f"\n{pregunta} (s/n): ").strip().lower()
        if respuesta == 's':
            return True
        elif respuesta == 'n':
            return False
        else:
            print("Respuesta inválida. Escribí 's' para sí o 'n' para no.")

def menu_principal(username):
    while True:
        print(f"\nMenú Principal - Bienvenido/a {username}")
        print("1. 🌤️ Consultar clima y guardar en historial")
        print("2. Ver historial personal por ciudad")
        print("3. Ver historial personal por rango de fechas")
        print("4. Exportar mi historial personal a Excel")
        print("5. Estadísticas globales y exportar historial completo")
        print("6. 🪄 Vestite según el clima (versión IA)")
        print("7. Acerca de GuardiánClima ITBA")
        print("8. 🚪 Cerrar sesión y salir")


        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            consultar_clima_y_guardar(username)
        elif opcion == '2':
            ver_historial_personal(username)
        elif opcion == '3':
            ver_historial_por_fecha(username)
        elif opcion == '4':
            exportar_historial_usuario(username)
        elif opcion == '5':
            estadisticas_globales()
        elif opcion == '6':
            mostrar_consejo_ia(username)
        elif opcion == '7':
            mostrar_info_aplicacion()
            preguntar_volver_o_salir()
        elif opcion == '8':
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida. Intentá de nuevo.")
