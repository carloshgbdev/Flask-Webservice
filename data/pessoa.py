class Pessoa:
    def __init__(self, nome: str, telefone: str, cep: str, rua: str, complemento: str):
        self.__nome = nome
        self.__telefone = telefone
        self.__cep = cep
        self.__rua = rua
        self.__complemento = complemento

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone: str):
        self.__telefone = telefone

    @property
    def cep(self):
        return self.__cep
    
    @cep.setter
    def cep(self, cep: str):
        self.__cep = cep
    
    @property
    def rua(self):
        return self.__rua

    @rua.setter
    def rua(self, rua: str):
        self.__rua = rua
    
    @property
    def complemento(self):
        return self.__complemento
    
    @complemento.setter
    def complemento(self, complemento: str):
        self.__complemento = complemento
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome
