# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Establecer el PYTHONPATH para que Python encuentre el módulo 'app'
ENV PYTHONPATH=/app

# Copiar los archivos de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY ./app /app

# Exponer el puerto en el que corre FastAPI
EXPOSE 8001

# Comando para iniciar FastAPI con Uvicorn
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
CMD ["uvicorn", "--app-dir", "/app", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
