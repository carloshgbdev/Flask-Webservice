from datetime import datetime
from typing import Set
from empresaDistribuidora import EmpresaDistribuidora
from empresaGeradora import EmpresaGeradora
from pessoaJuridica import PessoaJuridica

class IsIon(PessoaJuridica):
    def __init__(self, clientesGeradores: Set[EmpresaGeradora] = set(), clientesDistribuidores: Set[EmpresaDistribuidora] = set()):
        super().__init__(nome="Is-Ion", telefone="Nosso telefone", cep="Nosso CEP", rua="Nossa rua", 
                         complemento="Nosso complemento", cnpj="Nosso CNPJ", capitalSocial=0, 
                         dataInicio=datetime(2024, 8, 27), atividades="Fazemos a inovação no mercado livre de energia")
        
        self.__clientesGeradores = clientesGeradores
        self.__clientesDistribuidores = clientesDistribuidores
    
    @property
    def clientesGeradores(self):
        return self.__clientesGeradores
    
    @property
    def clientesDistribuidores(self):
        return self.__clientesDistribuidores
        
    def buscaClienteGerador(self, chave: str, metodo: str) -> EmpresaGeradora:
        try:
            match(metodo.lower()):
                case "cnpj":
                    for empresa in self.__clientesGeradores:
                        if (empresa.cnpj == chave):
                            return empresa
                case "nome":
                    for empresa in self.__clientesGeradores:
                        if (empresa.nome.upper() == chave.upper()):
                            return empresa
        
            raise("Empresa parceira não encontrada.")
        
        except ValueError:
            print("A empresa não existe no banco de dados.")
    
    def buscaClienteDistribuidor(self, chave: str, metodo: str) -> EmpresaDistribuidora:
        try:
            match(metodo.lower()):
                case "cnpj":
                    for empresa in self.__clientesDistribuidores:
                        if (empresa.cnpj == chave):
                            return empresa
                case "nome":
                    for empresa in self.__clientesDistribuidores:
                        if (empresa.nome.upper() == chave.upper()):
                            return empresa
        
            raise("Empresa parceira não encontrada.")
        
        except ValueError:
            print("A empresa não existe no banco de dados.")
 
    def adicionaClienteGerador(self, cliente: EmpresaGeradora):
        self.__clientesGeradores.add(cliente)
            
    def adicionaClienteDistribuidor(self, cliente: EmpresaDistribuidora):
        self.__clientesDistribuidores.add(cliente)
    
    def removeClienteGerador(self, chave: str, metodo: str):
        cliente = self.buscaClienteGerador(chave, metodo)
        
        self.__clientesGeradores.remove(cliente)
    
    def removeClienteDistribuidor(self, chave: str, metodo: str):
        cliente = self.buscaClienteDistribuidor(chave, metodo)
        
        self.__clientesDistribuidores.remove(cliente)