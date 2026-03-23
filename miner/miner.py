import requests
import re
import time
import os

GITHUB_API = "https://api.github.com"
VISUALIZER_URL = os.getenv("VISUALIZER_URL", "http://visualizer:5000/words")

HEADERS = {
    "Accept": "application/vnd.github+json"
}

# Token opcional para evitar rate limit
if "GITHUB_TOKEN" in os.environ:
    HEADERS["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


# -----------------------------------------
# Obtiene repositorios populares de un lenguaje específico,
# ordenados por número de estrellas.
# -----------------------------------------
def get_repositories(language):
    url = f"{GITHUB_API}/search/repositories?q=language:{language}&sort=stars&per_page=5"
    response = requests.get(url, headers=HEADERS)
    # Retorna la lista de repositorios o lista vacía si no hay resultados
    return response.json().get("items", [])


# -----------------------------------------
# Extrae nombres de funciones en Python usando regex
# Busca patrones tipo: def nombre_funcion(...)
# -----------------------------------------
def get_python_functions(code):
    return re.findall(r'def\s+(\w+)', code)


# -----------------------------------------
# Extrae nombres de métodos en Java usando regex.
# Considera modificadores opcionales como public/private/protected.
# -----------------------------------------
def get_java_methods(code):
    return re.findall(r'(?:public|private|protected)?\s+\w+\s+(\w+)\s*\(', code)


# -----------------------------------------
# Divide un nombre de función en palabras individuales.
#    Soporta:
#    - snake_case → separación por "_"
#    - camelCase → separación por mayúsculas
# -----------------------------------------
def split_words(name):
    # snake_case
    words = name.split("_")
    # camelCase
    final_words = []
    for word in words:
        split = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', word)
        final_words.extend(split)
    # Normaliza todo a minúsculas
    return [w.lower() for w in final_words if w]


# -----------------------------------------
#    Procesa un repositorio:
#    - Obtiene sus archivos
#    - Filtra por lenguaje
#    - Envía cada archivo a procesamiento
# -----------------------------------------
def process_repo(repo, language):
    # URL para listar contenido del repositorio
    contents_url = repo["contents_url"].replace("{+path}", "")
    response = requests.get(contents_url, headers=HEADERS)

    for file in response.json():
        # Ignora directorios u otros tipos
        if file["type"] != "file":
            continue
        # Filtra archivos Python
        if language == "Python" and file["name"].endswith(".py"):
            process_file(file["download_url"], get_python_functions)
        # Filtra archivos Java
        elif language == "Java" and file["name"].endswith(".java"):
            process_file(file["download_url"], get_java_methods)


# -----------------------------------------
# Procesa un archivo individual:
#    - Descarga el contenido
#    - Extrae nombres de funciones/métodos
#    - Divide en palabras
#    - Envía resultados al Visualizer
# -----------------------------------------
def process_file(url, extractor):
    try:
        # Descarga el código fuente
        code = requests.get(url).text
        # Extrae nombres usando la función correspondiente
        names = extractor(code)

        words = []
        for name in names:
            words.extend(split_words(name))
        # Envía solo si hay datos
        if words:
            send_words(words)

    except Exception as e:
        print("Error procesando archivo:", e)


# -----------------------------------------
# Envía las palabras al Visualizer mediante HTTP POST.
# -----------------------------------------
def send_words(words):
    try:
        requests.post(VISUALIZER_URL, json={"words": words})
    except Exception as e:
        print("Error enviando datos:", e)


# -----------------------------------------
# Loop principal del Miner.
# Ejecuta continuamente el flujo completo (simulación de streaming).
# -----------------------------------------
def main():
    while True:
        print("Miner ejecutándose...")

        for lang in ["Python", "Java"]:
            repos = get_repositories(lang)

            for repo in repos:
                process_repo(repo, lang)

        time.sleep(10)  # simula streaming continuo


if __name__ == "__main__":
    main()