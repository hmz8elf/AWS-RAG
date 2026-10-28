import os
import requests
import streamlit as st
from app.interfaces.appInterface import AppInterface
from dotenv import load_dotenv

load_dotenv()

class WebInterface(AppInterface):

    def __init__(self):
        self.ec2_url = os.getenv("EC2_URL", "http://localhost:8000")

    def processQuestion(self, question: str) -> str:
        """Envoie la question à l'API FastAPI sur EC2."""
        try:
            response = requests.post(
                f"{self.ec2_url}/ask",
                json={"question": question},
                timeout=30
            )
            return response.json()["answer"]
        except requests.exceptions.ConnectionError:
            return "Erreur : impossible de contacter le serveur EC2. Vérifiez EC2_URL dans .env"
        except requests.exceptions.Timeout:
            return "Erreur : le serveur EC2 ne répond pas (timeout 30s)"
        except Exception as e:
            return f"Erreur : {str(e)}"

    def start(self):
        st.set_page_config(
            page_title="AWS RAG Assistant",
            page_icon="☁️",
            layout="centered"
        )
        st.title("☁️ AWS RAG Assistant")
        st.caption("Posez vos questions sur les services AWS")

        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if question := st.chat_input("Ex: Je cherche un service de stockage NoSQL..."):
            st.session_state.messages.append(
                {"role": "user", "content": question}
            )
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Recherche dans la documentation AWS..."):
                    response = self.processQuestion(question)
                st.markdown(response)

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

    def getInput(self) -> str:
        pass

    def displayResponse(self, response: str):
        pass