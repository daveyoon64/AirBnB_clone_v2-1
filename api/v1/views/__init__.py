#!/usr/bin/python3
'''
    Create app_views and import
'''
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views import states, amenities, cities,\
                         places, places_reviews, users
