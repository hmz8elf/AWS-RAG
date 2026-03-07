import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Chemins
    DATA_GLOBAL_PATH = "data/global"
    DATA_SERVICES_PATH = "data/services"
    INDEX_GLOBAL_PATH = "indexes/global"
    INDEX_SERVICES_PATH = "indexes/services"
    
    # Chunking
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 150
    
    # Retrieval
    TOP_K_GLOBAL = 4
    TOP_K_SERVICE = 6
    
    # AWS
    AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
    S3_BUCKET = os.getenv("S3_BUCKET_NAME")
    
    # API
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Services
    AVAILABLE_SERVICES = ["s3", "ec2", "lambda", "dynamodb", "kinesis"]

settings = Settings()

def get_llm():
    from langchain_groq import ChatGroq
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="mixtral-8x7b-32768"
    )

def get_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )