#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_post_cities_in_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities])
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_state = City(state_id=state_id, **data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201




