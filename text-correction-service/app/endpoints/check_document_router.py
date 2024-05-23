from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, ConfigDict
from fastapi.staticfiles import StaticFiles

from app.services.check_document_service import CheckDocumentService

router = APIRouter(prefix="/corrections-api", tags=["Corrections"])

router.mount("/", StaticFiles(directory="static"), name="static")

class TextInput(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    text: str

@router.post("/correct-text-fast")
def correct_text_fast(data: TextInput, check_document_service: CheckDocumentService = Depends()):
    return check_document_service.correct_text_using_algorithm(data.text)


@router.post("/correct-text-ai-powered")
def correct_text_ai_powered(data: TextInput, check_document_service: CheckDocumentService = Depends()):
    return check_document_service.correct_text_using_ai_fast(data.text)


@router.post("/correct-text-long-ai-powered")
def correct_text_long_ai_powered(data: TextInput, check_document_service: CheckDocumentService = Depends()):
    return check_document_service.correct_text_using_ai_long(data.text)
