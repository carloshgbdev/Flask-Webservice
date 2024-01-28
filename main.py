import firebase_admin
import random
import os

from flask import Flask, request, render_template, make_response, session
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder='view') 
app.secret_key = os.urandom(24)

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

def adicionar_cliente(cnpj, nome, tipo, rua, cep, complemento, cpf_cnpj, telefone, consumo, energia_alocada):
    clientes_ref = db.collection('Clientes')
    # O Firestore criará automaticamente um ID único para cada novo documento
    cliente_ref = clientes_ref.document()
    
    # Definir o documento com os dados da empresa
    cliente_ref.set({
        'nome': nome,
        'tipo': tipo,
        'rua': rua,
        'cep': cep,
        'complemento': complemento,
        'cpf_cnpj': cpf_cnpj,
        'telefone': telefone,
        'consumo': consumo,
        'energia_alocada': energia_alocada,
        'status': 'Ativo'
    })
    
    lista_clientes = puxa_clientes_da_empresa(cnpj)
    
    lista_clientes.append(cliente_ref)
    empresa_ref = busca_primeiro_documento('Empresas Clientes', 'cnpj', cnpj)
    
    empresa_ref.update({
        'clientes': lista_clientes
    })

def puxa_clientes_da_empresa(cnpj):
    empresas_clientes_ref = db.collection('Empresas Clientes')
    
    query = empresas_clientes_ref.where('cnpj', '==', cnpj)
    
    resultados = query.stream()
    
    empresas = []
    
    for resultado in resultados:
        empresas.append(resultado.to_dict())
    
    empresa_alvo = empresas[0]
    
    if "clientes" in empresa_alvo:
        return empresa_alvo['clientes']
    else:
        return []

def busca_colecao(colecao):
    colecao_ref = db.collection(colecao)
    docs = colecao_ref.stream()
    
    colecao = []
    for doc in docs:
        # doc.to_dict() converte o documento em um dicionário
        colecao.append(doc.to_dict())

    return colecao

def busca_primeiro_documento(colecao, campo, valor):
    empresas_clientes_ref = db.collection(colecao)
    query = empresas_clientes_ref.where(campo, '==', valor)
    resultados = query.stream()
    
    documentos = []
    
    for resultado in resultados:
        documentos.append(resultado.reference)
    
    return documentos[0]

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
        
        session['cnpj'] = cnpj
        session['key'] = key
        
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
                    session['cnpj'] = cnpj
                    session['key'] = key
        
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
def adicao_clientes(msg=None):
    if (msg == None):
        return render_template('adicaoclientes.html')
    else:
        return render_template('adicaoclientes.html', msg=msg)

@app.route('/pagina-cliente//adicao-clientes/cliente', methods=['POST'])
def registra_cliente():
    nome = request.form['name']
    tipo = request.form['type']
    rua = request.form['rua']
    cep = request.form['cep']
    complemento = request.form['complemento']
    cpf_cnpj = request.form['cpf_cnpj']
    telefone = request.form['telefone']
    consumo = request.form['consumo_mensal']
    energia_alocada = request.form['energia_alocada']
    

    adicionar_cliente(nome=nome, tipo=tipo, 
                    rua=rua, cep=cep, 
                    complemento=complemento, cpf_cnpj=cpf_cnpj, 
                    telefone=telefone, consumo=consumo, 
                    energia_alocada=energia_alocada, cnpj=session.get('cnpj'))
    
    resp = make_response(adicao_clientes(msg="<p style=\"color: green\">Cliente adicionado com sucesso!</p>"))
    
    return resp



@app.route('/pagina-cliente/filtro-clientes', methods=['GET'])
def filtro_clientes(msg=None):
    if (msg == None):
        return render_template('filtroclientes.html')
    else:
        return render_template('filtroclientes.html', msg=msg)

@app.route('/pagina-cliente/filtro-clientes/filtrados', methods=['GET'])
def filtrados():
    return render_template('filtrados.html')

@app.route('/pagina-cliente/filtro-clientes/fatura', methods=['GET'])
def fatura():
    return render_template('fatura.html')

if __name__ == '__main__':
    app.run(debug=True)
