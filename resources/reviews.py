import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

reviews = Blueprint('reviews', 'reviews')



# index for reviews GET /api/v1/reviews
@reviews.route('/', methods=['GET'])
@login_required
def reviews_index():
	
	current_user_review_dicts = [model_to_dict(dog) for dog in current_user.dogs]
	
	for review_dict in current_user_review_dicts:
		review_dict['posted_by'].pop('password')
	
	print(current_user_review_dicts)

	return jsonify({
		'data': current_user_review_dicts,
		'message': f"Successfully found {len(current_user_review_dicts)} reviews",
		'status': 200
	}), 200



# route to create review
@reviews.route('/', methods=['POST'])
@login_required
def create_dog():
	
	payload = request.get_json()

	new_review = models.Review.create(
		title=payload['name'],
		date_posted = DateTimeField(default=datetime.datetime.now),
		posted_by= current_user.id,
		review=payload['review'],
		location=payload['location']
	)

	review.dict = model_to_dict(new_review)

	print(review_dict)

	dog_dict['owner'].pop('password')

	return jsonify(
		data=review_dict,
		message="Successfully created a review!!",
		status=201
	), 201


# route to destroy review 
@reviews.route('/<id>', methods=['DELETE'])
@login_required
def delete_review(id):

	try:

		review_to_delete = models.Review.get_by_id(id)

		if review_to_delete.owner.id == current_user.id:
			review_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Successfully deleted review with id {id}",
				status=200
			), 200

		else:

			return jsonify(
				data={
					'error': '403 Forbidden'
				},
				message="User name doesn't match review id. OP is the only one that can delete",
				status=403
			), 403

	except models.DoesNotExist:
		return jsonify(
			data={
				'error': '404 Not Found'
			},
			message="Sorry, but there is no record of a review with this ID here",
			status=404
		), 404














































