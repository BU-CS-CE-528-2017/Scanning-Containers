from flask import render_template, request, Flask, jsonify
from app import app

@app.route('/')	#route for URL
def index():
	user = {'nickname', 'Blake'} #placehoder for user

	#for mongo:
	#online_users = mongo.db.users.find({'online':True})
	
	return render_template('web_page2.html', title='Home', user=user)

@app.route('/action', methods = ['POST'])
def get_tasks():
        string = request.form['dockerrep']
	cmd = "sudo docker run"+string
        result = subprocess.check_output(cmd, shell=True)
        print result
        return jsonify("hahahaha")

