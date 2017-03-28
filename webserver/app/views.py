from flask import render_template, request, Flask, jsonify
from app import app
from pymongo import MongoClient

client = MongoClient()
db = client.tododb

@app.route('/')	#route for URL
def index():
	user = {'nickname', 'Blake'} #placehoder for user

	#for mongo:
	_items = db.tododb.find()
	items = [item for item in _items] 
	return render_template('web_page2.html', title='Home', user=user)

	#online_users = mongo.db.users.find({'online':True})
	
	return render_template('web_page2.html', title='Home', user=user)

#@app.route('/action', methods = ['POST'])
#def get_tasks():
#        string = request.form['dockerrep']
#	cmd = "docker run"+string
#        result = subprocess.check_output(cmd, shell=True)
#        print result
#        return jsonify("hahahaha")


@app.route('/new', methods=['POST'])
def new():
	item_dock = {
		'name': request.form['name'], 'description' : request.form['description']
	} 
	db.tododb.insert_one(item_doc)
	return redirect(url_for('todo'))
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True)
