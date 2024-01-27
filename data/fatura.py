from empresaDistribuidora import EmpresaDistribuidora
from contrato import Contrato

class Fatura:
    def __init__(self, tarifaDistribuicao: float, empresaDistribuicao: EmpresaDistribuidora, tributacao: float, 
                 convenioEstado: str, custosOperacao: float, tarifaEnergia: float):
        
        self.__tarifaDistribuicao = tarifaDistribuicao
        self.__empresaDistribuicao = empresaDistribuicao
        self.__tributacao = tributacao
        self.__convenioEstado = convenioEstado
        self.__custosOperacao = custosOperacao
        self.__tarifaEnergia = tarifaEnergia
        self.__contrato = None
    
    @property
    def tarifaDistribuicao(self):
        print(f'"{self.__tarifaDistribuicao}" foi acessado.')
        return self.__tarifaDistribuicao

    @property
    def empresaDistribuicao(self):
        print(f'"{self.__empresaDistribuicao}" foi acessado.')
        return self.__empresaDistribuicao

    @property
    def tributacao(self):
        print(f'"{self.__tributacao}" foi acessado.')
        return self.__tributacao    

    @property
    def convenioEstado(self):
        print(f'"{self.__convenioEstado}" foi acessado.')
        return self.__convenioEstado

    @property
    def custosOperacao(self):
        print(f'"{self.__custosOperacao}" foi acessado.')
        return self.__custosOperacao

    @property
    def tarifaEnergia(self):
        print(f'"{self.__tarifaEnergia}" foi acessado.')
        return self.__tarifaEnergia

    @property
    def contrato(self):
        return self.__contrato
    
    @contrato.setter
    def contrato(self, contrato: Contrato):
        self.__contrato = contrato

    @tarifaDistribuicao.setter
    def tarifaDistribuicao(self, valor: float):
        try:
            float(valor)
            self.__tarifaDistribuicao = valor
            print(f'o valor da tarifa de distribuição foi alterado de "{self.__tarifaDistribuicao}" para "{valor}"')

        except ValueError:
            raise TypeError('Insira uma tarifa de distribuição válida ') 

    @empresaDistribuicao.setter
    def empresaDistribuicao(self, valor: EmpresaDistribuidora):
        try:
            self.__empresaDistribuicao = valor
            print(f'A empresa distribuidora foi alterada de "{self.__empresaDistribuicao}" para "{valor}"')

        except ValueError:
            raise TypeError('Insira uma empresa distribuidora válida')           

    @tributacao.setter
    def tributacao(self, valor: float):
        try:
            float(valor)
            self.__tributacao = valor
            print(f'O valor de tributação foi alterado de  "{self.__tributacao}" para "{valor}"')

        except ValueError:
            raise TypeError('Insira um valor de tributação válido')   

    @convenioEstado.setter
    def convenioEstado(self, valor: str):
        try:
            str(valor)
            self.__convenioEstado = valor
            print(f'O convenio do estado foi alterado de  "{self.__convenioEstado}" para "{valor}"')

        except ValueError:
            raise TypeError('Insira um convenio de estado válido')

    @custosOperacao.setter
    def custosOperacao(self, valor: float):
        try:
            float(valor) 
            self.__custosOperacao = valor
            print(f'O valor do custo de operação foi alterado de  "{self.__custosOperacao}" para "{valor}"')       
        except ValueError:
            raise TypeError('Insira um valor de custo de operação válido')

    @tarifaEnergia.setter
    def tarifaEnergia(self,valor):
        try:
            float(valor) 
            self.__tarifaEnergia = valor
            print(f'O valor da tarifa de energia foi alterada de  "{self.__tarifaEnergia}" para "{valor}"')       
        except ValueError:
            raise TypeError('Insira um valor de tarifa de energia válido')       

    def calculaFatura(self) -> float:
        return (self.__tarifaEnergia * self.__tarifaDistribuicao * self.__tributacao) + self.__custosOperacao