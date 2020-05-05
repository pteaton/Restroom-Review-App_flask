import models
import datetime
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

reviews = Blueprint('reviews', 'reviews')



# index for reviews GET /api/v1/reviews/
@reviews.route('/', methods=['GET'])
@login_required
def reviews_index():
	
	current_user_review_dicts = [model_to_dict(review) for review in current_user.reviews]
	
	for review_dict in current_user_review_dicts:
		review_dict['posted_by'].pop('password')
	
	print(current_user_review_dicts)

	return jsonify({
		'data': current_user_review_dicts,
		'message': f"Successfully found {len(current_user_review_dicts)} reviews",
		'status': 200
	}), 200

# GET /reviews/all -- shows all reviews
@reviews.route('/all')
def get_all_reviews():
	reviews = models.Review.select()

	review_dicts = [model_to_dict(review) for review in reviews]

	for review_dict in review_dicts:
		review_dict['posted_by'].pop('password')
		if not current_user.is_authenticated:
			review_dict.pop('posted_by')

	return jsonify({
		'data': review_dicts,
		'message': f"Successfully found {len(review_dicts)} reviews",
		'status': 200

	}), 200


# route to create review
@reviews.route('/', methods=['POST'])
@login_required
def create_review():
	
	payload = request.get_json()

	new_review = models.Review.create(
		title=payload['title'],
		date_posted = datetime.datetime.now(),
		posted_by= current_user.id,
		review=payload['review'],
		location=payload['location']
	)

	review_dict = model_to_dict(new_review)

	print(review_dict)

	review_dict['posted_by'].pop('password')

	return jsonify(
		data=review_dict,
		message="Successfully created a review!!",
		status=201
	), 201




# update review route
@reviews.route('/<id>', methods=['PUT'])
@login_required
def update_review(id):

	payload = request.get_json()

	review_to_update = models.Review.get_by_id(id)

	if review_to_update.posted_by.id == current_user.id:

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

# show reviews
@reviews.route('/<id>', methods=['GET'])
def show_review(id):
	review = models.Review.get_by_id(id)

	if not current_user.is_authenticated:
		return jsonify(
			data={
				'title': review.title,
				'review': review.review,
				'location': review.location
			},
			message="Registered users can see more info about this review",
			status=200
		), 200

	else: 
		review_dict = model_to_dict(review)
		review_dict['posted_by'].pop('password')

		if review.posted_by.id != current_user.id:
			review_dict.pop('date_posted')

		return jsonify(
			data=review_dict,
			message=f"Found review with id {id}",
			status=200
		), 200


# route to destroy review 
@reviews.route('/<id>', methods=['DELETE'])
@login_required
def delete_review(id):

	try:

		review_to_delete = models.Review.get_by_id(id)

		if review_to_delete.posted_by.id == current_user.id:
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
