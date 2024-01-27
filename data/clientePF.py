from cliente import Cliente
from pessoaFisica import PessoaFisica

class ClientePF(PessoaFisica, Cliente):
    def __init__(self, nome: str, telefone: str, cep: str, rua: str, complemento: str, 
                 cpf: str, rg: str, dataNascimento: str, naturalidade: str):
        
        super().__init__(nome, telefone, cep, rua, complemento, cpf, rg, dataNascimento, naturalidade)
        self.__fatura = None
        
    @property
    def fatura(self):
        return self.__fatura
    
    @fatura.setter
    def fatura(self, fatura):
        # Métodos de validação da fatura
        self.__fatura = fatura
        self.__consumoMensal = 0 # Atualiza o consumo do mês de acordo com a fatura
    
    @property
    def consumoMensal(self):
        return self.__consumoMensal
    
    @property
    def energiaAlocada(self):
        return self.__energiaAlocada
    
    @energiaAlocada.setter
    def energiaAlocada(self, valor: float):
        # Métodos de validação para a energia alocada
        self.__energiaAlocada = valor
    
    def calculaDeltaEnergetico(self) -> float:
        return self.__energiaAlocada - self.__consumoMensal