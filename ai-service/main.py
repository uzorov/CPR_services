import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import io
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

name = 'Сервис работы с ИИ'

app = FastAPI(title=name)


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

logger.info("Загрузка модели коррекции текста начинается...")

tokenizer = AutoTokenizer.from_pretrained("ai-forever/sage-fredt5-distilled-95m")
model = AutoModelForSeq2SeqLM.from_pretrained("ai-forever/sage-fredt5-distilled-95m")

model.to("cpu")

logger.info("Модель загружена")


class TextCorrectionRequest(BaseModel):
    text: str
    
@app.post("/correct-text")
async def correct_text(request: TextCorrectionRequest):

    input_text = request.text

    inputs = tokenizer(input_text, max_length=None, padding="longest", truncation=False, return_tensors="pt")

    outputs = model.generate(**inputs.to(model.device), max_length = inputs["input_ids"].size(1) * 1.5)

    corrected_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    return {"corrected_text": corrected_text}


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Сохранение загруженного аудиофайла во временный файл
        temp_file_path = "/tmp/temp_audio_file"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Запрос к внешнему API для распознавания речи
        result = query(temp_file_path)
        transcription = result.get("text", "")

        return {"transcription": transcription}
    except Exception as e:
        logger.error(f"Ошибка при обработке аудио: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при обработке аудио")



