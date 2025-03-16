# Imagen base de Python
FROM python:3.9

# Actualizar el sistema e instalar herramientas de red necesarias
RUN apt update && apt install -y \
    iputils-ping \
    netcat-openbsd \
    telnet \
    mosquitto-clients && \
    rm -rf /var/lib/apt/lists/*

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . .

# Instalar dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
