from fastapi import APIRouter, Depends, HTTPException, Response
from uuid import UUID
from app.services.minio_files_management_service import MinioFilesManagementService
from urllib.parse import quote

minio_router = APIRouter(prefix='/minio-api', tags=['MinIO'])


@minio_router.get('/minio/{document_id}')
def download_file(document_id: int, minio_service: MinioFilesManagementService = Depends()):
    try:

        file_data, file_name = minio_service.download_document_file(document_id)
        quoted_file_name = quote(file_name)
        return Response(content=file_data,
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_file_name}"
            })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
