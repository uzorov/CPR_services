import uuid
from docxtpl import DocxTemplate
import re
import io
from docx import Document as WordDocument
import json
from uuid import UUID
from fastapi import Depends, HTTPException, Response
from typing import List

from app.repos.document_repo import DocumentRepository as DocumentRepo
from app.schemas.document import Document
from app.services.minio_files_management_service import MinioFilesManagementService


class DocumentService:
    document_repo: DocumentRepo

    def __init__(self, document_repo: DocumentRepo = Depends(DocumentRepo)) -> None:
        self.document_repo = document_repo

    def get_documents(self) -> List[Document]:
        return self.document_repo.get_documents()

    def get_document_by_id(self, id: int) -> Document:
        return self.document_repo.get_document(id)

    def create_document(self, document: Document) -> Document:
        return self.document_repo.create_document(document)

    def update_document(self, id: int, document: Document) -> Document:
        return self.document_repo.update_document(id, document)

    def delete_document(self, id: int) -> None:
        self.document_repo.delete_document(id)


    def generate_word_document_from_schema(self, id: int):
        document = self.document_repo.get_document(id)
        word_file = self.document_handler(document)

        file_id = uuid.uuid4()

        document.file_id = f"{file_id}.docx"
    
        self.document_repo.update_document(document.id, document)
        return word_file, document.file_id
    
    def get_documents_by_responsible_employee(self, employee_id: UUID) -> List[Document]:
        # Логика для получения документов по responsible_employee_id
        documents = [doc for doc in self.get_documents() if doc.responsible_employee_id == employee_id]
        return documents

    def get_documents_by_author(self, author_id: UUID) -> List[Document]:
        # Логика для получения документов по author_id
        documents = [doc for doc in self.get_documents() if doc.author_id == author_id]
        return documents



    def document_handler(self, document: Document) -> bytes:
        # toDo: Добавить метод get_user_by_id. Получить имя/должность для author_id, responsible_employee_id
        config = {
            'task_message': document.description
        }

        print("1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVV")
        doc_pattern = DocxTemplate("app/services/report_maket.docx")

        doc_pattern.render(config)

        # Create an in-memory bytes buffer
        file_stream = io.BytesIO()
        doc_pattern.save(file_stream)
        file_stream.seek(0)  # Move to the beginning of the BytesIO buffer

        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAVV", file_stream.getvalue())

        return file_stream.getvalue()


# def generate_word_document_from_schema(self, document: Document) -> str:
#     #get_report_file(get_report_attributes("report_maket.docx"), data)
#     return WordDocument(f'{document.title}.docx')
