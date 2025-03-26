from fastapi import FastAPI
from database import Base, engine
from routes import router

app = FastAPI()

# Crear las tablas
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/sensor_service")

@app.get("/")
def read_root():
    return {"message": "Sensor Service is running"}