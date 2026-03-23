# GitHub Function Name Analyzer

Sistema distribuido simple para analizar repositorios públicos de GitHub y extraer las palabras más frecuentes utilizadas en nombres de funciones y métodos en Python y Java.

---

## Tabla de Contenidos

* [Descripción](#descripción)
* [Arquitectura](#arquitectura)
* [Tecnologías](#tecnologías)
* [Estructura del Proyecto](#estructura-del-proyecto)
* [Cómo Ejecutar](#cómo-ejecutar)
* [Configuración](#configuración)
* [Uso](#uso)
* [Detalles Técnicos](#detalles-técnicos)
* [Manejo de Errores](#manejo-de-errores)
* [Limitaciones](#limitaciones)
* [Mejoras Futuras](#mejoras-futuras)

---

## Descripción

Este proyecto implementa un sistema basado en el patrón **productor–consumidor** para analizar código fuente de GitHub.

* El **Miner** actúa como productor: obtiene repositorios, extrae funciones y envía datos.
* El **Visualizer** actúa como consumidor: recibe datos, los procesa y muestra resultados.

El objetivo es identificar las palabras más utilizadas en nombres de funciones y métodos, respetando convenciones de escritura como `snake_case` y `camelCase`.

---

## Arquitectura

```
GitHub API
     ↓
   Miner  ─────HTTP─────▶  Visualizer
     ↓                       ↓
 extracción              conteo y ranking
```

### Características clave

* Comunicación vía HTTP
* Procesamiento continuo (simulación de streaming)
* Servicios desacoplados
* Contenedorización con Docker

---

## Tecnologías

* Python 3.11
* Flask (servidor web ligero)
* Requests (cliente HTTP)
* Docker
* Docker Compose

---

## Estructura del Proyecto

```
project/
│
├── miner/
│   ├── miner.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── visualizer/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## Cómo Ejecutar

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd project
```

### 2. Ejecutar con Docker Compose

```bash
docker-compose up --build
```

### 3. Acceder a resultados

* Consola: muestra el ranking en tiempo real
* API:

```bash
http://localhost:5000/top
```

---

## Configuración

Variables de entorno disponibles:

| Variable       | Descripción                     | Default  |
| -------------- | ------------------------------- | -------- |
| TOP_N          | Número de palabras a mostrar    | 10       |
| VISUALIZER_URL | Endpoint del consumidor         | interno  |
| GITHUB_TOKEN   | Token para evitar rate limiting | opcional |

### Uso de GitHub Token

Para evitar límites de la API:
1. Crear token en GitHub
2. Agregar en `docker-compose.yml`:

```yaml
- GITHUB_TOKEN=tu_token
```

---

## Uso

El sistema comienza automáticamente:

1. Miner consulta repositorios populares
2. Extrae funciones/métodos
3. Divide nombres en palabras
4. Envía datos al Visualizer
5. Visualizer actualiza conteo

### Ejemplo de salida

```
Top palabras:
get: 120
set: 95
data: 80
user: 65
```

---

## Detalles Técnicos

### Extracción de funciones

* Python: uso de expresiones regulares sobre `def`
* Java: detección de métodos mediante patrones de visibilidad

### Procesamiento de nombres

* `snake_case` → separación por `_`
* `camelCase` → separación por mayúsculas

### Comunicación

* Protocolo: HTTP
* Formato: JSON

Ejemplo de payload:

```json
{
  "words": ["get", "user", "data"]
}
```

### Procesamiento continuo

Se implementa mediante un bucle infinito con pausas (`sleep`), simulando un flujo de datos en tiempo real.

---

## Manejo de Errores

El sistema incluye manejo básico de errores:

* Fallos en requests HTTP
* Archivos no válidos
* Problemas de red

Estrategia:

* Uso de `try/except`
* Logs en consola
* Continuación del procesamiento

---

## Limitaciones

* Uso de expresiones regulares en lugar de parsing completo (AST)
* Procesamiento secuencial (no paralelo)
* No hay persistencia de datos
* Dependencia de la API de GitHub

---

## Mejoras Futuras

* Integración con cola de mensajes (Kafka / RabbitMQ)
* Persistencia en base de datos
* Interfaz web interactiva
* Procesamiento paralelo
* Uso de AST para mayor precisión
* Filtros por tipo de repositorio

---

