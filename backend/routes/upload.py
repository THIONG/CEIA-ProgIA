from fastapi import APIRouter, File, UploadFile
from backend.services import upload_to_s3, analyze_image_s3, save_to_db

router = APIRouter()

@router.post("/")
def upload_image(file: UploadFile = File(...)):
    image_url = upload_to_s3(file)
    rekognition_response = analyze_image_s3(image_url)
    save_to_db(image_url, rekognition_response)
    return {"image_url": image_url, "rekognition_data": rekognition_response}