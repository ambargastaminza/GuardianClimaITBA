##  GENERATIVE IA

import google.generativeai as genai
from dotenv import load_dotenv
import os 

load_dotenv()
api_key_gemini = os.getenv("API_KEY_GEMINI")
if not api_key_gemini:
    raise ValueError("⚠️ No se encontró la API_KEY_GEMINI en el archivo .env")

def obtener_consejo_ia_gemini(api_key_gemini, temperatura, condicion_clima, viento, humedad):
    try:
        genai.configure(api_key=api_key_gemini)
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt_disenado_por_equipo = (
            f"Genera un consejo de vestimenta conciso y neutral en cuanto a género "
            f"para las siguientes condiciones climáticas:\n"
            f"- Temperatura: {temperatura}°C\n"
            f"- Condición climática: {condicion_clima}\n"
            f"- Viento: {viento} km/h\n"
            f"- Humedad: {humedad}%\n\n"
            f"El consejo debe ser práctico, directo y adecuado para cualquier persona."
        )

        print("\nGenerando consejo de vestimenta con IA...")
        response = model.generate_content([prompt_disenado_por_equipo])

        if response.text:
            return response.text.strip()
        else:
            print("La IA no pudo generar un consejo. Razón (si está disponible):")
            if hasattr(response, 'prompt_feedback'):
                print(response.prompt_feedback)
            return "No se pudo generar un consejo en este momento."

    except Exception as e:
        if "quota" in str(e).lower():
            return "🚫 Límite de uso alcanzado. Intentá más tarde o usá otra API key."
        return f"⚠️ Error al generar el consejo de IA: {e}"
