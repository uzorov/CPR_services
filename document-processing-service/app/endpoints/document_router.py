from fastapi import APIRouter, Depends, HTTPException, Response
from urllib.parse import quote

from app.services.document_processing_service import DocumentService
from app.services.minio_files_management_service import MinioFilesManagementService
from app.schemas.document import DocumentCreate, DocumentUpdate, Document

document_router = APIRouter(prefix='/documents-api', tags=['Documents'])


@document_router.get('/')
def get_all_documents(document_service: DocumentService = Depends()):
    return document_service.get_documents()


@document_router.get('/{document_id}')
def get_document(document_id: int, document_service: DocumentService = Depends()):
    try:
        return document_service.get_document_by_id(document_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")


@document_router.post('/')
def create_document(document_data: DocumentCreate, document_service: DocumentService = Depends()):
    new_document = document_service.create_document(document_data)
    return new_document


@document_router.put('/{document_id}')
def update_document(document_id: int, document_data: DocumentUpdate, document_service: DocumentService = Depends()):
    try:
        updated_document = document_service.update_document(document_id, document_data)
        return updated_document
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")


@document_router.delete('/{document_id}')
def delete_document(document_id: int, document_service: DocumentService = Depends()):
    try:
        document_service.delete_document(document_id)
        return {"message": "Document deleted successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")


@document_router.get('/{document_id}/generate-word-document')
def generate_word_document(document_id: int, document_service: DocumentService = Depends(),
                           minio_service: MinioFilesManagementService = Depends()):
    try:
        res = document_service.generate_word_document_from_schema(document_id)

        minio_service.upload_file(res[0], f"{res[1]}")

        quoted_file_name = quote(res[1])

        return Response(content=res[0],
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_file_name}"
            })
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")


@document_router.post('/generate-word-document')
def generate_word_document_post(document_data: DocumentCreate, document_service: DocumentService = Depends(),
                           minio_service: MinioFilesManagementService = Depends()):
    try:
        new_document = document_service.create_document(document_data)
        res = document_service.generate_word_document_from_schema(new_document.id)

        minio_service.upload_file(res[0], f"{res[1]}")

        quoted_file_name = quote(res[1])

        return Response(content=res[0],
                        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_file_name}"
            })
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")