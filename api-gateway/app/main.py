import logging
from enum import Enum

import os
from uuid import UUID

import httpx
from fastapi import FastAPI, Request, APIRouter, Depends, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.endpoints.auth_router import auth_router, require_role

logging.basicConfig()



app = FastAPI()

origins = [
    "*",
    "http://localhost:8081",
    "http://localhost:8080",
    "http://192.168.0.108",
    "http://100.94.251.56",
    "http://192.168.7.44"
]
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

DOCUMENT_SERVICE_URL = os.getenv('DOCUMENT_SERVICE_URL', '127.0.0.1:83')
TEXT_CORRECTION_SERVICE_URL = os.getenv('TEXT_CORRECTION_SERVICE_URL', '127.0.0.1:84')


document_processing_router = APIRouter(prefix='/documents-api', tags=['document'])
text_correction_router = APIRouter(prefix='', tags=['ai'])
#app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')
app.include_router(auth_router)

MICROSERVICES = {
    "document-processing-service": f"{DOCUMENT_SERVICE_URL}/documents-api",
    "text-correction-service": f"{TEXT_CORRECTION_SERVICE_URL}",
}


async def proxy_request(service_name: str, path: str, request: Request):
    
    auth_token = request.headers.get('Authorization')
     
    url = f"{MICROSERVICES[service_name]}{path}"
    logging.info("url: %s", url)
    timeout = 20
    try: 
        headers = {'Authorization': auth_token} if auth_token else {}
        # print("url>>>", request.method, url)
        
        async with httpx.AsyncClient() as client:
            if request.method == 'GET':
                response = await client.get(url, headers=headers, timeout=timeout)
            elif request.method == 'POST':
                content_type = request.headers.get('Content-Type', '')
                
                if 'multipart/form-data' in content_type:
                    # Обработка файла для multipart/form-data
                    form_data = {}
                    # Получаем все поля формы
                    form = await request.form()
                    # Получаем файлы из формы
                    files = {file_key: (file.filename, file.file, file.content_type)
                             for file_key, file in form.items() if hasattr(file, 'filename')}
                    # Добавляем другие поля формы
                    form_data.update({key: value for key, value in form.items() if key not in files})

                    response = await client.post(
                        url,
                        files=files,
                        data=form_data,
                        headers=headers,
                        timeout=timeout
                    )

                else:
                    json_data = await request.json()
                    response = await client.post(url, json=json_data, headers=headers, timeout=timeout)
            elif request.method == 'PUT':
                json_data = await request.json()
                response = await client.put(url, json=json_data, headers=headers, timeout=timeout)
            elif request.method == 'DELETE':
                response = await client.delete(url, headers=headers, timeout=timeout)
            # Определение типа содержимого
            content_type = response.headers.get('Content-Type', '')
            logging.debug("Content-Type: %s", content_type)
            
            if 'application/json' in content_type:
                # Обработка JSON-ответа
                return response.json()
            elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
                # Обработка ответа с документом Word
                return Response(content=response.content,
                                media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                headers={
                                    "Content-Disposition": f"attachment; filename*=UTF-8''{request.query_params.get('filename', 'document.docx')}"
                                })
            else:
                # Если тип содержимого не распознан, вернуть как текст
                logging.warning("Unexpected content type received: %s", content_type)
                return {"error": "Unexpected response format", "content": response.text}
    except httpx.HTTPStatusError as exc:
        logging.error(f"HTTP error occurred: {exc}")
        return {"error": str(exc), "status_code": exc.response.status_code}
    except httpx.RequestError as exc:
        logging.error(f"Request error occurred: {exc}")
        return {"error": str(exc)}
    except UnicodeDecodeError as exc:
        logging.error(f"Unicode decode error occurred: {exc}")
        return {"error": "Invalid response encoding"}


# Эндпоинты для коррекции текста

@text_correction_router.post("/correct-text", description="Коррекция текста с использованием искусственного интеллекта.")
async def correct_text_ai_powered(request: Request, user: dict = Depends(require_role(["supervisor"]))):
    result = await proxy_request(service_name="text-correction-service", path="/correct-text", request=request)
    return result

@text_correction_router.post("/transcribe-audio", description="Транскрибация аудио")
async def transcribe_audio(request: Request, user: dict = Depends(require_role(["supervisor"]))):
    result = await proxy_request(service_name="text-correction-service", path="/transcribe-audio", request=request)
    return result

app.include_router(text_correction_router)

# Эндпоинты для обработки документов
@document_processing_router.get('/', description="Получение всех документов.")
async def get_all_documents(request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path="/", request=request) 

@document_processing_router.get('/{document_id}', description="Получение конкретного документа.")
async def get_document(document_id: int, request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path=f"/{document_id}", request=request) 

@document_processing_router.post('/', description="Создание нового документа.")
async def create_document(request: Request, user: dict = Depends(require_role(["supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path="/", request=request)

@document_processing_router.put('/{document_id}', description="Обновление документа.")
async def update_document(document_id: int, request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path=f"/{document_id}", request=request)

@document_processing_router.delete('/{document_id}', description="Удаление документа.")
async def delete_document(document_id: int, request: Request, user: dict = Depends(require_role(["supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path=f"/{document_id}", request=request) 

@document_processing_router.get('/{document_id}/generate-word-document', description="Генерация документа Word.")
async def generate_word_document(document_id: int, request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path=f"/{document_id}/generate-word-document", request=request)

@document_processing_router.get('/assigned-tasks/{client_id}', description="Получение назначенных задач")
async def get_assigned_tasks(client_id: UUID ,request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path=f"/assigned-tasks/{client_id}", request=request) 

@document_processing_router.get('/created-tasks/{client_id}', description="Получение созданных задач")
async def get_created_tasks(client_id: UUID, request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return await proxy_request(service_name="document-processing-service", path=f"/created-tasks/{client_id}", request=request) 

app.include_router(document_processing_router)