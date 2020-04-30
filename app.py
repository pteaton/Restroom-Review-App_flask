from flask import Flask, jsonify
import models

DEBUG=True
PORT=8000


app = Flask(__name__)


# print hellow world, test
@app.route('/test_json')
def get_json():
	return jsonify(['review that', 'review this', 'review it all'])

if __name__== '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)

