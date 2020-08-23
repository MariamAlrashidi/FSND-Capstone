import os
from flask import Flask, abort, request, jsonify
from database.models import db_drop_and_create_all, db, setup_db
from database.models import Actor, Movie, Show
from auth import AuthError, requires_auth
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def hi():
        return jsonify({
            'success': True,
            'message': 'Welcome to API'
        })

    @app.route('/actor', methods=['GET'])
    @requires_auth('get:actor')
    def get_all_actors(jwt):
        data = Actor.query.all()
        actor = list(map(Actor.get_actor, data))
        if actor is None or len(actor) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actor': actor
        })

    @app.route('/actor', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(jwt):
        body = request.get_json()
        if body is None:
            abort(404)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
            return jsonify({
                'success': True,
                'actors': [new_actor.get_actor()]
            })

        except Exception:
            abort(404)

    @app.route('/actor/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_one_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(404)
        updated_name = body.get('name', None)
        updated_age = body.get('age', None)
        updated_gender = body.get('gender', None)

        if updated_name is not None:
            actor.name = updated_name
        if updated_age is not None:
            actor.age = updated_age
        if updated_gender is not None:
            actor.gender = updated_gender

        try:
            actor.update()
            return jsonify({
                'success': True,
                'actor': [actor.get_actor()]
            })
        except Exception:
            abort(422)

    @app.route('/actor/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def drop_one_actor(jwt, actor_id):
        selected_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if selected_actor is None:
            abort(404)
        try:
            selected_actor.delete()
            return jsonify({
                "success": True,
                "deleted": actor_id
            })
        except Exception:
            abort(422)

    @app.route('/movie', methods=['GET'])
    @requires_auth('get:movie')
    def get_all_movie(jwt):
        data = Movie.query.all()
        movie = list(map(Movie.get_movie, data))
        if movie is None or len(movie) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movie': movie
        })

    @app.route('/movie', methods=['POST'])
    @requires_auth('post:movie')
    def create_new_movie(jwt):
        body = request.get_json()
        if 'title' not in body:
            abort(404)
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
            return jsonify({
                'success': True,
                'movie': [new_movie.get_movie()]
            })
        except Exception:
            abort(422)

    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(404)

        updated_title = body.get('title', None)
        updated_release_date = body.get('release_date', None)

        if updated_title is not None:
            movie.title = updated_title
        if updated_release_date is not None:
            movie.release_date = updated_release_date

        try:
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.get_movie()
            })
        except Exception:
            abort(422)

    @app.route('/movie/<movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def drop_one_movie(jwt, movie_id):
        selected_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if selected_movie is None:
            abort(404)
        try:
            selected_movie.delete()
            return jsonify({
                "success": True,
                "deleted": movie_id
            })
        except Exception:
            abort(422)

    @app.route('/show')
    def get_all_show():
        data = Show.query.all()
        show = list(map(Show.get_show, data))
        if show is None or len(show) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'show': show
        })

    @app.route('/show', methods=['POST'])
    def create_new_show():
        body = request.get_json()
        if body is None:
            abort(404)
        actor_id = body.get('actor_id', None)
        movie_id = body.get('movie_id', None)

        try:
            new_show = Show(actor_id=actor_id, movie_id=movie_id)
            new_show.insert()
            return jsonify({
                'success': True,
                'new show': [new_show.get_show()]
            })

        except Exception:
            abort(422)

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
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "code": error.error['code'],
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
