import streamlit as st
from app.interfaces.appInterface import AppInterface

class WebInterface(AppInterface):

    def start(self):
        st.set_page_config(
            page_title="AWS RAG Assistant",
            page_icon="☁️",
            layout="centered"
        )
        st.title("☁️ AWS RAG Assistant")
        st.caption("Posez vos questions sur les services AWS")

        if "pipeline" not in st.session_state:
            with st.spinner("Chargement du modèle..."):
                st.session_state.pipeline = self.pipeline

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