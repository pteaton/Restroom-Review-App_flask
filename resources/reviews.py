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
				message="Username doesn't match review id. Only OP can delete",
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


# update review route
@reviews.route('/<id>', methods=['PUT'])
@login_required
def update_review(id):

	payload = request.get_json()

	dog_to_update = models.Review.get_by_id(id)

	if dog_to_update.posted_by.id = current_user.id:

		if 'title' in payload:
			review_to_update.title = payload['title']
		if 'review' in payload:
			review_to_update.review = payload['review']
		if 'location' in payload:
			review_to_update.location = payload['location']

		review_to_update.save()

		updated_review_dict = model_to_dict(review_to_update)

		updated_review_dict['posted_by'].pop('password')

		return jsonify(
			data=updated_review_dict,
			message=f"Successfully updated your review with id {id}",
			status=200
		), 200

	else:
		return jsonify(
			data={
				'error': '403 Forbidden'
			},
			message="Username doesn't match review id. Only OP can update",
			status=403
		), 403










































