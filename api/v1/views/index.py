#!/usr/bin/python3
'''index for views'''
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status_check():
    '''
        return status of API
    '''
    return jsonify({'status': 'OK'})
