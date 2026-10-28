from langchain.schema import HumanMessage
from app.pipeline.baseStep import BaseStep

DISCOVERY_PROMPT = """
Tu es un expert AWS. L'utilisateur cherche un service adapté à son besoin.

Documentation AWS :
{context}

Question : {question}

Instructions :
- Recommande le ou les services les plus adaptés
- Pour chaque service : nom + cas d'usage en 2 lignes maximum
- Sois concis et direct
- Termine par : "Souhaitez-vous plus de détails sur l'un de ces services ?"
"""

TECHNICAL_PROMPT = """
Tu es un expert AWS. L'utilisateur a une question technique précise.

Documentation officielle AWS :
{context}

Question : {question}

Instructions :
- Réponds directement et précisément
- Si c'est une commande CLI ou du code, formate-le en markdown
- Base-toi uniquement sur la documentation fournie
"""

class GeneratorStep( BaseStep ) :

    def execute(self, context: dict) -> dict:
        question = context["question"]
        mode = context["mode"]
        docs = context["docs"]
        llm = context["llm"]

        doc_context = "\n\n---\n\n".join([
            f"Page {doc.metadata.get('page', '?')} :\n{doc.page_content}"
            for doc in docs
        ])
        if mode == "discovery":
            prompt = DISCOVERY_PROMPT.format(
                context=doc_context,
                question=question
            )
        else:
            prompt = TECHNICAL_PROMPT.format(
                context=doc_context,
                question=question
            )
        response = llm.invoke([HumanMessage(content=prompt)])
        context["response"] = response.content if hasattr(response, "content") else str(response)

        print(f"[GeneratorStep] Réponse générée ")
        return context