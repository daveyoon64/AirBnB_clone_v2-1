#!/usr/bin/python3
'''States API view'''
import json
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
import sys


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def get_states():
    '''Get states'''
    j_list = []
    for k, v in storage.all('State').items():
        j_list.append(v.to_dict())
    return jsonify(j_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    '''Get state by id'''
    try:
        state = storage.get('State', state_id)
        return jsonify(state.to_dict())
    except:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE']
                 strict_slashes=False)
def del_state_id(state_id):
    '''Delete state by id'''
    if 'State.' + state_id in storage.all('State'):
        state = storage.get('State', state_id)
        storage.delete(state)
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    '''Create a state'''
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    elif not 'name' in request.get_json():
        abort(400, 'Missing name')
    else:
        state = request.get_json()
        new = State(**state)
        storage.new(new)
        storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Update a state'''
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    if 'State.' + state_id in storage.all('State'):
        state = storage.get('State', state_id)
        data = request.get_json()
        for k, v in data.items():
            if k is not 'id' or k is not 'created_at' or k is not 'updated_at':
                setattr(state, k, v)
            storage.save()
        return jsonify(state.to_dict()), 200
    else:
        return abort(404)
