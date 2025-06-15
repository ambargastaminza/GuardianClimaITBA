import pandas as pd
import csv
import os
from obtener_clima import obtener_clima, guardar_en_historial, mostrar_clima, ARCHIVO_HISTORIAL
import matplotlib.pyplot as plt
from generativeIA import obtener_consejo_ia_gemini
import os
import datetime

def consultar_clima_y_guardar(username):
    ciudad = input("Ingresá el nombre de la ciudad: ").strip()
    datos = obtener_clima(ciudad)

    if datos:
        mostrar_clima(datos)
        guardar_en_historial(username, datos)
        print("Consulta guardada en el historial.")
    else:
        print("No se pudo obtener el clima.")

def ver_historial_personal(username):
    print(f"\n🗂️ Historial de consultas de {username}")
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
        print("⚠️ Formato de fecha inválido. Usá YYYY-MM-DD.")
        return

    if inicio > fin:
        print("⚠️ La fecha de inicio debe ser menor o igual a la fecha de fin.")
        return

    encontrado = False
    with open(ARCHIVO_HISTORIAL, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila['username'].strip().lower() == username.strip().lower():
                try:
                    fecha_consulta = datetime.datetime.fromisoformat(fila['fecha_hora'].strip()).date()
                except ValueError:
                    continue
                if inicio <= fecha_consulta <= fin:
                    print(f"{fila['username']} | {fila['ciudad']} | {fila['fecha_hora']} | {fila['temperatura']}°C | {fila['descripcion'].capitalize()} | Humedad: {fila['humedad']}% | Viento: {fila['viento']} km/h")
                    encontrado = True

    if not encontrado:
        print("⚠️ No se encontraron consultas para ese rango de fechas.")


def estadisticas_globales():
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
    print("\nUsuarios con más consultas:")
    print(usuarios_top)

    if input("\nExportar historial completo a Excel? (s/n): ").lower() == 's':
        df.to_excel("historial_exportado.xlsx", index=False)
        print("Historial exportado como 'historial_exportado.xlsx'")

    if input("\nGenerar gráficos globales? (s/n): ").lower() == 's':
        plt.figure(figsize=(10, 5))
        df['ciudad'].value_counts().plot(kind='bar')
        plt.title('Consultas por Ciudad')
        plt.xlabel('Ciudad')
        plt.ylabel('Cantidad de consultas')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        ciudad_elegida = input("Ciudad para gráfico de temperatura en el tiempo: ").strip()
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

def mostrar_consejo_ia(username):
    api_key = os.getenv("API_KEY_GEMINI")
    if not api_key:
        print("No se encontró la API KEY de Gemini.")
        return

    ciudad = input("Ingresá ciudad para consejo de vestimenta: ").strip()
    datos = obtener_clima(ciudad)

    if not datos:
        print("No se pudo obtener el clima.")
        return

    temperatura = datos['temperatura']
    condicion = datos['descripcion']
    viento = datos['viento']
    humedad = datos['humedad']

    consejo = obtener_consejo_ia_gemini(api_key, temperatura, condicion, viento, humedad)
    print(f"\nConsejo de vestimenta para {ciudad.capitalize()}:")
    print(consejo)

def mostrar_info_aplicacion():
    print("\n--- Acerca de GuardiánClima ITBA ---")
    print("GuardiánClima ITBA es una herramienta pensada para ayudarte a enfrentar el día con información precisa y relevante.")
    print("Permite consultar el clima en tiempo real, guardar tu historial de búsquedas, analizar patrones y obtener consejos útiles de vestimenta usando inteligencia artificial.")
    print("Diseñada con foco en la experiencia del usuario, combina programación, análisis de datos y tecnologías actuales para ofrecer una solución simple, funcional y con proyección real.")
    print("\n¿Cómo se usa?")
    print("- Menú de Acceso: podés iniciar sesión o registrarte.")
    print("- Menú Principal:")
    print("  - Consulta del clima y guardado en historial global.")
    print("  - Visualización del historial personal.")
    print("  - Estadísticas globales y exportación del historial.")
    print("  - Consejo de vestimenta basado en IA (próximamente).")
    print("  - Información general de la aplicación.")
    print("  - Cierre de sesión.")
    print("\n🫂 Equipo de desarrollo:")
    print("Nombre del grupo: FALTA!!")
    print("\n🙋 Desarrolladores:")
    print("- Barbás Delfina\n- Gastaminza Ámbar\n- Lee Angulo Osmary\n- López Antolin María\n- Saldivia Ramiro")
   


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
        print("8. Cerrar sesión")

        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            consultar_clima_y_guardar(username)
            preguntar_volver_o_salir()
        elif opcion == '2':
            ver_historial_personal(username)
            preguntar_volver_o_salir()
        elif opcion == '3':
            ver_historial_por_fecha(username)
            preguntar_volver_o_salir()
        elif opcion == '4':
            exportar_historial_usuario(username)
            preguntar_volver_o_salir()
        elif opcion == '5':
            estadisticas_globales()
            preguntar_volver_o_salir()
        elif opcion == '6':
            mostrar_consejo_ia(username)
            preguntar_volver_o_salir()
        elif opcion == '7':
            mostrar_info_aplicacion()
            preguntar_volver_o_salir()
        elif opcion == '8':
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida. Intentá de nuevo.")
