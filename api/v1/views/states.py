#!/usr/bin/python3
'''States API view'''
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

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
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
    print('hello', file=sys.stderr)
    if not request.json or not 'name' in request.json:
        abort(400)
    state = request.json
    print('hello {}'.format(state), file=sys.stderr)
    new = State('state')
    storage.save()
    return jsonify(new.to_dict()), 200
