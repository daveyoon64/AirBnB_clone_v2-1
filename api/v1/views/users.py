#!/usr/bin/python3
'''Users API view'''
import json
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User
import sys


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user_users():
    '''Get users'''
    j_list = []
    for k, v in storage.all('User').items():
        j_list.append(v.to_dict())
    return jsonify(j_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    '''Get user by id'''
    try:
        user = storage.get('User', user_id)
        return jsonify(user.to_dict())
    except Exception:
        return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user_id(user_id):
    '''Delete state by id'''
    if 'User.' + user_id in storage.all('User'):
        user = storage.get('User', user_id)
        storage.delete(user)
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    '''Create a user'''
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    elif 'email' not in request.get_json():
        abort(400, 'Missing email')
    elif 'password' not in request.get_json():
        abort(400, 'Missing password')
    else:
        user = request.get_json()
        new = User(**user)
        storage.new(new)
        storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Update a user'''
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    if 'User.' + user_id in storage.all('User'):
        user = storage.get('User', user_id)
        data = request.get_json()
        for k, v in data.items():
            if k is not 'id' or\
               k is not 'created_at' or\
               k is not 'updated_at' or\
               k is not 'email':
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(404)
