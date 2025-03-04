import os
from dotenv import load_dotenv

# Cargar variables desde un archivo .env (opcional)
load_dotenv()

# Credenciales de AWS
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "eu-west-2")
S3_BUCKET = os.getenv("S3_BUCKET")

# Base de datos MySQL en AWS
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")