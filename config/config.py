import os

# Leemos directamente de Railway (sin guiones bajos)
user = os.getenv('MYSQLUSER')      
password = os.getenv('MYSQLPASSWORD') 
host = os.getenv('MYSQLHOST')      
database = os.getenv('MYSQLDATABASE')    
port_db = os.getenv('MYSQLPORT', '3306') 

# Si alguna variable falta, usamos valores por defecto para que no sea 'None'
if not host:
    host = "localhost" # Esto es solo para que no explote si no hay host

# Construcción de la URI
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port_db}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_CONTENT_LENGTH = 2 * 1024 * 1024 

# Nombres exactos de tus variables en Railway
SECRET_KEY = os.getenv("SECRETKEY") 
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
BASE_URL = os.getenv("BASE_URL")