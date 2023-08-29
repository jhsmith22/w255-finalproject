import logging
import os

from fastapi import FastAPI, HTTPException, Request, Response
from typing import List, Dict
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from pydantic import BaseModel, Extra, ValidationError, validator
from redis import asyncio

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    return_all_scores=True,
)

logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://redis:6379"
app = FastAPI()

@app.on_event("startup")
def startup():
    HOST_URL = os.environ.get("REDIS_URL", LOCAL_REDIS_URL)
    logger.debug(HOST_URL)
    redis = asyncio.from_url(HOST_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
class SentimentRequest(BaseModel, extra=Extra.forbid):
    text: List[str]

class Sentiment(BaseModel):
    label: str
    score: float

class SentimentResponse(BaseModel):
    predictions: list[list[Sentiment]]

@app.post("/predict", response_model=SentimentResponse)
def predict(sentiments: SentimentRequest):
    return {"predictions": classifier(sentiments.text)}

@app.get("/health")
async def health():
    return {"status": "healthy"}