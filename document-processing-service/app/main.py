# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from fastapi import FastAPI
from fastapi import FastAPI, File, HTTPException
from fastapi.responses import FileResponse
import os

from starlette.middleware.cors import CORSMiddleware


from app.endpoints.document_router import document_router
from app.endpoints.minio_router import minio_router
from app.settings import settings

name = 'Сервис обработки документов'
app = FastAPI(title=name)
#
origins = [
    "*",
    "http://localhost:8080",
    "http://localhost:8081",
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

app.include_router(document_router, prefix='')
app.include_router(minio_router, prefix='')





