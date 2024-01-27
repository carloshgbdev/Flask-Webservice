from flask import Flask, request, render_template, make_response 

app = Flask(__name__, template_folder='view') 

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/adm')
def sobre_nos():
    return render_template('adm.html')

@app.route('/sobre-nos')
def sobre_nos():
    return render_template('sobrenos.html')

@app.route('/contato')
def sobre_nos():
    return render_template('contato.html')

@app.route('/login')
def sobre_nos():
    return render_template('login.html')

@app.route('/paginacliente')
def sobre_nos():
    return render_template('paginacliente.html')

@app.route('/paginacliente/clienteconfig')
def sobre_nos():
    return render_template('clienteconfig.html')

@app.route('/paginacliente/adicaoclientes')
def sobre_nos():
    return render_template('adicaoclientes.html')

@app.route('/paginacliente/filtroclientes')
def sobre_nos():
    return render_template('filtroclientes.html')

@app.route('/paginacliente/filtroclientes/filtrados')
def sobre_nos():
    return render_template('filtrados.html')

@app.route('/paginacliente/filtroclientes/fatura')
def sobre_nos():
    return render_template('fatura.html')

if __name__ == '__main__':
    app.run(debug=True)
