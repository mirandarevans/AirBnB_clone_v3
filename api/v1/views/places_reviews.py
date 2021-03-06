#!/usr/bin/python3
'''
all review routes
'''

from models import storage, Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def reviews_of_a_place(place_id):
    '''
        GET: list all reviews in a specific place
        POST: add a review to a specific place
    '''
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    if request.method == 'POST':
        review_dict = request.get_json()
        if review_dict is None:
            return 'Not a JSON', 400
        if 'user_id' not in review_dict.keys():
            return 'Missing user_id', 400
        if 'text' not in review_dict.keys():
            return 'Missing text', 400
        if storage.get('User', review_dict['user_id']) is None:
            abort(404)
        review_dict['place_id'] = place_id
        my_review = Review(**review_dict)
        my_review.save()
        return jsonify(my_review.to_dict()), 201
    my_reviews = [review.to_dict() for review in storage.all('Review').values()
                  if review.place_id == place_id]
    return jsonify(my_reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_review(review_id):
    '''
        GET: display a specific review
        DELETE: delete a review
        PUT: update a review
    '''
    my_review = storage.get('Review', review_id)
    if my_review is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(my_review)
        storage.save()
        return jsonify({})
    if request.method == 'PUT':
        review_dict = request.get_json()
        if review_dict is None:
            return 'Not a JSON', 400
        for key, value in review_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                if key != 'place_id' and key != 'user_id':
                    setattr(my_review, key, value)
        my_review.save()
    return jsonify(my_review.to_dict())
