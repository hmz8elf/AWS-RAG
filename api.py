from fastapi import FastAPI
from pydantic import BaseModel
from app.pipeline.pipeline import RAGPipeline
from config.settings import get_llm

app = FastAPI()
pipeline = RAGPipeline(get_llm())

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    response = pipeline.run(q.question)
    return {"answer": response}

@app.get("/health")
def health():
    return {"status": "ok"}