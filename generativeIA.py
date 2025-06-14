##  GENERATIVE IA

import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

load_dotenv()
api_key_gemini = os.getenv("API_KEY_GEMINI")
modelo_gemini = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not api_key_gemini:
    raise ValueError("⚠️ No se encontró la API_KEY_GEMINI en el archivo .env")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def obtener_consejo_ia_gemini(temperatura, condicion_clima, viento, humedad, temperatura_modelo=0.5):
    if not (isinstance(temperatura, (int, float)) and -50 <= temperatura <= 60):
        return "⚠️ Temperatura inválida."
    if not isinstance(condicion_clima, str) or not condicion_clima.strip():
        return "⚠️ Condición climática inválida."
    if not (isinstance(viento, (int, float)) and 0 <= viento <= 200):
        return "⚠️ Velocidad de viento inválida."
    if not (isinstance(humedad, (int, float)) and 0 <= humedad <= 100):
        return "⚠️ Humedad inválida."

    try:
        genai.configure(api_key=API_KEY_GEMINI)
        model = genai.GenerativeModel(MODELO_GEMINI)

        prompt = (
            f"Genera un consejo breve, neutral y útil de vestimenta para una persona "
            f"en las siguientes condiciones:\n"
            f"- Temperatura: {temperatura}°C\n"
            f"- Clima: {condicion_clima}\n"
            f"- Viento: {viento} km/h\n"
            f"- Humedad: {humedad}%\n"
            f"El consejo debe ser claro, directo y aplicable a cualquier contexto urbano."
        )

        print("\n🧠 Generando consejo de vestimenta con IA...")
        response = model.generate_content([prompt])

        if response.text:
            return response.text.strip()
        else:
            if hasattr(response, 'prompt_feedback'):
                print("🛑 Feedback de la IA:", response.prompt_feedback)
            return "No se pudo generar un consejo en este momento."

    except Exception as e:
        if "quota" in str(e).lower():
            return "🚫 Límite de uso alcanzado. Intentá más tarde o usá otra API key."
        return f"⚠️ Error al generar el consejo de IA: {e}"
