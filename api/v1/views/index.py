#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """ check the status of route """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def get_obj_count():
    """get the number of each objects by type"""
    objs = {"amenities": 'Amenity', "cities": 'City', "places": 'Place',
            "reviews": 'Review', "states": 'State', "users": 'User'}
    for k, v in objs.items():
        objs[k] = storage.count(v)
    return jsonify(objs)
