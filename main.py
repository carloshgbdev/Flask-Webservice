import firebase_admin
import random

from flask import Flask, request, render_template, make_response 
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder='view') 

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def adicionar_empresa_cliente(nome, tipo, rua, cep, complemento, cnpj, producao, consumo):
    empresas_clientes_ref = db.collection('Empresas Clientes')
    # O Firestore criará automaticamente um ID único para cada novo documento
    empresa_cliente_ref = empresas_clientes_ref.document()
    
    # Cria uma chave de acesso aleatória
    key = random.randint(1, 1000)
    
    # Definir o documento com os dados da empresa
    empresa_cliente_ref.set({
        'acess': key,
        'nome': nome,
        'tipo': tipo,
        'rua': rua,
        'cep': cep,
        'complemento': complemento,
        'cnpj': cnpj,
        'producao': producao,
        'consumo': consumo,
        'status': 'Ativo'
    })

def busca_colecao(colecao):
    empresas_clientes_ref = db.collection(colecao)
    docs = empresas_clientes_ref.stream()
    
    empresas_clientes = []
    for doc in docs:
        # doc.to_dict() converte o documento em um dicionário
        empresas_clientes.append(doc.to_dict())

    return empresas_clientes

@app.route('/', methods=['GET'])
def home():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cookies = request.cookies
    autenticado = cookies.get('autenticado')
    
    if (autenticado == 'true'):
        cnpj = cookies.get('cnpj')
        key = cookies.get('key')
        
        if (cnpj == 'admin' and key == 'admin'):
            resp = make_response(adm())
            
            return resp
        else:
            resp = make_response(render_template('paginacliente.html',
                                                 acess=cnpj,
                                                 key=key))
            
            return resp
        
    return render_template('login.html')

@app.route('/login/autenticacao', methods=['POST'])
def autenticacao():
    cnpj = request.form['cnpj']
    key = request.form['key']
    remember = "off"
    
    try:
        remember = request.form['remember']
    except:
        remember = "off"
    
    if (cnpj == 'admin' and key == 'admin'):
        resp = make_response(adm())
        
        if (remember == 'on'):
            resp.set_cookie('cnpj', cnpj, max_age=30)
            resp.set_cookie('key', key, max_age=30)
            resp.set_cookie('autenticado', 'true', max_age=30)
        
        return resp
    else:
        try:
            empresas = busca_colecao('Empresas Clientes')
            
            for empresa in empresas:
                if (cnpj == empresa['cnpj'] and key == empresa['acess']):
                    if (remember == 'on'):
                        resp.set_cookie('cnpj', cnpj, max_age=30)
                        resp.set_cookie('key', key, max_age=30)
                        resp.set_cookie('autenticado', 'true', max_age=30)
                    
                    resp = make_response(render_template('paginacliente.html', acess=cnpj, key=key))
                    return resp
                
                return render_template('login.html', msg_err_autenticacao='CNPJ ou chave de acesso incorreta!')
        except:
            return render_template('login.html', msg_err_autenticacao='Erro na autenticação!')
    
@app.route('/adm', methods=['GET', 'POST'])
def adm(msg=None, acess='admin', key='admin'):
    empresas = busca_colecao('Empresas Clientes')
    
    if (msg == None):
        return render_template('adm.html', empresas=empresas, acess=acess, key=key)
    else:
        return render_template('adm.html', empresas=empresas, acess=acess, key=key, msg=msg)

@app.route('/adm/adiciona-empresa', methods=['POST'])
def adiciona_empresa_cliente():
    nome = request.form['nome']
    tipo = request.form['tipo']
    rua = request.form['rua']
    cep = request.form['cep']
    complemento = request.form['complemento']
    cnpj = request.form['cnpj']
    
    try:
        adicionar_empresa_cliente(nome=nome, cep=cep, 
                                tipo=tipo, rua=rua, 
                                complemento=complemento, cnpj=cnpj, 
                                producao='N/E', consumo='N/E')
        
        resp = make_response(adm(msg="<p style=\"color: green\">Cliente adicionado com sucesso!</p>"))
        
        return resp
    except:
        return adm(msg="<p style=\"color: red\">Erro ao adicionar o cliente</p>")

@app.route('/sobre-nos', methods=['GET'])
def sobre_nos():
    return render_template('sobrenos.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')

@app.route('/pagina-cliente', methods=['GET'])
def pagina_cliente():
    return render_template('paginacliente.html')

@app.route('/pagina-cliente/cliente-config', methods=['GET', 'POST'])
def cliente_config():
    return render_template('clienteconfig.html')

@app.route('/pagina-cliente/adicao-clientes', methods=['GET', 'POST'])
def adicao_clientes():
    return render_template('adicaoclientes.html')

@app.route('/pagina-cliente/filtro-clientes', methods=['GET'])
def filtro_clientes():
    return render_template('filtroclientes.html')

@app.route('/pagina-cliente/filtro-clientes/filtrados', methods=['GET'])
def filtrados():
    return render_template('filtrados.html')

@app.route('/pagina-cliente/filtro-clientes/fatura', methods=['GET'])
def fatura():
    return render_template('fatura.html')

if __name__ == '__main__':
    app.run(debug=True)
