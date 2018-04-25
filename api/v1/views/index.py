#!/usr/bin/python3
'''index for views'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage

props = {'Amenity': 'amenities', 'City': 'cities',
         'Place': 'places', 'Review': 'reviews',
         'State': 'states', 'User': 'users'}


@app_views.route('/status')
def status_check():
    '''
        return status of API
    '''
    return make_response(jsonify({'status': 'OK'}))


@app_views.route('/stats')
def get_stats():
    '''
        return stats of API
    '''
    stats = {}
    for k, v in props.items():
        stats[v] = storage.count(k)
    return make_response(jsonify(stats))
