import logging
from enum import Enum

import httpx
from fastapi import FastAPI, Request, APIRouter, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.endpoints.auth_router import auth_router, require_role

host_ip = "87.242.86.68"
auth_url = f"http://{host_ip}:8000/auth/login"

logging.basicConfig()



app = FastAPI()

origins = [
    "*",
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


# notification_router = APIRouter(prefix='/notification-api', tags=['notification'])
document_processing_router = APIRouter(prefix='/document-processing-api', tags=['document'])
text_correction_router = APIRouter(prefix='', tags=['ai'])
#app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')
app.include_router(auth_router)


MICROSERVICES = {
    "document-processing-service": f"http://{host_ip}:83/documents-api",
    "text-correction-service": f"http://{host_ip}:84",
}



class dropdownChoices(str, Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"

async def proxy_request(service_name: str, path: str, request: Request):
    url = f"{MICROSERVICES[service_name]}{path}"
    timeout = 20
    try:
        print("url>>>", request.method, url)
        
        async with httpx.AsyncClient() as client:
            if request.method == 'GET':
                response = await client.get(url, timeout=timeout)
            elif request.method == 'POST':
                json_data = await request.json()
                print("json_data>>>>", json_data)
                response = await client.post(url, json=json_data, timeout=timeout)
            elif request.method == 'PUT':
                json_data = await request.json()
                response = await client.put(url, json=json_data, timeout=timeout)
            elif request.method == 'DELETE':
                response = await client.delete(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        return {"error": str(exc), "status_code": exc.response.status_code}
    except httpx.RequestError as exc:
        return {"error": str(exc)}


# Эндпоинты для коррекции текста

@text_correction_router.post("/correct-text", description="Коррекция текста с использованием искусственного интеллекта.")
async def correct_text_ai_powered(request: Request, user: dict = Depends(require_role("supervisor"))):
    result = await proxy_request(service_name="text-correction-service", path="/correct-text", request=request)
    return result

@text_correction_router.post("/transcribe-audio", description="Транскрибация аудио")
async def transcribe_audio(request: Request, user: dict = Depends(require_role("supervisor"))):
    result = await proxy_request(service_name="text-correction-service", path="/transcribe-audio", request=request)
    return result

app.include_router(text_correction_router)

# Эндпоинты для обработки документов
@document_processing_router.get('/', description="Получение всех документов.")
def get_all_documents(request: Request, user: dict = Depends(require_role("employee"))):
    return proxy_request(service_name="document-processing-service", path="/", request=request) 

@document_processing_router.get('/{document_id}', description="Получение конкретного документа.")
def get_document(request: Request, user: dict = Depends(require_role("employee"))):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/", request=request) 

@document_processing_router.post('/', description="Создание нового документа.")
def create_document(request: Request, user: dict = Depends(require_role("supervisor"))):
    return proxy_request(service_name="document-processing-service", path="/", request=request)

@document_processing_router.put('/{document_id}', description="Обновление документа.")
def update_document(request: Request, user: dict = Depends(require_role("employee"))):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/", request=request)

@document_processing_router.delete('/{document_id}', description="Удаление документа.")
def delete_document(request: Request, user: dict = Depends(require_role("supervisor"))):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/", request=request) 

@document_processing_router.get('/{document_id}/generate-word-document', description="Генерация документа Word.")
def generate_word_document(request: Request, user: dict = Depends(require_role(["supervisor"]))):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/generate-word-document", request=request)

@document_processing_router.get('/assigned-tasks/{client_id}', description="Получение назначенных задач")
def get_assigned_tasks(request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return proxy_request(service_name="document-processing-service", path="/assigned-tasks/{client_id}", request=request) 

@document_processing_router.get('/created-tasks/{client_id}', description="Получение созданных задач")
def get_created_tasks(request: Request, user: dict = Depends(require_role(["employee", "supervisor"]))):
    return proxy_request(service_name="document-processing-service", path="/assigned-tasks/{client_id}", request=request) 

app.include_router(document_processing_router)

    
# @document_router.get('/assigned-tasks/{client_id}')
# def get_assigned_tasks(client_id: UUID, document_service: DocumentService = Depends()):
#     documents = document_service.get_documents_by_responsible_employee(client_id)
#     if not documents:
#         raise HTTPException(status_code=404, detail="No documents found for the given responsible employee ID")
#     return documents

# @document_router.get('/created-tasks/{client_id}')
# def get_created_tasks(client_id: UUID, document_service: DocumentService = Depends()):
#     documents = document_service.get_documents_by_author(client_id)
#     if not documents:
#         raise HTTPException(status_code=404, detail="No documents found for the given author ID")
#     return documents