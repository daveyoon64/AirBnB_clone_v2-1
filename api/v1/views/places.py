#!/usr/bin/python3
'''Places API view'''
import json
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    '''Get places'''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    j_list = []
    for k, v in storage.all('Place').items():
        if v.city_id == city.id:
            j_list.append(v.to_dict())
    return make_response(jsonify(j_list))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_id(place_id):
    '''Get place by id'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return make_response(jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place_id(place_id):
    '''Delete place by id'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    place.delete()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    '''Create a place'''
    r = request.get_json()
    if r is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    elif 'user_id' not in r:
        return (jsonify({"error": "Missing user_id"}), 400)
    elif 'name' not in r:
        return (jsonify({"error": "Missing name"}), 400)
    if 'City.' + city_id in storage.all('City'):
        if 'User.' + r['user_id'] in storage.all('User'):
            new = Place(**r)
            new.save()
        else:
            abort(404)
    else:
        abort(404)
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Update a place'''
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']

    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    for k, v in data.items():
        if k not in ignore:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
