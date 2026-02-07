# Usamos una versión específica para mayor estabilidad en infraestructura
FROM python:3.9-slim

# Evita que Python genere archivos .pyc y que el buffer se llene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias primero para aprovechar el caché de Docker
# Se agregan dependencias mínimas de sistema para que pandas y plotly funcionen bien
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir streamlit pandas plotly \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el resto del proyecto
COPY . .

EXPOSE 8501

# Salud del contenedor (opcional pero recomendado en Portainer)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
