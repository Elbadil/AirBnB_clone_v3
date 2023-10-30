#!/usr/bin/python3
"""Main application"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)


# Initialize CORS with the app instance
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """handles the error pages"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404  # Setting the HTTP status code to 404
    return response


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    if getenv('HBNB_API_PORT'):
        port = int(getenv('HBNB_API_PORT'))

    app.run(host=host, port=port, threaded=True)
