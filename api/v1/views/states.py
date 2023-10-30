#!/usr/bin/python3
"""Route for states objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_hbnb_states():
    """Retrives the list of all State objects on a GET request"""
    all_states = storage.all(State)
    states_list = [state.to_dict() for state in all_states.values()]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_hbnb_state(state_id):
    """Retrives a state object that matches the id given"""
    state = storage.get(State, state_id)
    if state is None:
        # Return a 404 error response if the state is not found
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200  # 200 status code


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Adds a new state to states using POST method"""
    new_state_json = request.get_json()
    if not new_state_json:
        abort(400, 'Not a JSON')
    if "name" not in new_state_json:
        abort(400, "Missing name")
    new_state = State(**new_state_json)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201  # 201 status code


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Updates a state using PUT method"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_json = request.get_json()
    if not state_json:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "created_at", "updated_at"]
    for key, value in state_json.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200  # 200 status code
