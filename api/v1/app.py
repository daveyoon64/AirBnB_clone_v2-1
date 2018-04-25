#!/usr/bin/python3
'''
    V1 of AirBnB API
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    '''handle 404 page'''
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_app(error):
    '''
        close application
    '''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
