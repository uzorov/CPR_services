import logging
from enum import Enum

import httpx
from fastapi import FastAPI, Request, APIRouter
from starlette.middleware.sessions import SessionMiddleware

from app.endpoints.auth_router import auth_router

host_ip = "192.168.98.198"
auth_url = f"http://{host_ip}:8000/auth/login"

logging.basicConfig()



app = FastAPI()

notification_router = APIRouter(prefix='/notification-api', tags=['notification'])
document_processing_router = APIRouter(prefix='/document-processing-api', tags=['document'])
text_correction_router = APIRouter(prefix='/text-correction-api', tags=['correction'])
app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')
app.include_router(auth_router)


MICROSERVICES = {
    "document-processing-service": f"http://{host_ip}:82/documents-api",
    "notification-service": f"http://{host_ip}:80/api",
    "text-correction-service": f"http://{host_ip}:85/correction-api",
}



class dropdownChoices(str, Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"

def proxy_request(service_name: str, path: str, request: Request):
    url = f"{MICROSERVICES[service_name]}{path}"
    timeout = 20
    # headers = {
    #     'user': str(user_info)
    # }
    print(request.method)
    if request.method == 'GET':
        response = httpx.get(url, timeout=timeout).json()
    elif request.method == 'POST':
        response = httpx.post(url, timeout=timeout).json()
    elif request.method == 'PUT':
        response = httpx.put(url).json()
    elif request.method == 'DELETE':
        response = httpx.delete(url).json()
    return response


# Эндпоинты для коррекции текста
@text_correction_router.post("/correct-text-fast", description="Коррекция текста быстро.")
def correct_text_fast(request: Request):
    return proxy_request(service_name="text-correction-service", path="/correct-text-fas/", request=request) 

@text_correction_router.post("/correct-text-ai-powered", description="Коррекция текста с использованием искусственного интеллекта.")
def correct_text_ai_powered(request: Request):
    return proxy_request(service_name="text-correction-service", path="/correct-text-ai-powered/", request=request) 

@text_correction_router.post("/correct-text-long-ai-powered", description="Коррекция текста с использованием длительного процесса искусственного интеллекта.")
def correct_text_long_ai_powered(request: Request):
    return proxy_request(service_name="text-correction-service", path="/correct-text-long-ai-powered/", request=request) 

app.include_router(text_correction_router)

# Эндпоинты для обработки документов
@document_processing_router.get('/', description="Получение всех документов.")
def get_all_documents(request: Request):
    return proxy_request(service_name="document-processing-service", path="/", request=request) 

@document_processing_router.get('/{document_id}', description="Получение конкретного документа.")
def get_document(request: Request):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/", request=request) 

@document_processing_router.post('/', description="Создание нового документа.")
def create_document(request: Request):
    return proxy_request(service_name="document-processing-service", path="/", request=request)

@document_processing_router.put('/{document_id}', description="Обновление документа.")
def update_document(request: Request):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/", request=request)

@document_processing_router.delete('/{document_id}', description="Удаление документа.")
def delete_document(request: Request):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/", request=request) 

@document_processing_router.get('/{document_id}/generate-word-document', description="Генерация документа Word.")
def generate_word_document(request: Request):
    return proxy_request(service_name="document-processing-service", path="/{document_id}/", request=request)

app.include_router(document_processing_router)

# Эндпоинт для отправки электронной почты
@notification_router.post('/Email/send', description="Отправка электронной почты.")
def send_email(request: Request):
    return proxy_request(service_name="notification-service", path="/Email/send/", request=request)      

app.include_router(notification_router)