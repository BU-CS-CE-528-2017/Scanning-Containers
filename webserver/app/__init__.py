from flask import Flask 
#from flask_pymongo import PyMongo

app = Flask(__name__)
#mongo = PyMongo(app) 

app.config.from_object('config')

from app import views
