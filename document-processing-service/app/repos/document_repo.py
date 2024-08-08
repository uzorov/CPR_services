import traceback
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.models.document import Document
from app.schemas.document import Document as DocumentSchema

from contextlib import contextmanager


logging.basicConfig()

class DocumentRepository:
    def _map_to_model(self, document: Document) -> DocumentSchema:
        result = DocumentSchema.from_orm(document)
        return result

    def _map_to_schema(self, document: DocumentSchema) -> Document:
        data = dict(document)
        result = Document(**data)
        return result

    def get_documents(self) -> List[DocumentSchema]:
        with get_db() as db:  # Используем контекстный менеджер
            documents = []
            for d in db.query(Document).all():
                documents.append(self._map_to_model(d))
            return documents

    def get_document(self, id: int) -> DocumentSchema:
        with get_db() as db:  # Используем контекстный менеджер
            document = db.query(Document).filter(Document.id == id).first()
            if document is None:
                raise KeyError
            return self._map_to_model(document)

    def create_document(self, document: DocumentSchema) -> DocumentSchema:
        with get_db() as db:  # Используем контекстный менеджер
            try:
                db_document = self._map_to_schema(document)
                db.add(db_document)
                db.commit()
                return self._map_to_model(db_document)
            except:
                traceback.print_exc()
                raise KeyError

    def delete_document(self, document_id: int) -> None:
        with get_db() as db:  # Используем контекстный менеджер
            try:
                db_document = db.query(Document).filter(Document.id == document_id).first()
                if db_document:
                    db.delete(db_document)
                    db.commit()
                else:
                    raise KeyError(f"Document with id {document_id} not found")
            except Exception as e:
                logging.error(f"Error deleting document: {e}")
                raise

    def update_document(self, id: int, document: DocumentSchema) -> DocumentSchema:
        with get_db() as db:  # Используем контекстный менеджер
            try:
                db_document = db.query(Document).filter(Document.id == id).first()
                db_document.file_id = document.file_id
                db_document.subject = document.subject
                db_document.description = document.description
                db_document.status = document.status
                db_document.priority = document.priority
                db_document.author_id = document.author_id
                db_document.responsible_employee_id = document.responsible_employee_id
                db_document.registration_date = document.registration_date
                db.commit()
                return db.query(Document).filter(Document.id == id).first()
            except:
                traceback.print_exc()
                raise KeyError
