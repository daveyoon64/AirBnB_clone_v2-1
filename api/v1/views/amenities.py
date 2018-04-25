#!/usr/bin/python3
'''Amenities API view'''
import json
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
import sys


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''Get amenities'''
    j_list = []
    for k, v in storage.all('Amenity').items():
        j_list.append(v.to_dict())
    return make_response(jsonify(j_list))


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    '''Get amenity by id'''
    try:
        amenity = storage.get('Amenity', amenity_id)
        return make_response(jsonify(amenity.to_dict()))
    except Exception:
        return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity_id(amenity_id):
    '''Delete amenity by id'''
    if 'Amenity.' + amenity_id in storage.all('Amenity'):
        amenity = storage.get('Amenity', amenity_id)
        storage.delete(amenity)
        return make_response(jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    '''Create an amenity'''
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    elif 'name' not in request.get_json():
        abort(400, 'Missing name')
    else:
        amenity = request.get_json()
        new = Amenity(**amenity)
        storage.new(new)
        storage.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    '''Update an amenity'''
    ignore = ['id', 'created_at', 'updated_at']
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    if 'Amenity.' + amenity_id in storage.all('Amenity'):
        amenity = storage.get('Amenity', amenity_id)
        data = request.get_json()
        for k, v in data.items():
            if k not in ignore:
                setattr(amenity, k, v)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        return abort(404)
