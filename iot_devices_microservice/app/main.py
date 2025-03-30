from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Config
from app.api.v1.router import api_router
from app.db.session import engine, Base

if Config.ENVIRONMENT in ["development", "test"]:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IoT Devices API",
    description="API para gestionar dispositivos IoT en una mina subterránea",
    version="1.0.0",
    debug=Config.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": f"IoT Devices API is running in {Config.ENVIRONMENT} mode!"}
