from datetime import datetime
from typing import Set
from pessoaJuridica import PessoaJuridica
from clientePF import ClientePF
from clientePJ import ClientePJ

class EmpresaDistribuidora(PessoaJuridica):
    def __init__(self, nome: str, telefone: str, cep: str, rua: str, complemento: str, 
                 cnpj: str, capitalSocial: float, dataInicio: datetime, atividades: str,
                 clientesPF = set(), clientesPJ = set(), empresasGeradoras = set()):
        
        super().__init__(nome, telefone, cep, rua, complemento, cnpj, capitalSocial, dataInicio, atividades)
        self.__clientesPF = clientesPF
        self.__clientesPJ = clientesPJ
        self.__empresasGeradoras = empresasGeradoras
    
    @property
    def clientesPF(self):
        return self.__clientesPF
    
    @property
    def clientesPJ(self):
        return self.__clientesPJ
    
    @property
    def empresasGeradoras(self):
        return self.__empresasGeradoras
    
    def buscaClientePF(self, chave: str, metodo: str) -> ClientePF:
        try:
            match(metodo.lower()):
                case "cpf":
                    for cliente in self.__clientesPF:
                        if (cliente.cpf == chave):
                            return cliente
                case "nome":
                    for cliente in self.__clientesPF:
                        if (cliente.nome.upper() == chave.upper()):
                            return cliente
                case "rg":
                    for cliente in self.__clientesPF:
                        if (cliente.rg == chave):
                            return cliente
        
            raise("Cliente não encontrado.")
        
        except ValueError:
            print("O cliente não existe no banco de dados.")
    
    def buscaClientePJ(self, chave: str, metodo: str) -> ClientePJ:
        try:
            match(metodo.lower()):
                case "cnpj":
                    for cliente in self.__clientesPJ:
                        if (cliente.cnpj == chave):
                            return cliente
                case "nome":
                    for cliente in self.__clientesPJ:
                        if (cliente.nome.upper() == chave.upper()):
                            return cliente
        
            raise("Cliente não encontrado.")
        
        except ValueError:
            print("O cliente não existe no banco de dados.")
    
    def buscaEmpresaGeradora(self, chave: str, metodo: str):
        try:
            match(metodo.lower()):
                case "cnpj":
                    for empresa in self.__empresasGeradoras:
                        if (empresa.cnpj == chave):
                            return empresa
                case "nome":
                    for empresa in self.__empresasGeradoras:
                        if (empresa.nome.upper() == chave.upper()):
                            return empresa
        
            raise("Empresa parceira não encontrada.")
        
        except ValueError:
            print("A empresa não existe no banco de dados.")
    
    def adicionaClientePF(self, cliente: ClientePF):
        self.__clientesPF.add(cliente)
            
    def adicionaClientePJ(self, cliente: ClientePJ):
         self.__clientesPJ.add(cliente)
    
    def adicionaEmpresaGeradora(self, empresa):
        self.__empresasGeradoras.add(empresa)
    
    def removeEmpresaGeradora(self, chave: str, metodo: str):
        from empresaGeradora import EmpresaGeradora
        empresa = self.buscaEmpresaGeradora(chave, metodo)
        
        self.__empresasGeradoras.remove(empresa)
    
    def removeClientePF(self, chave: str, metodo: str):
        cliente = self.buscaClientePF(chave, metodo)
        
        self.__clientesPF.remove(cliente)
    
    def removeClientePJ(self, chave: str, metodo: str):
        cliente = self.buscaClientePJ(chave, metodo)

        self.__clientesPJ.remove(cliente)
    
    def emiteFatura(self, cliente):
        from fatura import Fatura
        # Métodos de emissão da fatura
        pass
    
    def calculaNumClientes(self):
        return len(self.__clientesPF) + len(self.__clientesPJ)

    def __entraEnergia():
        # Como não estamos interessados em regras de negócio,
        # essa função não é importante
        pass
    
    def __distribuiEnergia():
        # Como não estamos interessados em regras de negócio,
        # essa função não é importante
        pass