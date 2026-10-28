FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install torch==2.5.1+cpu \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --no-cache-dir

RUN pip install fastapi uvicorn --no-cache-dir

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/index/ ./app/index/
COPY app/pipeline/ ./app/pipeline/
COPY app/__init__.py ./app/
COPY config/ ./config/
COPY indexes/ ./indexes/
COPY api.py .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]