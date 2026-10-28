import os
from langchain_community.vectorstores import FAISS
from config.settings import get_embeddings

class IndexSingleton:
    instance = None
    embeddings = None
    indexCache = {}

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.embeddings = get_embeddings()
        return cls.instance

    def getEmbeddings(self):
        return self.embeddings

    def loadIndex(self, path):
        if path not in self.indexCache:
            faiss_file = os.path.join(path, "index.faiss")
            if not os.path.exists(faiss_file):
                raise FileNotFoundError(
                    f"Index introuvable : {faiss_file}\n"
                    f"Lance d'abord : python3 app/indexer.py"
                )
            self.indexCache[path] = FAISS.load_local(
                path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        return self.indexCache[path]

    def clearCache(self):
        self.indexCache.clear()
