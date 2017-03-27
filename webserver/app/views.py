from flask import render_template
from app import app
from pymongo import MongoClient

client = MongoClient()
db = client.tododb

@app.route('/')	#route for URL
@app.route('/index')
def index():
	user = {'nickname', 'Blake'} #placehoder for user

	#for mongo:
	_items = db.tododb.find()
	items = [item for item in _items] 
	return render_template('web_page2.html', title='Home', user=user)

@app.route('/new', methods=['POST'])
def new():
	item_dock = {
		'name': request.form['name'], 'description' : request.form['description']
	} 
	db.tododb.insert_one(item_doc)
	return redirect(url_for('todo'))
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True)
