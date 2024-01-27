from flask import Flask

app = Flask(__name__, template_folder='view') #por default use o nome da pasta templates 

from app import admin
from app import cliente