#!/usr/bin/python3
"""Route for users objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrives the list of all User objects on a GET request"""
    users = storage.all(User)
    users_list = [user.to_dict() for user in users.values()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrives a User object that matches the id given"""
    user = storage.get(User, user_id)
    if user is None:
        # Return a 404 error response if the user is not found
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object that matches the id given"""
    user = storage.get(User, user_id)
    if user is None:
        # Return a 404 error response if the user is not found
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200  # 200 status code


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Adds a new User object to users"""
    user_json_data = request.get_json()
    if not user_json_data:
        abort(400, 'Not a JSON')
    if "email" not in user_json_data:
        abort(400, "Missing email")
    if "password" not in user_json_data:
        abort(400, "Missing password")

    user = User(**user_json_data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201  # 201 status code


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User object that matches the id given"""
    user = storage.get(User, user_id)
    if user is None:
        # Return a 404 error response if the user is not found
        abort(404)
    user_json_data = request.get_json()
    if not user_json_data:
        abort(400, 'Not a JSON')

    ignored_keys = ["id", "created_at", "updated_at", "email"]
    for key, value in user_json_data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200  # 200 status code
