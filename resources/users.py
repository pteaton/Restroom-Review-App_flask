import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def text_user_resource():
	return "user resource working"

# register
@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()

	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()
	print(payload)

	try:
		models.User.get(models.User.email == payload['email'])

		return jsonify(
			data={},
			message=f"Sorry bud, a user with the email {payload['email']} already exists",
			status=401
		), 401

	except models.DoesNotExist:
		pw_hash = generate_password_hash(payload['password'])

		created_user = models.User.create(
			username=payload['username'],
			email=payload['email'],
			password=pw_hash
		)
		print(created_user)

		login_user(created_user)

		created_user_dict = model_to_dict(created_user)
		print(created_user_dict)

		print(type(created_user_dict['password']))

		created_user_dict.pop('password')

		return jsonify(
			data=created_user_dict,
			message=f"Successfully registered user {created_user_dict['email']}",
			status=201
		), 201

# login
@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()

	try:
		user = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user)
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		if(password_is_good):
			login_user(user)
			print(model_to_dict(user))

			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message=f"Successfully logged in {user_dict['email']}",
				status=201
			), 201

		else:
			print('pw is no good here')
			return jsonify(
				data={},
				message="Email or password is incorrect",
				status=401
			), 401

	except models.DoesNotExist:
		print('username is no good here')
		return jsonify(
			data={},
			message="Email or password is incorrect",
			status=401
		), 401

# logout
@users.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data={},
		message="Successfully logged out.",
		status=200
	), 200

# destroy
@users.route('/<id>', methods=['DELETE'])
@login_required
def delete_account(id):
	user_to_delete = models.User.get_by_id(id)

	if current_user.id == user_to_delete.id:
		user_to_delete.delete_instance()

		return jsonify(
			data={},
			message="Your account has been successfully deleted",
			status=200
		), 200

	else:
		return jsonify(
			data={},
			message="This account does not belong to you",
			status=403
		), 403

	return "delete route is here"




