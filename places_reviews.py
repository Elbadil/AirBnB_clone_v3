#!/usr/bin/python3
"""Route for reviews objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """
    Retrives the list of all Review objects of a Place
    on a GET request
    """
    place = storage.get(Place, place_id)
    if place is None:
        # Return a 404 error response if the place is not found
        abort(404)
    place_reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(place_reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrives a Review object that matches the id given"""
    review = storage.get(Review, review_id)
    if review is None:
        # Return a 404 error response if the review is not found
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object that matches the id given"""
    review = storage.get(Review, review_id)
    if review is None:
        # Return a 404 error response if the review is not found
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200  # 200 status code


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Adds a Review object in a Place that matches the id given"""
    place = storage.get(Place, place_id)
    if place is None:
        # Return a 404 error response if the place is not found
        abort(404)
    review_json_data = request.get_json()
    if not review_json_data:
        abort(400, 'Not a JSON')
    if "user_id" not in review_json_data:
        abort(400, "Missing user_id")
    if "text" not in review_json_data:
        abort(400, "Missing text")
    # Checking if the user_id passed exists
    user_id = review_json_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        # Return a 404 error response if the user is not found
        abort(404)
    # Adding the city_id given to the new place attributes
    review_json_data['place_id'] = place_id
    review = Review(**review_json_data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201  # 201 status code


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a Review object that matches the id given"""
    review = storage.get(Review, review_id)
    if review is None:
        # Return a 404 error response if the review is not found
        abort(404)
    review_json_data = request.get_json()
    if not review_json_data:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "created_at", "updated_at", "user_id", "place_id"]
    for key, value in review_json_data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200  # 200 status code
