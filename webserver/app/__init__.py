
from flask import Flask 
#from flask_pymongo import PyMongo

app = Flask(__name__)
#mongo = PyMongo(app) 

app.config.from_object('config')

from app import views

#<<<<<<< HEAD
#import shell for launching docker
#import subprocess
#subprocess.call("ls", shell=True)
#subprocess.call("./run_docker.sh", shell = True)
#=======
#from "run_docker.py"
#import subprocess
#subprocess.call("ls", shell=True)
#subprocess.call("./run_docker.sh", shell=True)

#>>>>>>> dev-1
