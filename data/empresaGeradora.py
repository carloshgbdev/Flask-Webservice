from datetime import datetime
from pessoaJuridica import PessoaJuridica
from empresaDistribuidora import EmpresaDistribuidora
from typing import Dict, List, Set

class EmpresaGeradora(PessoaJuridica):
    def __init__(self, nome: str, telefone: str, cep: str, rua: str, complemento: str, 
                 cnpj: str, capitalSocial: float, dataInicio: datetime, atividades: str,
                 geracao: List[float], divisaoGeracao: Dict[str, float], clientes: Set[EmpresaDistribuidora] = set()):
        
        super().__init__(nome, telefone, cep, rua, complemento, cnpj, capitalSocial, dataInicio, atividades)
        self.__clientes = clientes
        self.__geracao = geracao
        self.__divisaoGeracao = divisaoGeracao
    
    @property
    def clientes(self):
        return self.__clientes
    
    def buscaCliente(self, chave: str, metodo: str) -> EmpresaDistribuidora:
        try:
            match(metodo.lower()):
                case "cnpj":
                    for cliente in self.__clientes:
                        if (cliente.nome.upper() == chave.upper()):
                            return cliente
                case "nome":
                    for cliente in self.__clientes:
                        if (cliente.nome == chave):
                            return cliente
        
            raise("Cliente não encontrado.")
        
        except ValueError:
            print("O cliente não existe no banco de dados.")
    
    def adicionaCliente(self, cliente: EmpresaDistribuidora):
        self.__clientes.add(cliente)
    
    def removeCliente(self, chave: str, metodo: str):
        cliente = self.buscaCliente(chave, metodo)
        
        self.__clientes.remove(cliente)
    
    @property
    def geracao(self):
        return self.__geracao
    
    @geracao.setter
    def geracao(self, valor: List[float]):
        # Métodos de validação da geração
        self.__geracao = valor
    
    @property
    def divisaoGeracao(self):
        return self.__divisaoGeracao
    
    @divisaoGeracao.setter
    def divisaoGeracao(self, valor: Dict[str, float]):
        # Métodos de validação da divisão de geração
        self.__divisaoGeracao = valor
    
    def emiteFatura(self, cliente):
        from fatura import Fatura
        # Métodos de emissão da fatura
        pass
    
    def calculaNumClientes(self):
        return len(self.__clientesPF) + len(self.__clientesPJ)

    def __geraEnergia():
        # Como não estamos interessados em regras de negócio,
        # essa função não é importante
        pass
    
    def __transmiteEnergia():
        # Como não estamos interessados em regras de negócio,
        # essa função não é importante
        pass