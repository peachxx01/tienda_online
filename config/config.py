import os

user = os.environ.get('MYSQLUSER')
password = os.environ.get('MYSQLPASSWORD')
host = os.environ.get('MYSQLHOST')
database = os.environ.get('MYSQLDATABASE')
port_db = os.environ.get('MYSQLPORT')

# Construcción de la URI
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port_db}/{database}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAX_CONTENT_LENGTH = 2 * 1024 * 1024
SECRET_KEY = os.environ.get("SECRETKEY")
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN")
BASE_URL = os.environ.get("BASE_URL")

CLOUD_NAME = os.environ.get("CLOUD_NAME")
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")