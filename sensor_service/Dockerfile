# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY ./app .

# Exponer el puerto en el que corre FastAPI
EXPOSE 8001

# Comando para iniciar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
