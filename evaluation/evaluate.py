import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import get_llm
from app.pipeline.classifierStep import ClassifierStep
from app.index.indexFactory import IndexFactory
from app.pipeline.generatorStep import GeneratorStep
from evaluation.eval_dataset import EVAL_DATASET
from langchain.schema import HumanMessage

def evaluate_faithfulness(question, answer, context, llm):
    print("      [DEBUG] Appel LLM faithfulness...")
    prompt = f"""
Tu es un évaluateur. Donne un score entre 0 et 1.
Le score doit indiquer si la RÉPONSE est basée uniquement sur le CONTEXTE fourni.
1.0 = totalement fidèle au contexte
0.0 = inventé, pas dans le contexte

CONTEXTE : {context[:500]}
RÉPONSE  : {answer[:300]}

Réponds UNIQUEMENT avec un nombre entre 0 et 1. Exemple: 0.85
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    print(f"      [DEBUG] Réponse LLM : {response.content.strip()}")
    try:
        return float(response.content.strip())
    except:
        return 0.5

def evaluate_relevancy(question, answer, llm):
    print("      [DEBUG] Appel LLM relevancy...")
    prompt = f"""
Tu es un évaluateur. Donne un score entre 0 et 1.
Le score doit indiquer si la RÉPONSE répond bien à la QUESTION.
1.0 = répond parfaitement
0.0 = hors sujet

QUESTION : {question}
RÉPONSE  : {answer[:300]}

Réponds UNIQUEMENT avec un nombre entre 0 et 1. Exemple: 0.85
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    print(f"      [DEBUG] Réponse LLM : {response.content.strip()}")
    try:
        return float(response.content.strip())
    except:
        return 0.5

def run_evaluation():
    print("---- Démarrage de l'évaluation\n")
    print(f"   Nombre de questions : {len(EVAL_DATASET)}")
    print(f"   LLM : Groq llama-3.3-70b\n")

    print("[DEBUG] Chargement LLM...")
    llm = get_llm()
    print("[DEBUG] LLM chargé")

    classifier = ClassifierStep()
    generator = GeneratorStep()

    faithfulness_scores = []
    relevancy_scores = []

    for i, item in enumerate(EVAL_DATASET):
        question = item["question"]
        print(f"\n[{i+1}/{len(EVAL_DATASET)}] {question[:60]}...")

        context_pipeline = {
            "question": question,
            "llm": llm,
            "mode": None,
            "services": []
        }

        print("   [DEBUG] Classification...")
        context_pipeline = classifier.execute(context_pipeline)

        mode = context_pipeline["mode"]
        services = context_pipeline["services"]
        print(f"   [DEBUG] Mode: {mode} | Services: {services}")

        from config.settings import settings
        if mode == "technical" and services and services[0] in settings.AVAILABLE_SERVICES:
            index = IndexFactory.create(services[0])
            top_k = settings.TOP_K_SERVICE
        else:
            index = IndexFactory.create("global")
            top_k = settings.TOP_K_GLOBAL

        print(f"   [DEBUG] Recherche {top_k} chunks...")
        docs = index.similarity_search(question, k=top_k)
        print(f"   [DEBUG] {len(docs)} chunks trouvés")

        context_pipeline["docs"] = docs
        print("   [DEBUG] Génération réponse...")
        context_pipeline = generator.execute(context_pipeline)
        print(f"   [DEBUG] Réponse : {context_pipeline['response'][:100]}...")

        answer = context_pipeline["response"]
        context = "\n".join([d.page_content for d in docs])

        time.sleep(2)

        print("   Évaluation faithfulness...")
        f_score = evaluate_faithfulness(question, answer, context, llm)
        faithfulness_scores.append(f_score)
        time.sleep(2)

        print("   Évaluation relevancy...")
        r_score = evaluate_relevancy(question, answer, llm)
        relevancy_scores.append(r_score)
        time.sleep(2)

        print(f" Faithfulness: {f_score:.2f} | Relevancy: {r_score:.2f}")

    avg_faithfulness = sum(faithfulness_scores) / len(faithfulness_scores)
    avg_relevancy = sum(relevancy_scores) / len(relevancy_scores)
    score_global = (avg_faithfulness + avg_relevancy) / 2

    print("\n" + "="*50)
    print(" RÉSULTATS ÉVALUATION")
    print("="*50)
    print(f"  Faithfulness     : {avg_faithfulness:.3f}  (objectif > 0.75)")
    print(f"  Answer Relevancy : {avg_relevancy:.3f}  (objectif > 0.75)")
    print(f"\n  Score Global     : {score_global:.3f}")
    if score_global >= 0.75:
        print("  Objectif atteint !")
    else:
        print("Score en dessous de l'objectif")
    print("="*50)

if __name__ == "__main__":
    run_evaluation()