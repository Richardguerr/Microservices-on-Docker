from fastapi import FastAPI
from database import Base, engine
from routes import router

app = FastAPI()

# Crear las tablas
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/iot_devices")

@app.get("/")
def read_root():
    return {"message": "IoT Devices Service is running"}