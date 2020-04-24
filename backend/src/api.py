import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES


@app.route('/drinks', methods=['GET'])
def drinks_get():
    drinks_raw = Drink.query.all()
    drinks = [drink.short() for drink in drinks_raw]
    if len(drinks) == 0:
        abort(404)
    data = {
        "success": True,
        "drinks": drinks
    }
    return jsonify(data), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_get_detail(payload):
    drinks_raw = Drink.query.all()
    drinks = [drink.long() for drink in drinks_raw]
    if len(drinks) == 0:
        abort(404)
    data = {
        "success": True,
        "drinks": drinks
    }
    return jsonify(data), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def drinks_post(payload):
    try:
        data = request.get_json()
        drink = Drink(
                        title=data['title'],
                        recipe=json.dumps(data['recipe']))
        drink.insert()
    except:
        abort(422, 'Missing values')
    else:
        return jsonify({
            'success': True,
            'drinks': drink.long()
            })


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def drinks_patch(payload, drink_id):
    try:
        data = request.get_json()

        drink = Drink.query.filter(Drink.id == drink_id).first()

        title = data.get('title', None)
        recipe = data.get('recipe', None)

        if title:
            drink.title = data['title']

        if recipe:
            drink.recipe = json.dumps(data['recipe'])

        drink.update()
    except Exception as e:
        print(e)
        abort(404, "drink not found")
    else:
        return jsonify({
            'success': True,
            'drinks': Drink.long(drink)
            })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def drinks_delete(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).first()

        drink.delete()
    except:
        abort(404, 'Drink not found')
    else:
        return jsonify({
            'success': True,
            'delete': drink_id
            })

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": str(error)
                    }), 422


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": str(error)
                    }), 404


@app.errorhandler(AuthError)
def authentification_failed(AuthError):
    return jsonify({
                "success": False,
                "error": AuthError.status_code,
                "message": AuthError.error
            }), 401
