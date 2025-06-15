# GuardiánClima ITBA

GuardiánClima ITBA es una aplicación de consola desarrollada en Python como parte del Challenge Tecnológico Integrador del trayecto de Tecnología en el Proceso de admisión ITBA. La misma está diseñada para interactuar con datos climáticos, gestionar usuarios con validación de contraseñas seguras, registrar y analizar consultas, y generar consejos personalizados de vestimenta usando inteligencia artificial.

# Objetivos del Proyecto

- Desarrollar una aplicación funcional que integre Programación, Ciberseguridad, Análisis de Datos, Inteligencia Artificial y conceptos de Cloud Computing.
- Implementar un sistema de registro e inicio de sesión con validación de contraseñas seguras.
- Consultar el clima actual de cualquier ciudad mediante una API externa.
- Almacenar el historial de consultas en archivos `.csv`.
- Calcular estadísticas globales con opción de exportación y visualización en gráficos.
- Generar consejos de vestimenta utilizando una API de IA (Google Gemini).

# Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Módulos principales:**
  - `csv` para manejo de archivos
  - `requests` para acceso a APIs
  - `matplotlib` y `pandas` para análisis y visualización de datos
  - `bcrypt` para el hasheo de contraseñas
  - `dotenv` para gestión de variables de entorno
  - `google-generativeai` para generar consejos inteligentes

- **APIs externas:**
  - [OpenWeatherMap](https://openweathermap.org/) — Para obtener datos meteorológicos.
  - [Google Gemini](https://aistudio.google.com/) — Para generar consejos de vestimenta con IA.

-----------------------------------

# Instalación y Ejecución

1. **Clonar o descargar** este repositorio.
2. **Instalar dependencias** ejecutando:
   pip install -r requirements.txt
3. **Crear un archivo .env** con las siguientes variables:
API_KEY_CLIMA=tu_api_key_de_openweathermap
API_KEY_GEMINI=tu_api_key_de_google_gemini
4. Ejecutá el programa principal (main.py) desde consola

# ESTRUCTURA PRINCIPAL
menu_acceso.py: Inicio del programa, registro e inicio de sesión.
menu_principal.py: Lógica principal de las funciones del sistema.
obtener_clima.py: Manejo de clima e historial.
generativeIA.py: Conexión a Gemini API para consejos inteligentes.
seguridad.py: Validación y encriptado de contraseñas.
usuarios_simulados.csv: Almacena usuarios registrados.
historial_global.csv: Historial de todas las consultas realizadas.

**---------------------------------**

Proyecto desarrollado por el equipo de estudiantes del ITBA:
- Barbás Delfina
- Gastaminza Ámbar
- Lee Angulo Osmary
- López Antolin María
- Saldivia Ramiro

¡Gracias por probar GuardiánClima ITBA! 