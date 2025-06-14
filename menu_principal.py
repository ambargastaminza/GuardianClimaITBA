## MENÚ PRINCIPAL - GuardianClimaITBA

import pandas as pd
import csv
import os
from obtener_clima import obtener_clima, guardar_en_historial, mostrar_clima, ARCHIVO_HISTORIAL
import matplotlib.pyplot as plt
from generativeIA import obtener_consejo_ia_gemini
import os


def consultar_clima_y_guardar(username):
    ciudad = input("Ingresá el nombre de la ciudad: ").strip()
    datos = obtener_clima(ciudad)

    if datos:
        mostrar_clima(datos)
        guardar_en_historial(username, datos)
        print("✅ Consulta guardada en el historial.")
    else:
        print("❌ No se pudo obtener el clima.")


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
                print(f"{fila['fecha_hora']} | {fila['ciudad']} | {fila['temperatura']}°C | {fila['descripcion'].capitalize()}")
                encontrado = True

    if not encontrado:
        print("No se encontraron consultas guardadas para este usuario.")

def ver_historial_por_fecha(username):
    if not os.path.exists(ARCHIVO_HISTORIAL):
        print("No hay historial disponible.")
        return

    fecha_inicio = input("Ingresá fecha inicio (YYYY-MM-DD): ").strip()
    fecha_fin = input("Ingresá fecha fin (YYYY-MM-DD): ").strip()
    try:
        inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de fecha inválido.")
        return

    if inicio > fin:
        print("La fecha inicio debe ser menor o igual a fecha fin.")
        return

    encontrado = False
    with open(ARCHIVO_HISTORIAL, mode='r', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['username'] == username:
                fecha_consulta = datetime.datetime.strptime(fila['fecha_hora'], "%Y-%m-%d %H:%M:%S").date()
                if inicio <= fecha_consulta <= fin:
                    print(f"{fila['fecha_hora']} | {fila['ciudad']} |_]()

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

    if input("\n¿Querés exportar el historial completo a Excel? (s/n): ").lower() == 's':
        df.to_excel("historial_exportado.xlsx", index=False)
        print("Historial exportado como 'historial_exportado.xlsx'")

def exportar_historial_usuario(username):
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
    print(f"Historial personal exportado a {nombre_archivo}")


    # -------- GRÁFICOS --------
    if input("\n¿Querés generar gráficos con los datos globales? (s/n): ").lower() == 's':
        # 1. Gráfico de Barras: cantidad de consultas por ciudad
        plt.figure(figsize=(10, 5))
        df['ciudad'].value_counts().plot(kind='bar', color='skyblue')
        plt.title('Consultas por Ciudad')
        plt.xlabel('Ciudad')
        plt.ylabel('Cantidad de consultas')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # 2. Gráfico de Líneas: temperatura a lo largo del tiempo para una ciudad específica
        ciudad_elegida = input("Para el gráfico de líneas, ingresá una ciudad: ").strip()
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
            print(f"No hay suficientes datos para la ciudad '{ciudad_elegida}'.")

        # 3. Gráfico de Torta: distribución de condiciones climáticas
        condiciones = df['descripcion'].str.capitalize().value_counts()
        plt.figure(figsize=(6, 6))
        condiciones.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title("Distribución de Condiciones Climáticas")
        plt.ylabel('')
        plt.tight_layout()
        plt.show()


def mostrar_consejo_ia(username):
    api_key = os.getenv("API_KEY_GEMINI")
    if not api_key:
        print("❌ No se encontró la API KEY de Gemini. Verificá tu archivo .env")
        return

    ciudad = input("Ingresá el nombre de la ciudad para obtener un consejo de vestimenta: ").strip()
    datos = obtener_clima(ciudad)

    if not datos:
        print("❌ No se pudo obtener el clima.")
        return

    temperatura = datos['temperatura']
    condicion = datos['descripcion']
    viento = datos['viento']
    humedad = datos['humedad']

    consejo = obtener_consejo_ia_gemini(api_key, temperatura, condicion, viento, humedad)
    print(f"\n🧥 Consejo de vestimenta para hoy en {ciudad.capitalize()}:")
    print(f"{consejo}")


def mostrar_info_aplicacion():
    print("\n--- Acerca de GuardiánClima ITBA ---")
    print("GuardiánClima ITBA es una herramienta pensada para ayudarte a enfrentar el día con información precisa y relevante.")
    print("Permite consultar el clima en tiempo real, guardar tu historial de búsquedas, analizar patrones y obtener consejos útiles de vestimenta usando inteligencia artificial.")
    print("Diseñada con foco en la experiencia del usuario, combina programación, análisis de datos y tecnologías actuales para ofrecer una solución simple, funcional y con proyección real.")
    print("\n¿Cómo se usa?")
    print("- Menú de Acceso: podés iniciar sesión o registrarte.")
    print("- Menú Principal:")
    print("  1. Consulta del clima y guardado en historial global.")
    print("  2. Visualización del historial personal.")
    print("  3. Estadísticas globales y exportación del historial.")
    print("  4. Consejo de vestimenta basado en IA (próximamente).")
    print("  5. Información general de la aplicación.")
    print("  6. Cierre de sesión.")
    print("\n🙋 Desarrolladores:")
    print("- Barbás Delfina\n- Gastaminza Ámbar\n- Lee Angulo Osmary\n- López Antolin María\n- Saldivia Ramiro")
    print("\n🫂 Equipo de desarrollo:")
    print("Nombre del grupo: Aeolos")


def menu_principal(username):
    while True:
        print(f"\n=== Menú Principal - Bienvenido/a, {username} ===")
        print("1. 🌤️ Consultar clima actual y guardar en historial")
        print("2. 🗂️ Ver mi historial personal por ciudad")
        print("3. 📊 Ver estadísticas globales y exportar historial")
        print("4. 🪄 Vestite según el clima (versión IA)")
        print("5. ℹ️ Acerca de GuardiánClima ITBA")
        print("6. 🚪 Cerrar sesión")
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            consultar_clima_y_guardar(username)
        elif opcion == '2':
            ver_historial_personal(username)
        elif opcion == '3':
            estadisticas_globales()
        elif opcion == '4':
            mostrar_consejo_ia(username)
        elif opcion == '5':
            mostrar_info_aplicacion()
        elif opcion == '6':
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida. Intentá de nuevo.")
