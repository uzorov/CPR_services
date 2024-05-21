import traceback
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.models.document import Document
from app.schemas.document import Document as DocumentSchema

logging.basicConfig()

class DocumentRepository:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())
    
    def _map_to_model(self, document: Document) -> DocumentSchema:
        result = DocumentSchema.from_orm(document)
        return result

    def _map_to_schema(self, document: DocumentSchema) -> Document:
        data = dict(document)
        result = Document(**data)
        return result

    def get_documents(self) -> List[DocumentSchema]:
        documents = []
        for d in self.db.query(Document).all():
            documents.append(self._map_to_model(d))
        return documents
    
    def get_document(self, id: int) -> DocumentSchema:
        document = self.db.query(Document).filter(Document.id == id).first()
        if document is None:
            raise KeyError
        return self._map_to_model(document)

    def create_document(self, document: DocumentSchema) -> DocumentSchema:
        try:
            db_document = self._map_to_schema(document)
            self.db.add(db_document)
            self.db.commit()
            return self._map_to_model(db_document)
        except:
            traceback.print_exc()
            raise KeyError
    
    def update_document(self, document: DocumentSchema) -> DocumentSchema:
        try:
            db_document = self.db.query(Document).filter(Document.id == document.id).first()
            db_document.file_id = document.file_id
            db_document.title = document.title
            db_document.body = document.body
            db_document.author_id = document.author_id
            db_document.responsible_employee_id = document.responsible_employee_id
            db_document.created_at = document.created_at
            self.db.commit()
            return self.db.query(Document).filter(Document.id == document.id).first()
        except:
            traceback.print_exc()
            raise KeyError
