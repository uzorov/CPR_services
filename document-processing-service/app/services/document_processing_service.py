import uuid
import logging
from docxtpl import DocxTemplate
import re
import io
import httpx
import os
from docx import Document as WordDocument
import json
from uuid import UUID
from fastapi import Depends, HTTPException, Response
from typing import List, Optional

from app.repos.document_repo import DocumentRepository as DocumentRepo
from app.schemas.document import Document
from app.services.minio_files_management_service import MinioFilesManagementService

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

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


    async def generate_word_document_from_schema(self, id: int, auth_header: str):
        document = self.document_repo.get_document(id)
        word_file = await self.document_handler(document, auth_header)

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

    async def _get_user_by_id(self, user_id: UUID, auth_header: str) -> Optional[str]:
        
        host_ip = os.getenv('HOST_IP', '127.0.0.1');
        gateway_port = os.getenv('GATEWAY_PORT', '81')
        url = f"http://{host_ip}:{gateway_port}/auth/user/{user_id}"
        
        headers = {'Authorization': auth_header}
        
        logger.info(f"Authorization Header: {auth_header}")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()  # Поднимет исключение для кодов 4xx/5xx
                
                user_data = response.json()
                # Предполагаем, что имя пользователя находится в поле "name"
                name = user_data.get('name')
                return name
            
            except httpx.HTTPStatusError as exc:
                # Логируем или обрабатываем ошибку по вашему усмотрению
                print(f"HTTP error occurred: {exc}")
                return None
            except httpx.RequestError as exc:
                # Логируем или обрабатываем ошибку по вашему усмотрению
                print(f"Request error occurred: {exc}")
                return None


    async def document_handler(self, document: Document, auth_header: str) -> bytes:
        # Получение данных пользователя
        
        
        author_name = await self._get_user_by_id(document.author_id, auth_header)
        responsible_name = await self._get_user_by_id(document.responsible_employee_id, auth_header)

        # Настройка данных для вставки в шаблон
        config = {
            'task_message': document.description,
            'subject': document.subject,
            'owner_name': author_name,
            'initiator_name': responsible_name,
            'status': document.status,
            'priority': document.priority,
            'registration_date': document.registration_date.strftime('%Y.%m.%d'),
        }

        # Загрузка шаблона и рендеринг данных
        doc_pattern = DocxTemplate("app/services/report_maket.docx")
        doc_pattern.render(config)

        # Создание потока байтов для сохранения документа
        file_stream = io.BytesIO()
        doc_pattern.save(file_stream)
        file_stream.seek(0)  # Перемещение в начало потока

        return file_stream.getvalue()
    

