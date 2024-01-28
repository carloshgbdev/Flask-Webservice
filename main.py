import firebase_admin

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
    
    # Definir o documento com os dados da empresa
    empresa_cliente_ref.set({
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

def busca_empresas_clientes():
    empresas_clientes_ref = db.collection('Empresas Clientes')
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
            empresas = busca_empresas_clientes()
            resp = make_response(adm(empresas=empresas))
            
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
        empresas = busca_empresas_clientes()
        resp = make_response(adm(empresas=empresas))
        
        if (remember == 'on'):
            resp.set_cookie('cnpj', cnpj, max_age=30)
            resp.set_cookie('key', key, max_age=30)
            resp.set_cookie('autenticado', 'true', max_age=30)
        
        return resp
    else:
        return render_template('login.html', msg_err_autenticacao='Erro na autenticação!')
    
@app.route('/adm', methods=['GET', 'POST'])
def adm(empresas, msg=None, acess='admin', key='admin'):
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
        
        empresas = busca_empresas_clientes()
        resp = make_response(adm(empresas=empresas, 
                                 msg="<p style=\"color: green\">Cliente adicionado com sucesso!</p>"))
        
        return resp
    except:
        empresas = busca_empresas_clientes()
        return adm(empresas=empresas,
                   msg="<p style=\"color: red\">Erro ao adicionar o cliente</p>")

@app.route('/sobre-nos', methods=['GET'])
def sobre_nos():
    return render_template('sobrenos.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')

@app.route('/paginacliente', methods=['GET'])
def paginacliente():
    return render_template('paginacliente.html')

@app.route('/paginacliente/clienteconfig', methods=['GET', 'POST'])
def clienteconfig():
    return render_template('clienteconfig.html')

@app.route('/paginacliente/adicaoclientes', methods=['GET', 'POST'])
def adicaoclientes():
    return render_template('adicaoclientes.html')

@app.route('/paginacliente/filtroclientes', methods=['GET'])
def filtroclientes():
    return render_template('filtroclientes.html')

@app.route('/paginacliente/filtroclientes/filtrados', methods=['GET'])
def filtrados():
    return render_template('filtrados.html')

@app.route('/paginacliente/filtroclientes/fatura', methods=['GET'])
def fatura():
    return render_template('fatura.html')

if __name__ == '__main__':
    app.run(debug=True)
