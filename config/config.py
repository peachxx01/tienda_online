from dotenv import load_dotenv
import os

load_dotenv()

user= os.getenv('MYSQL_USER')
password=os.getenv('MYSQL_PASSWORD')
host=os.getenv('MYSQL_HOST')
database=os.getenv('MYSQL_DB')

DATABASE_CONNECTION_URI=f"mysql+pymysql://{user}:{password}@{host}/{database}"

MAX_CONTENT_LENGTH= 2*1024*1024 #2MB Máximo, va al handler de app

SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY")
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")

BASE_URL = os.getenv("BASE_URL")