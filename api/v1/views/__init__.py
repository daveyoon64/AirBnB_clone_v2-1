#!/usr/bin/python3
'''
    Create app_views and import
'''
from flask import Blueprint
from api.v1.views import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
if app_views:
    from api.v1.views.index import *
