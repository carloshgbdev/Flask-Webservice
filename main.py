import firebase_admin
import random
import os

from flask import Flask, request, render_template, make_response, session, redirect, url_for
from firebase_admin import credentials, firestore, auth

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
    
def adicionar_contato(first_name, last_name, company_name, company_email, company_role, state, comments, privacy):
    contato_ref = db.collection('Contato')
    # O Firestore criará automaticamente um ID único para cada novo documento
    contato_ref = contato_ref.document()

    contato_ref.set({
        'first-name': first_name,
        'last-name': last_name,
        'company-name': company_name,
        'company-email': company_email,
        'company-role': company_role,
        'state': state,
        'comments': comments,
        'privacy': privacy
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

def obter_clientes_por_referencias(cnpj):
    ref = busca_primeiro_documento('Empresas Clientes', 'cnpj', cnpj)
    doc = ref.get()

    # Lista para armazenar os dados dos clientes
    lista_de_clientes = []

    # Supõe-se que o campo que contém as referências é chamado 'clientes'
    if 'clientes' in doc.to_dict():
        # Obter o array de referências
        referencias = doc.to_dict()['clientes']

        # Iterar sobre as referências e obter cada documento de cliente
        for ref_cliente in referencias:
            # A referência é um objeto DocumentReference, então você pode chamar get() diretamente
            doc_cliente = ref_cliente.get()
            if doc_cliente.exists:
                # Adicionar os dados do cliente à lista
                lista_de_clientes.append(doc_cliente.to_dict())

    return lista_de_clientes

def filtra_clientes(filtro,parametro):
    docs = db.collection('Clientes').where(parametro, '==', filtro).stream()
    clientes_filtrados = []
    for doc in docs:
        clientes_filtrados.append(doc.to_dict())
    
    return clientes_filtrados


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
                print(cnpj)
                print(empresa['cnpj'])     
                print(key)
                print(empresa['acess'])
                if (cnpj == empresa['cnpj'] and key == str(empresa['acess'])):
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
    
def busca_id_documento_pelo_cnpj(cnpj):
    # Consultar a coleção para obter o documento com o CNPJ correspondente
    query_ref = db.collection("Empresas Clientes").where('cnpj', '==', cnpj).limit(1)
    resultados = query_ref.stream()

    # Obter o ID do documento a partir dos resultados da consulta
    for doc in resultados:
        # Retornar o ID do documento
        return doc.id
    return None  # Se não encontrar nenhum documento, retorna None

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
def contato(msg=None):
    return render_template('contato.html')

@app.route('/contato/adiciona-contato', methods=['POST'])
def adiciona_contato():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    company_name = request.form['company_name']
    company_email = request.form['company_email']
    company_role = request.form['company_role']
    state = request.form['state'] # Arrumar aqui
    comments = request.form['comments']
    privacy = request.form['privacy']
    
    try:
        adicionar_contato(first_name = first_name, last_name = last_name, 
                          company_name = company_name, company_email = company_email,
                          company_role = company_role, state = state,
                          comments = comments, privacy = privacy) #Arrumar aqui
        
        resp = make_response(contato(msg="<p style=\"color: green\">Contato adicionado com sucesso!</p>"))
        
        return resp
    except:
        return contato(msg="<p style=\"color: red\">Erro ao adicionar o contato</p>")


@app.route('/pagina-cliente', methods=['GET', 'POST'])
def pagina_cliente():
    return render_template('paginacliente.html')

@app.route('/pagina-cliente/cliente-config', methods=['GET', 'POST'])
def cliente_config(msg=None):   
    return render_template('clienteconfig.html', msg=msg)

@app.route('/pagina-cliente/cliente-config/deletar-conta', methods=['POST'])
def deletar_conta():
    document_id = busca_id_documento_pelo_cnpj(session.get('cnpj'))  # Substitua pelo ID do documento a ser excluído
    try:
        # Use o Firestore para excluir o documento
        db.collection('Empresas Clientes').document(document_id).delete()
        # Redirecione o usuário para a página de logout ou outra página apropriada
        return redirect(url_for('home'))
    except Exception as e:
        # Lide com erros ou exceções aqui, por exemplo, exibir uma mensagem de erro
        return "Erro ao excluir conta: " + str(e)

# @app.route('/pagina-cliente/cliente-config/atualizar', methods=['POST'])
# def atualizar_configuracoes():
#     print("Entrou em atualizar")
#     document_id = busca_id_documento_pelo_cnpj(session.get('cnpj'))
#     doc_ref = db.collection('Empresas Clientes').document(document_id)

#     # Dados originais do documento
#     doc_original = doc_ref.get().to_dict()

#     # Dados para atualizar
#     dados_atualizados = {
#         'nome': request.form['name'] if 'name' in request.form and request.form['name'] else doc_original['nome'],
#         'cnpj': request.form['cnpj'] if 'cnpj' in request.form and request.form['cnpj'] else doc_original['cnpj'],
#         'email': request.form['email'] if 'email' in request.form and request.form['email'] else doc_original['email'],
#         'date': request.form['date'] if 'date' in request.form and request.form['date'] else doc_original['date'],
#         'country': request.form['country'] if 'country' in request.form and request.form['country'] else doc_original['country'],
#         'cep': request.form['cep'] if 'cep' in request.form and request.form['cep'] else doc_original['cep'],
#         'state': request.form['state'] if 'state' in request.form and request.form['state'] else doc_original['state'],
#         'city': request.form['city'] if 'city' in request.form and request.form['city'] else doc_original['city'],
#         'neighborhood': request.form['neighborhood'] if 'neighborhood' in request.form and request.form['neighborhood'] else doc_original['neighborhood'],
#         'rua': request.form['street'] if 'street' in request.form and request.form['street'] else doc_original['street'],
#         'complement': request.form['complement'] if 'complement' in request.form and request.form['complement'] else doc_original['complement'],
#         'acess': request.form['new-password'] if 'new-password' in request.form and request.form['new-password'] == request.form.get('confirm-password', '') else doc_original['acess']
#     }

#     # Atualiza o documento apenas com os campos fornecidos
#     doc_ref.update(dados_atualizados)




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

@app.route('/pagina-cliente/filtro-clientes', methods=['GET','POST'])
def filtro_clientes():
    clientes = obter_clientes_por_referencias(session.get('cnpj'))
    filtro = request.form.get('filtro')
    clientes_filtrados = filtra_clientes(filtro,'tipo')

    if (filtro == 'todos' or filtro == None):
        return render_template('filtroclientes.html', clientes=clientes)
    else:
        return render_template('filtroclientes.html', clientes=clientes_filtrados)

@app.route('/pagina-cliente/filtro-clientes', methods=['GET','POST'])
def filtrados():
    
   
    return render_template('filtrados.html')

@app.route('/pagina-cliente/filtro-clientes/fatura', methods=['GET'])
def fatura():
    return render_template('fatura.html')


@app.route('/buscar', methods=['POST'])
def buscar_cliente():
    clientes = obter_clientes_por_referencias(session.get('cnpj'))
    nome_cliente = request.form.get('search')
    texto = nome_cliente
    if nome_cliente.isnumeric():
        filtro = 'cpf_cnpj'
    else:
        filtro = 'nome'

    print(nome_cliente)
    clientes_filtrados = filtra_clientes(nome_cliente,filtro)
    if clientes_filtrados:
        mensagem = ''
        return render_template('pesquisaclientes.html', clientes=clientes_filtrados,mensagem=mensagem,texto=texto)
    else:
        mensagem = "Cliente não encontrado."
        return render_template('pesquisaclientes.html', clientes=clientes,mensagem=mensagem,texto=texto)
    



if __name__ == '__main__':
    app.run(debug=True)
