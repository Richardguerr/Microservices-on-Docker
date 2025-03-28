from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import Config

if not Config.DATABASE_URL:
    raise ValueError("DATABASE_URL no está definido en las variables de entorno.")

engine = create_engine(Config.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        raise
    finally:
        db.close()
