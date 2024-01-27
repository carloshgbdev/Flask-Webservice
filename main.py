from flask import Flask, request, render_template, make_response 

app = Flask(__name__, template_folder='view') 

@app.route('/', methods=['GET'])
def home():
    return render_template('homepage.html')

@app.route('/adm', methods=['GET'])
def adm():
    return render_template('adm.html')

@app.route('/sobre-nos', methods=['GET'])
def sobre_nos():
    return render_template('sobrenos.html')

@app.route('/contato', methods=['GET'])
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['POST'])
def login():
    return render_template('login.html')

@app.route('/paginacliente', methods=['GET'])
def paginacliente():
    return render_template('paginacliente.html')

@app.route('/paginacliente/clienteconfig', methods=['GET'])
def clienteconfig():
    return render_template('clienteconfig.html')

@app.route('/paginacliente/adicaoclientes', methods=['GET'])
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
