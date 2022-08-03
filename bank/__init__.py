from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'uploaded_files/'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

global_response_template = {'isSuccess': False, 'response': None, 'error': None, 'logs': None}

from bank import routes