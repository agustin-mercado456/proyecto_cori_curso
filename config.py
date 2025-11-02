# config.py

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la base de datos
DB_TYPE = os.getenv("DB_TYPE", "mysql")        # mysql o postgresql
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "mi_base")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Configuración de la aplicación
APP_TITLE = os.getenv("APP_TITLE", "Mi Aplicación")
APP_WIDTH = int(os.getenv("APP_WIDTH", 800))
APP_HEIGHT = int(os.getenv("APP_HEIGHT", 600))

# Construir la URL de conexión para SQLAlchemy
if DB_TYPE == "mysql":
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_TYPE == "postgresql":
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    raise ValueError(f"Tipo de base de datos no soportado: {DB_TYPE}")

