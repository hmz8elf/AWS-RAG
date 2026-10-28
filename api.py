"""FastAPI backend exposing the RAG pipeline over HTTP.

Endpoints:
    POST /ask     {"question": "..."} -> {"answer": "..."}
    GET  /health  liveness check

This is the app served by the Docker image (uvicorn api:app, port 8000).
"""
from fastapi import FastAPI
from pydantic import BaseModel
from app.pipeline.pipeline import RAGPipeline
from config.settings import get_llm

app = FastAPI(title="AWS RAG Assistant API")

llm = get_llm()
pipeline = RAGPipeline(llm)

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    response = pipeline.run(q.question)
    return {"answer": response}

@app.get("/health")
def health():
    return {"status": "ok"}