import firebase_admin

from flask import Flask, request, render_template, make_response 
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder='view') 

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/', methods=['GET'])
def home():
    return render_template('homepage.html')

@app.route('/adm', methods=['GET', 'POST'])
def adm():
    return render_template('adm.html')

@app.route('/sobre-nos', methods=['GET'])
def sobre_nos():
    return render_template('sobrenos.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cookies = request.cookies
    autenticado = cookies.get('autenticado')
    
    if (autenticado == 'true'):
        cnpj = cookies.get('cnpj')
        key = cookies.get('key')
        
        if (cnpj == 'admin' and key == 'admin'):
            resp = make_response(render_template('adm.html',
                                                 acess=cnpj,
                                                 key=key))
            
            return resp
        else:
            resp = make_response(render_template('paginacliente.html',
                                                 acess=cnpj,
                                                 key=key))
            
            return resp
        
    return render_template('login.html')

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
        resp = make_response(render_template('adm.html', acess=cnpj, key=key))
        
        if (remember == 'on'):
            resp.set_cookie('cnpj', cnpj, max_age=30)
            resp.set_cookie('key', key, max_age=30)
            resp.set_cookie('autenticado', 'true', max_age=30)
        
        return resp
    else:
        return render_template('login.html', msg_err_autenticacao='Erro na autenticação!')
    
if __name__ == '__main__':
    app.run(debug=True)
