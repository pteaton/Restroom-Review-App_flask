import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

reviews = Blueprint('reviews', 'reviews')

@reviews.route('/', methods=[GET])
def review_index():
	result = models.Review.select()
	print('')
	print('result of review query')
	print(result)
	return 'check terminal'

@reviews.route('/', methods=[POST])
def create_review():
	'''creates a review in databse '''
	payload = request.get_json()
	print(payload)

	new_review = models.Review.create(title=payload['title'], date_posted=payload['date posted'], review=payload['review'], location=payload['location'])
	print(new_review)
	print(new_review.__dict__)
	print(dir(new_review))

	car_dict = model_to_dict(new_review)
	return jsonify(
		data=review_dict,
		message='Successfully created a review',
		status=201
		), 201