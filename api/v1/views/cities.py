#!/usr/bin/python3
'''Cities API view'''
import json
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import City
import sys


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    '''Get cities'''
    try:
        state = storage.get('State', state_id)
        j_list = []
        for k, v in storage.all('City').items():
            if v.state_id == state.id:
                j_list.append(v.to_dict())
        return make_response(jsonify(j_list))
    except Exception:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    '''Get city by id'''
    try:
        city = storage.get('City', city_id)
        return make_response(jsonify(city.to_dict()))
    except Exception:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city_id(city_id):
    '''Delete city by id'''
    if 'City.' + city_id in storage.all('City'):
        city = storage.get('City', city_id)
        storage.delete(city)
        return make_response(jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    '''Create a city'''
    try:
        state = storage.get('State', state_id)
        if type(request.get_json()) is not dict:
            abort(400, 'Not a JSON')
        elif 'name' not in request.get_json():
            abort(400, 'Missing name')
        else:
            data = request.get_json()
            data['state_id'] = state_id
            new = City(**data)
            storage.new(new)
            storage.save()
        return make_response(jsonify(new.to_dict()), 201)
    except Exception:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Update a city'''
    ignore = ['created_at', 'updated_at', 'state_id']
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    if 'City.' + city_id in storage.all('City'):
        city = storage.get('City', city_id)
        data = request.get_json()
        for k, v in data.items():
            if k not in ignore:
                setattr(city, k, v)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    else:
        return abort(404)
