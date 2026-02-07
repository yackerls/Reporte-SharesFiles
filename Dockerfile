FROM python:3.9-slim

# Evitar basura de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalación limpia en una sola capa
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir streamlit pandas plotly \
    && find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' + \
    && rm -rf /var/lib/apt/lists/*

# Copiamos SOLO lo necesario
COPY app.py .
# Si tienes más archivos de código, agrégalos específicamente:
# COPY utils.py . 

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
