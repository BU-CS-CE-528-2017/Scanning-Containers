from flask import Flask 
#from flask_pymongo import PyMongo

app = Flask(__name__)
#mongo = PyMongo(app) 

app.config.from_object('config')

from app import views

#from "run_docker.py"
import subprocess
subprocess.call("ls", shell=True)
subprocess.call("./run_docker.sh", shell=True)

