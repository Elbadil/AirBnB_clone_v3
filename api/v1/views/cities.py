#!/usr/bin/python3
"""Route for cities objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_of_state(state_id):
    """
    Retrives the list of all City objects of a State
    on a GET request
    """
    state = storage.get(State, state_id)
    if state is None:
        # Return a 404 error response if the state is not found
        abort(404)
    state_cities = state.cities
    cities_of_state_list = [city.to_dict() for city in state_cities]
    return jsonify(cities_of_state_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrives a City object that matches the id given"""
    city = storage.get(City, city_id)
    if city is None:
        # Return a 404 error response if the city is not found
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object that matches the id given"""
    city = storage.get(City, city_id)
    if city is None:
        # Return a 404 error response if the city is not found
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200  # 200 status code


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Adds a new City object to a State that matches the id given"""
    state = storage.get(State, state_id)
    if state is None:
        # Return a 404 error response if the state is not found
        abort(404)
    city_json_data = request.get_json()
    if not city_json_data:
        abort(400, 'Not a JSON')
    if "name" not in city_json_data:
        abort(400, "Missing name")

    # adding state_id of the State as attribute to city_json_data
    city_json_data['state_id'] = state_id
    city = City(**city_json_data)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201  # 201 status code


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a City objects that matches the id given"""
    city = storage.get(City, city_id)
    if city is None:
        # Return a 404 error response if the city is not found
        abort(404)

    city_json_data = request.get_json()
    if not city_json_data:
        abort(400, 'Not a JSON')

    ignored_keys = ["id", "created_at", "updated_at", "state_id"]
    for key, value in city_json_data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200  # 200 status code
