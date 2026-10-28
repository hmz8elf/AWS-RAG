from abc import ABC, abstractmethod

class AppInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def getInput(self) -> str:
        pass

    @abstractmethod
    def displayResponse(self, response: str):
        pass

    @abstractmethod
    def processQuestion(self, question: str) -> str:
        pass