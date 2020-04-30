from flask import Flask


DEBUG=True
PORT=8000


app = Flask(__name__)


# print hellow world, test
@app.route('/')
def hello():
	return 'Hello, world!'

if __name__== '__main__':
	app.run(debug=DEBUG, port=PORT)

