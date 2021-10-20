#########################################################
#I# IMPORTS
#########################################################
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

#I### Imports from models and auth
from .database.models import db_drop_and_create_all, setup_db, Actor
#from .auth.auth import AuthError, requires_auth


#########################################################
#I# CREATE_APP
#########################################################
def create_app(test_config=None):

    #########################################################
    #I# INITIALISATION
    #########################################################
    app = Flask(__name__)

    setup_db(app)
    CORS(app)


    #########################################################
    ## CORS Headers   [TO BE CHECKED]
    #########################################################
    # @app.after_request
    # def after_request(response):
    #     response.headers.add(
    #     'Access-Control-Allow-Headers',
    #     'Content-Type,Authorization,true')
    #     response.headers.add(
    #     'Access-Control-Allow-Methods',
    #     'GET,PUT,POST,DELETE,OPTIONS')
    #     return response
    #
    # also insert @cross_origin() decorator where appropriate [TBC]
    #
    #

    #########################################################
    ## DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    #########################################################
    #db_drop_and_create_all()

    #########################################################
    ## ROUTES
    #########################################################
    '''
        endpoint GET /actors
            required permissions: 
                'get: actors'
            returns 
                status code 200 and json {"success": True, "actors": actors}
                or error status code with reason for failure
    '''
    @app.route('/actors', methods=['GET'])
    #@requires_auth(permission='get:actors')
    def get_actors():
    #def get_actors(payload):
        try:      
            actors = Actor.query.order_by(Actor.id).all()
            actors_array = [actor.todictionary() for actor in actors]
            print(actors_array)
        except:
            abort(422)

        return jsonify({
            'success': True,
            'actors': actors_array
        }, 200)


    '''
        endpoint POST /actor
            should create a new row in the Actors table
            required permissions: 
                'post: actor'
            returns 
                status code 200 and json {"success": True, "actor": actor} where actor is an array containing only the newly created actor
                or error status code with reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    #@requires_auth(permission='post:actors')
    #def post_actors(payload):
    def post_actors():
        try:
            
            body = request.get_json()

            new_name = body.get("name", None)
            new_age = body.get("age", None)
            new_gender = body.get("gender", None)

            new_actor = Actor(
                name = new_name,
                age = new_age,
                gender = new_gender
            )
            new_actor.insert()

            return jsonify({
                'success': True,
                'actor': new_actor.todictionary()
            }, 200)

        except:
            abort(422)

    '''
        endpoint PATCH /actors/id
            where <id> is the existing actor id
                it should respond with a 404 error if <id> is not found
                it should update the corresponding row for <id>
            required permissions: 
                'patch: actors'
            returns 
                status code 200 and json {"success": True, "actor": actor} where actor an array containing only the updated actor
                or error status code with reason for failure
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    #@requires_auth(permission='patch:actors')
    #def patch_actors(payload, id):
    def patch_actors(id):
            
        actor_to_patch = Actor.query.filter(Actor.id == id).one_or_none()
        if actor_to_patch is None:
            abort(404)

        try:
            body = request.get_json()

            new_name = body.get("name", None)
            new_age = body.get("age", None)
            new_gender = body.get("gender", None)

            print(new_name)

            if new_name != "null":
                actor_to_patch.name = new_name   
            if new_age != "null":
                actor_to_patch.age = new_age
            if new_gender != "null":
                actor_to_patch.gender = new_gender

            actor_to_patch.update()

            return jsonify({
                'success': True,
                'actor': actor_to_patch.todictionary()
            }, 200)

        except:
            abort(422, "bad request etc error description")


    '''
        endpoint DELETE /actors/id
            where <id> is the existing actor id
                it should respond with a 404 error if <id> is not found
                it should delete the corresponding row for <id>
            required permissions: 
                'delete: actors'
            returns 
                status code 200 and json {"success": True, "actor": actor} where actor an array containing only the deleted actor
                or error status code with reason for failure
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    #@requires_auth(permission='delete:actors')
    #def delete_actors(payload, id):
    def delete_actors(id):
            
        actor_to_delete = Actor.query.filter(Actor.id == id).one_or_none()
        if actor_to_delete is None:
            abort(404)

        try:
            actor_to_delete.delete()

            return jsonify({
                'success': True,
                'actor': actor_to_delete.todictionary()
            }, 200)

        except:
            abort(422, "bad request etc error description")


    #########################################################
    ## Error Handling
    #########################################################
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                        "success": False, 
                        "error": 422,
                        "message": "unprocessable"
                        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                        'success': False,
                        'error': 400,
                        'message': 'bad request'
                        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
                        'success': False,
                        'error': 405,
                        'message': 'method not allowed'
                        }), 405


    '''
    AuthError error handler
    '''
##########################################################################
##########################################################################
##########################################################################
##########################################################################
    #@app.errorhandler(AuthError)         <--   INCLUDE?   TO BE CHECKED
##########################################################################
##########################################################################     
##########################################################################
##########################################################################
    def handle_auth_error(ex):
        '''
        Receive the raised authorization error and include it in the response.
        '''
        response = jsonify(ex.error)
        response.status_code = ex.status_code

        return response
    
    
    return app


app = create_app()

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080, debug=True)
    app.run()

