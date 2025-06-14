##  GENERATIVE IA

import google.generativeai as genai
from dotenv import load_dotenv
import os 

load_dotenv()
api_key_gemini = os.getenv("API_KEY_GEMINI")
modelo_gemini = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if not api_key_gemini:
    raise ValueError("⚠️ No se encontró la API_KEY_GEMINI en el archivo .env")


def obtener_consejo_ia_gemini(temperatura, condicion_clima, viento, humedad):
    """Genera un consejo de vestimenta usando IA de Google Gemini."""
    try:
        # Validación básica de datos climáticos
        if None in (temperatura, condicion_clima, viento, humedad):
            return "⚠️ Faltan datos climáticos para generar el consejo."

        genai.configure(api_key=api_key_gemini)
        model = genai.GenerativeModel(modelo_gemini)

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
