import json
from langchain.schema import HumanMessage
from app.pipeline.baseStep import BaseStep
from config.settings import settings


INTENT_PROMPT = """
Tu es un classificateur de requêtes AWS.
Analyse la question et réponds UNIQUEMENT en JSON valide.
Aucun texte avant ou après le JSON.

Format attendu :
{{
  "mode": "discovery" ou "technical",
  "services": ["services AWS détectés en minuscules"]
}}

Règles :
- "discovery" : question vague, cherche une recommandation, compare des services
- "technical" : demande du code, une commande CLI, une configuration précise

Services reconnus : {services}

Question : {question}
"""
class ClassifierStep (BaseStep) :

    def execute(self, context) -> dict:
        question = context["question"]
        llm = context["llm"]

        prompt = INTENT_PROMPT.format(
            services=", ".join(settings.AVAILABLE_SERVICES),
            question=question
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content if hasattr(response, "content") else str(response)
        content = content.replace("```json", "").replace("```", "").strip()

        try:
            intent = json.loads(content)
        except json.JSONDecodeError:
            print("[ClassifierStep ] JSON invalide, fallback discovery")
            intent = {"mode": "discovery", "services": []}

        context["mode"] = intent.get("mode", "discovery")
        context["services"] = intent.get("services", [])

        print(f"[ClassifierStep] Mode: {context['mode']} | Services: {context['services']}")
        return context