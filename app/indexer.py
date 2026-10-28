import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from config.settings import settings
from app.index.indexSingleton import IndexSingleton

singleton = IndexSingleton()
embeddings = singleton.getEmbeddings()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " "]
)

def buildIndex(pdf_path: str, index_path: str):
    
    print("\n Chargement : ",pdf_path)

    if not os.path.exists(pdf_path):
        print("PDF introuvable : ", pdf_path," skipping...")
        return None
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"{len(docs)} pages chargées")

    chunks = splitter.split_documents(docs)
    print(f"{len(chunks)} chunks créés")

    db = FAISS.from_documents(chunks, embeddings)

    os.makedirs(index_path, exist_ok=True)
    db.save_local(index_path)
    print(f"Index sauvegardé : {index_path}")

    return db

def buildAllIndexes():
    print("Construction des index FAISS\n")
    print(f"   Chunk size    : {settings.CHUNK_SIZE} tokens")
    print(f"   Chunk overlap : {settings.CHUNK_OVERLAP} tokens")
    print(f"   Services      : {settings.AVAILABLE_SERVICES}\n")

    buildIndex(
        f"{settings.DATA_GLOBAL_PATH}/aws-overview.pdf",
        settings.INDEX_GLOBAL_PATH
    )

    for service in settings.AVAILABLE_SERVICES:
        pdf_path = f"{settings.DATA_SERVICES_PATH}/{service}.pdf"
        index_path = f"{settings.INDEX_SERVICES_PATH}/{service}_index"
        buildIndex(pdf_path, index_path)

    print("\n Construction terminée !")



if __name__ == "__main__":
    buildAllIndexes()