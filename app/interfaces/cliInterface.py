import os
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from app.interfaces.appInterface import AppInterface
from dotenv import load_dotenv

load_dotenv()
console = Console()

class CLIInterface(AppInterface):

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
        console.print(Panel(
            Text.assemble(
                ("AWS RAG Assistant\n", "bold cyan"),
                (f"Mode : CLI  |  Serveur : {self.ec2_url}", "dim")
            ),
            border_style="cyan",
            padding=(1, 4)
        ))
        console.print("[dim]Commandes : 'exit' pour quitter | 'clear' pour effacer[/dim]\n")

        history = FileHistory(".cli_history")

        while True:
            try:
                question = self.getInput(history)

                if not question:
                    continue
                if question.lower() in ["exit", "quit", "q"]:
                    console.print("\n[dim]Au revoir ![/dim]")
                    break
                if question.lower() == "clear":
                    console.clear()
                    continue

                with console.status("[cyan]Recherche dans la documentation AWS...[/cyan]"):
                    response = self.processQuestion(question)

                self.displayResponse(response)

            except KeyboardInterrupt:
                console.print("\n[dim]Au revoir ![/dim]")
                break

    def getInput(self, history=None) -> str:
        return prompt("\n You: ", history=history).strip()

    def displayResponse(self, response: str):
        console.print("\n[bold cyan] Assistant:[/bold cyan]")
        console.print(Markdown(response))