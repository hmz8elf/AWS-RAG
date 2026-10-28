from abc import ABC,abstractmethod

class BaseStep (ABC) :
    
    @abstractmethod
    def execute ( self, context : dict) -> dict :
        pass

