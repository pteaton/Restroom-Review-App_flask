import os
from flask import Flask, jsonify, g
from resources.reviews import reviews
from resources.users import users
import models 
from flask_cors import CORS
from flask_login import LoginManager

DEBUG=True
PORT=8000

app = Flask(__name__)

# Login/Authentication
app.secret_key = "This string is the secret string."
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		print("loading the following user")
		user = models.User.get_by_id(user_id)

		return user

	except models.DoesNotExist:
		return None

@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={
		'error': 'User is not logged in'
		},
		message="You must be logged in to access this resource.",
		status=401
	), 401

# CORS
CORS(reviews, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

# Blueprint
app.register_blueprint(reviews, url_prefix='/api/v1/reviews')
app.register_blueprint(users, url_prefix='/api/v1/users')

# Deployment
@app.before_request
def before_request():
	print("you should see this before each request")
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	print("you hsould see this after each request")
	g.db.close()
	return response 



# jsonify test
@app.route('/test_json')
def get_json():
	return jsonify(['review that', 'review this', 'review it all'])

# Heroku initialization
if 'ON_HEROKU' in os.environ:
	print('\non heroku!')
	models.initialize()

# Run App
if __name__== '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

