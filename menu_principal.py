## MENÚ PRINCIPAL - GuardianClimaITBA

import pandas as pd
import csv
import os
from obtener_clima import obtener_clima, guardar_en_historial, mostrar_clima

ARCHIVO_HISTORIAL = 'historial_global.csv'


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
    print("Nombre del grupo: [ELEGIR NOMBRE DEL GRUPO]")


def menu_principal(username):
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
            consultar_clima_y_guardar(username)
        elif opcion == '2':
            ver_historial_personal(username)
        elif opcion == '3':
            estadisticas_globales()
        elif opcion == '4':
            print("[Opción 4] Consejo IA (a implementar)")
        elif opcion == '5':
            mostrar_info_aplicacion()
        elif opcion == '6':
            print("Cerrando sesión...")
            break
        else:
            print("Opción inválida. Intentá de nuevo.")
