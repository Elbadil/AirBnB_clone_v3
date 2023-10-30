#!/usr/bin/python3
"""Route for places objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """
    Retrives the list of all Place objects of a City
    on a GET request
    """
    city = storage.get(City, city_id)
    if city is None:
        # Return a 404 error response if the city is not found
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrives a Place object that matches the id given"""
    place = storage.get(Place, place_id)
    if place is None:
        # Return a 404 error response if the place is not found
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object that matches the id given"""
    place = storage.get(Place, place_id)
    if place is None:
        # Return a 404 error response if the place is not found
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200  # 200 status code


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Adds a new Place object to a City that matches the id given"""
    city = storage.get(City, city_id)
    if city is None:
        # Return a 404 error response if the city is not found
        abort(404)
    place_json_data = request.get_json()
    if not place_json_data:
        abort(400, 'Not a JSON')
    if "user_id" not in place_json_data:
        abort(400, "Missing user_id")
    if "name" not in place_json_data:
        abort(400, "Missing name")
    # Checking if the user_id passed exists
    user_id = place_json_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        # Return a 404 error response if the user is not found
        abort(404)
    # Adding the city_id given to the new place attributes
    place_json_data['city_id'] = city_id
    place = Place(**place_json_data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201  # 201 status code


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place object that matches the id given"""
    place = storage.get(Place, place_id)
    if place is None:
        # Return a 404 error response if the place is not found
        abort(404)
    place_json_data = request.get_json()
    if not place_json_data:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, value in place_json_data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200  # 200 status code
