from acessorio import Acessorio as Ferramentas
from pessoa import Pessoa
from datetime import datetime

class PessoaFisica(Pessoa):

    def __init__(self, nome: str, telefone: str, cep: str, rua: str, complemento: str, cpf: str, rg: str, dataNascimento: datetime, naturalidade: str):
        super().__init__(nome, telefone, cep, rua, complemento)
        self.__ferramentas = Ferramentas()
        self.__cpf = cpf if self.__ferramentas.validaCPF(cpf) else None
        self.__rg = rg if self.__ferramentas.validaRG(rg) else None
        self.__dataNascimento = dataNascimento
        self.__naturalidade = naturalidade
        self.__idade = self.__ferramentas.calculaIdade(dataNascimento)

    @property
    def naturalidade(self):
        return self.__naturalidade
    
    @naturalidade.setter
    def naturalidade(self, naturalidade: str):
        self.__naturalidade = naturalidade

    @property
    def dataNascimento(self):
        return self.__dataNascimento
    
    @dataNascimento.setter
    def dataNascimento(self, dataNascimento: datetime):
        self.__dataNascimento= dataNascimento
        self.__idade = self.__ferramentas.calculaIdade(dataNascimento)
        # Ele recebe a nova data de nascimento e já atualiza o valor da idade

    @property
    def idade(self):
        return self.__idade
    
    @property
    def cpf(self):
        return self.__cpf
    
    @cpf.setter
    def cpf(self, cpf: str):
        try:
            if self.__ferramentas.validaCPF(cpf):
                self.__cpf = cpf
            else:
                raise ValueError('CPF Invalido!')
        except ValueError:
            print('CPF Invalido!')

    @property
    def rg(self):
        return self.__rg
    
    @rg.setter
    def rg(self, rg: str):
        try:
            if self.__ferramentas.validaRG(rg):
                self.__rg = rg
            else:
                raise ValueError("RG Invalido!")
        except ValueError:
            print("RG Invalido!")