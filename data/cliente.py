from abc import ABC, abstractmethod

class Cliente(ABC):
    def __init__(self):
        self.__consumoMensal = None
        self.__energiaAlocada = None
    
    @abstractmethod
    def consumoMensal(self):
        pass
    
    @abstractmethod
    def energiaAlocada(self):
        pass
    
    @abstractmethod
    def energiaAlocada(self, valor: float):
        pass
    
    @abstractmethod
    def calculaDeltaEnergetico(self):
        pass