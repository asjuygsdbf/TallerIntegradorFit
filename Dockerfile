# Usa una imagen base con Python 3.10
FROM python:3.10-slim

# Evita prompts en install
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema necesarias para opencv-headless
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto estándar para Railway
EXPOSE 8080

# Comando para ejecutar el servidor con Gunicorn en el puerto 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
