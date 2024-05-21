from minio import Minio
from minio.error import S3Error
from fastapi import Depends, HTTPException
from uuid import UUID
from app.repos.document_repo import DocumentRepository as DocumentRepo
from app.schemas.document import Document
import io
from pathlib import Path
import os
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

print(f"Current working directory: {os.getcwd()}")
print(f"Is .env file present: {os.path.isfile(env_path)}")
print(f"env_path: {env_path}")


print("AAAAAAAAAAAAAAAAAAAA" + os.getenv("MINIO_URL"))

minio_client = Minio(
    os.getenv("MINIO_URL"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)
bucket_name = "files"

class MinioFilesManagementService:
    def __init__(self, document_repo: DocumentRepo = Depends(DocumentRepo)) -> None:
        self.document_repo = document_repo




        # Ensure the bucket exists
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

    def upload_file(self, file_data: bytes, file_name: str) -> str:
        try:
            file_stream = io.BytesIO(file_data)
            self.client.put_object(
                self.bucket_name, file_name, file_stream, len(file_data)
            )
            return file_name
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload file: {e}")

    def get_file(self, file_name: str) -> bytes:
        try:
            response = minio_client.get_object(bucket_name, file_name)
            file_data = response.read()
            response.close()
            response.release_conn()
            return file_data
        except S3Error as e:
            raise HTTPException(status_code=404, detail=f"File not found: {e}")

    def get_document_by_id(self, document_id: int) -> Document:
        document = self.document_repo.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document

    def upload_document_file(self, document_id: int, file_data: bytes, file_name: str) -> str:
        document = self.document_repo.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Upload file to MinIO
        file_key = self.upload_file(file_data, file_name)
        # Update document record with the file key or any other relevant info
        document.file_ids.append(file_key)
        self.document_repo.update_document(document)

        return file_key

    def download_document_file(self, document_id: int):
        document = self.get_document_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Retrieve file from MinIO
        file_data = self.get_file(document.file_id)

        return file_data, document.title

