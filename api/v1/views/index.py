#!/usr/bin/python3
"""Defining app routes"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """displays the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def models_stats():
    """Displays a dictionary with the stats of each model"""
    models_dict = {}
    models = [Amenity, City, Place, Review, State, User]
    for model in models:
        models_dict[model.__tablename__] = storage.count(model)
    return jsonify(models_dict)
