from fastapi import APIRouter, Depends, HTTPException
from app.services.document_processing_service import DocumentService
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
def generate_word_document(document_id: int, document_service: DocumentService = Depends()):
    try:
        return document_service.generate_word_document_from_schema(document_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")
