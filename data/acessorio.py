from datetime import datetime
import re

class Acessorio:
    def __init__(self) -> None:
        pass
    
    def validaCPF(self, cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))
        if (len(cpf) != 11) or (cpf == cpf[0] * len(cpf)):
            return False

        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11)
            if digit == 10:
                digit = 0
            if digit != int(cpf[i]):
                return False
        return True

    def validaRG(self, rg: str) -> bool: 
        #remove os caracteres não numericos e X com 10, como digito verificador
        rg = rg.upper().replace('X','0')
        rg = ''.join(re.findall('\\d', rg))

        #Não ha um sistema unificado de verificacao de RG entre os estados
        #Por isso o unico sistema de verificação que conseguimos fazer esse 
        #Que seria ver se não é muito grande nem nulo.
        if (not rg) or (len(rg) < 7) or (len(rg) > 9) or (rg == rg[0] * len(rg)):
            return False
        else:
            return True

    def calculaIdade(self, data: datetime) -> int:
            today = datetime.now()
            idade = today.year - data.year -((today.month, today.day) < (data.month, data.day))

            return idade
        
    def validaCNPJ(self, cnpj: str) -> bool:
        cnpj = ''.join(filter(str.isdigit, cnpj))
        if (len(cnpj) != 14) or (cnpj == cnpj[0] * len(cnpj)):
            return False
        else:
        # Cálculo dos dígitos verificadores
            for i in [12, 13]:
                soma = 0
                peso = 2
                for j in range(i-1, -1, -1):
                    soma += int(cnpj[j]) * peso
                    peso += 1
                    if peso > 9:
                        peso = 2
                d = 11 - soma % 11
                if d > 9:
                    d = 0
                if int(cnpj[i]) != d:
                    return False
            return True