#!/usr/bin/python3
'''Places API view'''
import json
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_reviews(place_id):
    '''Get place reviews'''
    j_list = []
    if 'Place.' + place_id in storage.all('Place'):
        for k, v in storage.all('Review').items():
            j_list.append(v.to_dict())
        return make_response(jsonify(j_list))
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    '''Get review by id'''
    try:
        review = storage.get('Review', review_id)
        return make_response(jsonify(review.to_dict()))
    except Exception:
        return abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review_id(review_id):
    '''Delete review by id'''
    if 'Review.' + review_id in storage.all('Review'):
        review = storage.get('Review', review_id)
        storage.delete(review)
        return make_response(jsonify({}), 200)
    else:
        return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    '''Create a place'''
    r = request.get_json()
    if type(r) is not dict:
        abort(400, 'Not a JSON')
    elif 'user_id' not in r:
        abort(400, 'Missing user_id')
    elif 'text' not in r:
        abort(400, 'Missing text')
    if 'Place.' + place_id in storage.all('Place'):
        if 'User.' + r['user_id'] in storage.all('User'):
            review = request.get_json()
            new = Review(**review)
            storage.new(new)
            storage.save()
        else:
            abort(404)
    else:
        abort(404)
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Update a place'''
    ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
    if type(request.get_json()) is not dict:
        abort(400, 'Not a JSON')
    if 'Review.' + review_id in storage.all('Review'):
        review = storage.get('Review', review_id)
        data = request.get_json()
        for k, v in data.items():
            if k not in ignore:
                setattr(review, k, v)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    else:
        return abort(404)
