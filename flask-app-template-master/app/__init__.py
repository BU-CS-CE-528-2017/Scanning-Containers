# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from flask import Flask, current_app
from flask_bootstrap import Bootstrap
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_login import LoginManager
#from pymongo import MongoClient, Connection


app = Flask(__name__)


def get_db():
    cl = MongoClient()
    return cl.db

#collUsers = cl["scans"]["users"]
#connection = Connection()
#db = connection['test']
#db.test.insert( { "item": "card", "qty": 15 } )
#app.db = db


#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

bootstrap = Bootstrap(app) #flask-bootstrap
#db = SQLAlchemy(app) #flask-sqlalchemy
#db = PyMongo(app)

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'


from app import views, models
