from flask import Flask, request, render_template, make_response 

app = Flask(__name__, template_folder='view') 

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
                                                 var1=cnpj,
                                                 var2=key))
            
            return resp
        else:
            resp = make_response(render_template('paginacliente.html',
                                                 var1=cnpj,
                                                 var2=key))
            
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
        resp = make_response(render_template('adm.html', var1=cnpj, var2=key))
        
        if (remember == 'on'):
            resp.set_cookie('cnpj', cnpj, max_age=30)
            resp.set_cookie('key', key, max_age=30)
            resp.set_cookie('autenticado', 'true', max_age=30)
        
        return resp
    else:
        return render_template('login.html', msg_err_autenticacao='Erro na autenticação.')
    
if __name__ == '__main__':
    app.run(debug=True)
