from langchain_community.vectorstores import FAISS
from app.index.indexSingleton import IndexSingleton
from config.settings import settings

class IndexFactory:

    _singleton = IndexSingleton()

    @staticmethod
    def create(service: str) -> FAISS:
        if service == "global":
            index_path = settings.INDEX_GLOBAL_PATH
        elif service in settings.AVAILABLE_SERVICES:
            index_path = f"{settings.INDEX_SERVICES_PATH}/{service}_index"
        else:
            index_path = settings.INDEX_GLOBAL_PATH

        return IndexFactory._singleton.loadIndex(index_path)

    @staticmethod
    def getEmbeddings():
        return IndexFactory._singleton.getEmbeddings()
    