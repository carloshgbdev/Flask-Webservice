from datetime import datetime
from empresaGeradora import EmpresaGeradora

class Contrato:
    def __init__(self, tarifa: float, dataInicio: datetime, dataFim: datetime, empresaGeradora: EmpresaGeradora, condicoesNegociadas: str):
        self.__tarifa = tarifa
        self.__dataInicio = dataInicio
        self.__dataFinal = dataFim
        self.__empresaGeradora = empresaGeradora 
        self.__condicoesNegociadas = condicoesNegociadas

    @property
    def tarifa(self):
        print(f'"{self.__tarifa}" foi acessado.')
        return self.__tarifa
    
    @property
    def dataInicio(self):
        print(f'"{self.__dataInicio}" foi acessado.')
        return self.__dataInicio
    
    @property
    def dataFinal(self):
        print(f'"{self.__dataFinal}" foi acessado.')
        return self.__dataFinal
    
    @property
    def empresaGeradora(self):
        print(f'"{self.__empresaGeradora}" foi acessado.')
        return self.__empresaGeradora

    @property
    def condicoesNegociadas(self):
        print(f'"{self.__condicoesNegociadas}" foi acessado.')
        return self.__condicoesNegociadas
    
    @tarifa.setter
    def tarifa(self, valor: float):
        try:
            float(valor)
            self.__tarifa = valor
            print(f'o valor da tarifa foi alterado de "{self.__tarifa}" para "{valor}"')

        except ValueError:
            raise TypeError('Insira uma tarifa válida ')
        
    @dataInicio.setter
    def dataInicio(self, valor: datetime):
        try:
            self.__dataInicio = valor
            print(f'a data de inicio do contrado foi alterado de "{self.__dataInicio}" para "{valor}"')

        except ValueError:
            raise TypeError('Insira uma data de inicio válida ')
    

    @dataFinal.setter
    def dataFinal(self, valor: datetime):
        try:
            self.__tarifa = valor
            print(f'a data de fim do contrado foi alterado de "{self.__dataFim}" para "{valor}"')

        except ValueError:
            raise TypeError('Insira uma data de fim válida ')
    
    @empresaGeradora.setter
    def empresaGeradora(self, valor: EmpresaGeradora):
        try:
            self.__empresaGeradora = valor
            print(f' A empresa geradora foi alterada de "{self.__empresaGeradora}" para "{valor}"')
            
        except ValueError:
            raise TypeError('Insira uma empresa geradora válida')

    @condicoesNegociadas.setter
    def condicicoesNegociadas(self, valor: str):
        try:
            str(valor)
            self.__condicoesNegociadas = valor
            print(f'As condições negóciadas foram alteradas de "{self.__condicoesNegociadas}" para "{valor}"')
        except:
            raise TypeError ('Insira uma condição válida')

    def calculaDuracao(self) -> datetime:
        return (self.__dataFim - self.__dataInicio)