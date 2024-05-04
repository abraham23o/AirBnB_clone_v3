#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    if request.method == 'GET':
        return jsonify([state.to_dict() for state in
                        storage.all(State).values()])
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'PUT',
                                                'DELETE'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    elif request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        val = request.get_json()
        for k, v in val.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
        storage.save()
        return jsonify(state.to_dict()), 200
