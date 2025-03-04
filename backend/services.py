import boto3
import pymysql
import uuid
from fastapi import UploadFile, HTTPException
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION, S3_BUCKET, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

# Configuración de AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Configuración de AWS Rekognition
rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Subir imagen a S3
def upload_to_s3(file: UploadFile):
    file_extension = file.filename.split('.')[-1]
    s3_filename = f"images/{uuid.uuid4()}.{file_extension}"
    try:
        s3_client.upload_fileobj(file.file, S3_BUCKET, s3_filename)
        return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen a S3: {str(e)}")

# Analizar imagen con Rekognition
def analyze_image_s3(image_url: str):
    try:
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': S3_BUCKET, 'Name': image_url.split(f"s3.{AWS_REGION}.amazonaws.com/")[1]}},
            MaxLabels=10,
            MinConfidence=75
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Rekognition: {str(e)}")

# Guardar datos en la base de datos
def save_to_db(image_url: str, labels: dict):
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        cursor = connection.cursor()

        # Insertar la imagen y obtener su ID
        cursor.execute("INSERT INTO images (url) VALUES (%s)", (image_url,))
        image_id = cursor.lastrowid  

        # Insertar etiquetas relacionadas con la imagen
        for label in labels["Labels"]:
            cursor.execute("INSERT INTO labels (image_id, label) VALUES (%s, %s)", (image_id, label["Name"]))

        connection.commit()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {str(e)}")
