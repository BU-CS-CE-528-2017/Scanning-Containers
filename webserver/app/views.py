from flask import render_template
from app import app

@app.route('/')	#route for URL
@app.route('/index')
def index():
	user = {'nickname', 'Blake'} #placehoder for user

	#for mongo:
	#online_users = mongo.db.users.find({'online':True})
	
	return render_template('index.html', title='Home', user=user)

