import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

def obtener_clima(ciudad, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': ciudad,
        'appid': api_key,
        'units': 'metric',
        'lang': 'es'
    }

    try:
        respuesta = requests.get(url, params=params, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        clima = {
            'ciudad': ciudad,
            'fecha_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'temperatura': datos['main']['temp'],
            'descripcion': datos['weather'][0]['description'],
            'humedad': datos['main']['humidity'],
            'viento': datos['wind']['speed']
        }

        return clima

    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None


def guardar_en_historial(nombre_usuario, datos_clima):
    with open('historial_global.csv', mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([
            nombre_usuario,
            datos_clima['ciudad'],
            datos_clima['fecha_hora'],
            datos_clima['temperatura'],
            datos_clima['descripcion'],
            datos_clima['humedad'],
            datos_clima['viento']
        ])


def mostrar_clima(datos):
    print(f"\n📍 Ciudad: {datos['ciudad']}")
    print(f"📅 Fecha y hora: {datos['fecha_hora']}")
    print(f"🌡️ Temperatura: {datos['temperatura']}°C")
    print(f"💧 Humedad: {datos['humedad']}%")
    print(f"🌬️ Viento: {datos['viento']} km/h")
    print(f"🌤️ Descripción: {datos['descripcion'].capitalize()}")


