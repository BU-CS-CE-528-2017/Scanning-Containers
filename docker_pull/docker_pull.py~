#!flask/bin/python
from flask import Flask, jsonify, render_template, request 
import subprocess

app = Flask(__name__)

@app.route('/action', methods = ['POST'])
def get_tasks():
        string = request.form['dockerrep']
	cmd = "sudo docker run"+string
        result = subprocess.check_output(cmd, shell=True)
        print result
        return jsonify("hahahaha")

@app.route("/")
def home_page():
	return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

