import boto3
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

# AWS S3 Configurations
MEDIA_S3_BUCKET = "kushal-media"
AWS_DEFAULT_REGION = "ap-south-1"

# Establish connection with AWS S3
s3_client = boto3.client("s3", region_name=AWS_DEFAULT_REGION)


@router.post("/upload", tags=["S3"])
async def upload_file(file: UploadFile = File(...)):
    try:
        # Upload file to S3
        s3_client.upload_fileobj(file.file, MEDIA_S3_BUCKET, file.filename)
        # Generate URL for uploaded file
        url = f"https://{MEDIA_S3_BUCKET}.s3.{AWS_DEFAULT_REGION}.amazonaws.com/{file.filename}"
        return JSONResponse(content={"url": url}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
