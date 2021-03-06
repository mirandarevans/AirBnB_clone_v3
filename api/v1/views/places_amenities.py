#!/usr/bin/python3
'''
routes to view and alter place/amenity relationships
'''

from os import getenv
from models import storage, Place, Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def amenities_of_a_place(place_id):
    '''
        lists all amenities of a place
    '''
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        my_amenities = [amenity.to_dict() for amenity in my_place.amenities]
    else:
        my_amenities = my_place.amenity_ids
    return jsonify(my_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST', 'DELETE'])
def change_relationship(place_id, amenity_id):
    '''
        adds or deletes an amenity from a place
    '''
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        if request.method == 'POST':
            if my_amenity in my_place.amenities:
                return jsonify(my_amenity.to_dict()), 200
            my_place.amenities.append(my_amenity)
            storage.save()
            return jsonify(my_amenity.to_dict()), 201
        else:
            if my_amenity not in my_place.amenities:
                abort(404)
            my_place.amenities.remove(my_amenity)
            storage.save()
            return jsonify({}), 200
    else:
        if request.method == 'POST':
            if amenity_id in my_place.amenity_ids:
                return jsonify(my_amenity.to_dict()), 200
            else:
                my_place.amenity_ids.append(amenity_id)
                my_place.save()
                return jsonify(my_amenity.to_dict()), 201
        else:
            if amenity_id not in my_place.amenity_ids:
                abort(404)
            else:
                my_place.amenity_ids.remove(amenity_id)
                my_place.save()
                return jsonify({}), 200
