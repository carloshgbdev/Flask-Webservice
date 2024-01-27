from app import app
from flask import request, render_template, make_response

@app.route("/", methods=['GET']) 
def root():
    #Escrever as paradas. Fazer realmente funcionar agora
    return None#Coloquei essa linha so para preencher espaco