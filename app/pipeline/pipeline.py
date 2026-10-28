"""RAG pipeline orchestrator.

Runs the steps in order on a shared context dict:
    ClassifierStep -> RetrieverStep -> GeneratorStep
(intent + service detection, FAISS retrieval, LLM answer generation)
and returns the generated answer.
"""
from app.pipeline.classifierStep import ClassifierStep
from app.pipeline.retrieverStep import RetrieverStep
from app.pipeline.generatorStep import GeneratorStep

class RAGPipeline :

    def __init__(self, llm):
        self.llm = llm
        self.steps = [
            ClassifierStep(),
            RetrieverStep(),
            GeneratorStep()
        ]
    
    def run(self, question: str) -> str:
        context = {
            "question": question,
            "llm": self.llm,
            "mode": None,
            "services": [],
            "docs": [],
            "response": ""
        }
        print(f"\n{'='*50}")
        print(f"Question : {question}")
        print(f"{'='*50}")
        
        for step in self.steps:
            context = step.execute(context)

        return context["response"]