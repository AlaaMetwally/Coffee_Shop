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

db_drop_and_create_all()

## ROUTES


@app.route('/drinks',methods=['GET'])
def get_drinks():
        all_drinks = Drink.query.all()
        drinks = list(map(Drink.short,all_drinks))

        return jsonify({
            'success':True,
            'drinks': drinks
        }),200


@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    all_drinks = Drink.query.all()
    drinks = list(map(Drink.long,all_drinks))

    return jsonify({
        'success':True,
        'drinks':drinks
    }),200


@app.route("/drinks",methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(payload):
    req = request.get_json()
    try:
        drink = Drink(title=req['title'],recipe=json.dumps(req['recipe']))
        drink.insert()
    except BaseException:
        abort(400)
    
    return jsonify({
        'success':True,
        'drinks':[drink.long()]
    }),200


@app.route('/drinks/<int:drink_id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload,drink_id):
    try:
        req = request.get_json()
        drink = Drink.query.filter_by(id=drink_id).one_or_none()

        if drink is None:
            abort(404)
        
        if req['title'] :
            drink.title = req['title'] 

        if req['recipe'] :
            drink.title = json.dumps(req['recipe'])

        drink.update()
        return jsonify({
            'success':True,
            'deleted':[drink.long()]
        }),200
    except:
        abort(422)

@app.route('/drinks/<int:drink_id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload,drink_id):
    try:
        drink = Drink.query.filter_by(id=drink_id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()
        return jsonify({
            'success':True,
            'deleted':drink_id
        }),200
    except:
        abort(422)
## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(AuthError)
def error_found(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
                    "success": False, 
                    "error": 500,
                    "message": "internal server error"
                    }), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
                    "success": False, 
                    "error": 405,
                    "message": "method not allowed"
                    }), 405
