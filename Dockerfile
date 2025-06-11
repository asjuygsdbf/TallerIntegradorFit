# Imagen base con Python 3.10
FROM python:3.10-slim

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias del sistema para opencv y mediapipe
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear y usar directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto 8080 (usado por Gunicorn en Railway)
EXPOSE 8080

# Comando para iniciar Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
