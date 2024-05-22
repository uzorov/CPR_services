
from fastapi import FastAPI

from app.endpoints.check_document_router import router
from app.services.check_document_service import CheckDocumentService
from starlette.middleware.cors import CORSMiddleware
name = 'Сервис проверки текстов'

app = FastAPI(title=name)


# @app.on_event('startup')
# def startup():
#     loop = asyncio.get_event_loop()
#     asyncio.ensure_future(rabbitmq.consume(loop))


origins = [
     "*",
    "http://localhost",
    "http://localhost:8080",
 ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(router, prefix='')

