from dotenv import load_dotenv
import os

load_dotenv()

# Nombres exactos según tu lista de Railway
user = os.getenv('MYSQLUSER')      
password = os.getenv('MYSQLPASSWORD') 
host = os.getenv('MYSQLHOST')      
database = os.getenv('MYSQLDATABASE')    
port = os.getenv('MYSQLPORT', '3306') 

# Construcción de la URI
DATABASE_CONNECTION_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

MAX_CONTENT_LENGTH = 2 * 1024 * 1024 

SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
BASE_URL = os.getenv("BASE_URL")