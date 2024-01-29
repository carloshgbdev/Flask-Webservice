from acessorio import Acessorio as Ferramentas
from pessoa import Pessoa
from datetime import datetime

class PessoaJuridica(Pessoa):
    #Irei tirar o parametro "porte", não faz muito sentido
    def __init__(self, nome: str, telefone: str, cep: str, rua: str, complemento: str, cnpj: str, capitalSocial: float, dataInicio: datetime, atividades: str):
        super().__init__(nome, telefone, cep, rua, complemento)
        self.__ferramentas = Ferramentas()
        self.__cnpj = cnpj if self.__ferramentas.validaCNPJ(cnpj) else None
        self.__capitalSocial = capitalSocial
        self.__dataInicio = dataInicio
        self.__atividades = atividades
        self.__idadePJ = self.__ferramentas.calculaIdade(dataInicio)

    @property
    def capitalSocial(self):
        return self.__capitalSocial
    
    @capitalSocial.setter
    def capitalSocial(self, capitalsocial: float):
        self.__capitalSocial = capitalsocial

    @property
    def atividades(self):
        return self.__atividades 
    
    @atividades.setter
    def atividades(self, atividades: str):
        self.__atividades = atividades

    @property
    def cnpj(self):
        return self.__cnpj
    
    @cnpj.setter
    def cnpj(self, cnpj: str):
        try:
            if self.__ferramentas.validaCNPJ(cnpj):
                self.__cnpj = cnpj
            else:
                raise ValueError('CNPJ Invalido!')
        except ValueError:
            print('CNPJ Invalido!')
        
    @property
    def dataInicio(self):
        return self.__dataInicio
    
    @dataInicio.setter
    def dataInicio(self, dataInicio: datetime):
        self.__dataInicio = dataInicio
        self.__idadePJ = self.__ferramentas.calculaIdade(dataInicio)

    @property
    def idadePJ(self):
        return self.__idadePJ