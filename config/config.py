import os

# Forzamos la obtención de las variables
user = os.environ.get('MYSQLUSER')      
password = os.environ.get('MYSQLPASSWORD') 
host = os.environ.get('MYSQLHOST')      
database = os.environ.get('MYSQLDATABASE')    
port_db = os.environ.get('MYSQLPORT', '3306') 

# DEBUG: Esto nos dirá en el log de Railway si las variables están llegando
if not host:
    print("--- ERROR: NO SE ENCONTRÓ MYSQLHOST EN LAS VARIABLES ---")
else:
    print(f"--- CONECTANDO A HOST: {host} ---")

# Construcción de la URI
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port_db}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_CONTENT_LENGTH = 2 * 1024 * 1024 

SECRET_KEY = os.environ.get("SECRETKEY") 
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN")
BASE_URL = os.environ.get("BASE_URL")