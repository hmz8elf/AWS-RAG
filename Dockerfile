FROM python:3.11-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Torch CPU avant tout
RUN pip install torch==2.5.1+cpu \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    --no-cache-dir

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code source
COPY app/ ./app/
COPY config/ ./config/
COPY evaluation/ ./evaluation/
COPY indexes/ ./indexes/
COPY main.py .

# Variables d'environnement
ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["streamlit", "run", "main.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
