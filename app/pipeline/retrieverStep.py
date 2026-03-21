from app.pipeline.baseStep import BaseStep
from app.index.indexFactory import IndexFactory
from config.settings import settings

class RetrieverStep (BaseStep) :

    def execute(self, context: dict) -> dict:
        question = context["question"]
        mode = context["mode"]
        services = context["services"]

        if mode == "technical" and services:
            service = services[0]
            if service in settings.AVAILABLE_SERVICES:
                print(f"[RetrieverStep] Index service : {service}")
                index = IndexFactory.create(service)
                top_k = settings.TOP_K_SERVICE
            else:
                print(f"[RetrieverStep] Service inconnu → fallback global")
                index = IndexFactory.create("global")
                top_k = settings.TOP_K_GLOBAL
        else:
            print(f"[RetrieverStep] Index global")
            index = IndexFactory.create("global")
            top_k = settings.TOP_K_GLOBAL
        
        docs = index.similarity_search(question, k=top_k)
        print(f"[RetrieverStep] {len(docs)} chunks récupérés")

        context["docs"] = docs
        return context