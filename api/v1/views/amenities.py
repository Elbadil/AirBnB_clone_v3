#!/usr/bin/python3
"""Route for amenities objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrives the list of all Amenity objects on a GET request"""
    amenities = storage.all(Amenity)
    amenities_list = [am.to_dict() for am in amenities.values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrives an Amenity object that matches the id given"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        # Return a 404 error response if the amenity is not found
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object that matches the id given"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        # Return a 404 error response if the amenity is not found
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200  # 200 status code


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Adds a new Amenity object to amenities"""
    amenity_json_data = request.get_json()
    if not amenity_json_data:
        abort(400, 'Not a JSON')
    if "name" not in amenity_json_data:
        abort(400, "Missing name")
    amenity = Amenity(**amenity_json_data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201  # 201 status code


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an Amenity object that matches the id given"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        # Return a 404 error response if the amenity is not found
        abort(404)
    amenity_json_data = request.get_json()
    if not amenity_json_data:
        abort(400, 'Not a JSON')

    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in amenity_json_data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200  # 200 status code
