from flask import Flask, request, jsonify
from collections import Counter
import threading
import time
import os

app = Flask(__name__)

# Estructura para almacenar el conteo de palabras
word_counter = Counter()
# Número de palabras a mostrar en el ranking (configurable por variable de entorno)
TOP_N = int(os.getenv("TOP_N", 10))


@app.route("/words", methods=["POST"])
def receive_words():
    """
    Endpoint que recibe palabras desde el Miner.
    - Espera un JSON con formato: { "words": [...] }
    - Actualiza el contador global de palabras
    """
    data = request.json
    # Obtiene lista de palabras o lista vacía si no existe
    words = data.get("words", [])
    # Actualiza el contador acumulativo
    word_counter.update(words)
    return jsonify({"status": "ok"})


@app.route("/top", methods=["GET"])
def get_top():
    """
    Endpoint que retorna el ranking de palabras más frecuentes.
    - Usa Counter.most_common() para obtener el Top-N
    """
    return jsonify(word_counter.most_common(TOP_N))


def print_top():
    """
    Función que imprime periódicamente el ranking en consola.
    Se ejecuta en un hilo separado para no bloquear el servidor Flask.
    """
    while True:
        # Intervalo de actualización (simula visualización en tiempo real)
        time.sleep(5)
        print("\nTop palabras:")
        for word, count in word_counter.most_common(TOP_N):
            print(f"{word}: {count}")


if __name__ == "__main__":
    """
    Punto de entrada del servicio.
    - Inicia un hilo en segundo plano para imprimir resultados
    - Levanta el servidor HTTP con Flask
    """
    # Hilo daemon: se cierra automáticamente cuando el programa termina
    thread = threading.Thread(target=print_top, daemon=True)
    thread.start()
    # Servidor accesible desde otros contenedores (Docker)
    app.run(host="0.0.0.0", port=5000)