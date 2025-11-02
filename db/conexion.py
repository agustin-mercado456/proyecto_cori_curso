from sqlalchemy import create_engine
from config import DATABASE_URL

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)  # echo=True para ver logs SQL
