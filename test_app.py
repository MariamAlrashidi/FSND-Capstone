import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import db, db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth
import logging
from settingup import CASTING_ASSISTANT_JWT
from settingup import CASTING_DIRECTOR_JWT
from settingup import EXECUTIVE_PRODUCER_JWT


casting_assistant_token = CASTING_ASSISTANT_JWT
casting_director_token = CASTING_DIRECTOR_JWT
executive_producer_token = EXECUTIVE_PRODUCER_JWT


def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client


# define set authetification method


def settingup_auth(role):
    JWT = ''
    if role == 'casting_assistant':
        JWT = casting_assistant_token
    elif role == 'casting_director':
        JWT = casting_director_token
    elif role == 'executive_producer':
        JWT = executive_producer_token

    return {
        "Content-Type": "application/json",
        'Authorization': 'Bearer {}'.format(JWT)
    }


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        database_name = "casting_agency"
        self.database_path = "postgres://postgres:1234567890@{}/{}".format('localhost:5432', database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "name": "Test acotor",
            "age": 22,
            "gender": "Male"
        }
        self.new_movie = {
            "title": "Test movie"
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()
            
    def tearDown(self):
        pass
    ################################################
    #####           Actor Tests                #####
    ################################################
    # test get actor end point

    def test_get_all_actor_casting_assistant(self):
        res = self.client().get('/actor',
                                headers=settingup_auth("casting_assistant"))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))


    def test_get_all_actor_casting_director(self):
        res = self.client().get('/actor',
                                headers=settingup_auth("casting_director"))

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_get_actor_all_executive_producer(self):
        res = self.client().get('/actor',
                                headers=settingup_auth("executive_producer"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_401_get_all_actor_unsuccessful(self):
        res = self.client().get('/actor', headers=settingup_auth(''))
        self.assertEqual(res.status_code, 401)

    # test post actor end point
    def test_401_create_actor_casting_assistant(self):
        res = self.client().post('/actor', json=self.new_actor,
                                 headers=settingup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)

    def test_create_actor_executive_producer(self):
        res = self.client().post('/actor', json=self.new_actor,
                                 headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        
    def test_404_create_actor_unsuccessful(self):
        res = self.client().post('/actor', json={},
                                 headers=settingup_auth('casting_director'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # test patch actor end point
    def test_401_update_actor_casting_assistant(self):
        actor = Actor('malek', 23, 'Male')
        actor.insert()
        res = self.client().patch('/actor/'+str(actor.id), json={'age': 23},
                                  headers=settingup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)

    def test_update_actor_casting_director(self):
        actor = Actor('malek', 23, 'Male')
        actor.insert()
        res = self.client().patch('/actor/'+str(actor.id), json={'age': 23},
                                  headers=settingup_auth('casting_director'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(actor.get_actor()['age'], 23)

    def test_update_actor_executive_producer(self):
        actor = Actor('malek', 23, 'Male')
        actor.insert()
        res = self.client().patch('/actor/'+str(actor.id), json={'age': 23},
                                  headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.age, 23)


    def test_404_update_actor_unsuccessful(self):
        res = self.client().patch('/actor/100', json={},
                                  headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test delete actor end point
    def test_401_drop_actor_casting_assistant(self):
        actor = Actor('malek', 23, 'Male')
        actor.insert()
        res = self.client().delete('/actor/'+str(actor.id),
                                   headers=settingup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)

    def test_drop_actor_casting_director(self):
        actor = Actor('malek', 23, 'Male')
        actor.insert()
        res = self.client().delete('/actor/'+str(actor.id),
                                   headers=settingup_auth('casting_director'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['deleted']), actor.id)

    def test_drop_actor_executive_producer(self):
        actor = Actor('malek', 23, 'Male')
        actor.insert()
        res = self.client().delete('/actor/'+str(actor.id),
                                   headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['deleted']), actor.id)


    def test_401_drop_actor_unsuccessful(self):
        actor = Actor('malek', 23, 'Male')
        actor.insert()
        res = self.client().delete('/actor/'+str(actor.id), headers=settingup_auth(''))
        self.assertEqual(res.status_code, 401)

    ###############################################
    ####           Movie Tests                #####
    ###############################################

    def test_get_all_movie_casting_assistant(self):
        res = self.client().get('/movie',
                                headers=settingup_auth("casting_assistant"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_get_all_movie_executive_producer(self):
        res = self.client().get('/movie',
                                headers=settingup_auth("executive_producer"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_get_all_movie_casting_director(self):
        res = self.client().get('/movie',
                                headers=settingup_auth("casting_director"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_get_all_movie_unsucessful(self):
        res = self.client().get('/movie', headers=settingup_auth(''))
        self.assertEqual(res.status_code, 401)

    def test_create_movie_executive_producer(self):
        res = self.client().post('/movie', json=self.new_movie,
                                 headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_401_create_movie_casting_assistant(self):
        res = self.client().post('/movie', json=self.new_movie,
                                 headers=settingup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)

    def test_401_create_movie_casting_director(self):
        res = self.client().post('/movie', json=self.new_movie,
                                 headers=settingup_auth('casting_director'))
        self.assertEqual(res.status_code, 401)


    def test_401_create_movies_fail(self):
        res = self.client().post('/movie', json={},
                                 headers=settingup_auth(''))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_movie_casting_director(self):
        movie = Movie(title='first Name')
        movie.insert()

        res = self.client().patch('/movie/'+str(movie.id),
                                  json={'title': 'updated_movie'},
                                  headers=settingup_auth('casting_director'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], 'updated_movie')

    def test_update_movie_executive_producer(self):
        movie = Movie(title='first Name')
        movie.insert()

        res = self.client().patch('/movie/'+str(movie.id),
                                  json={'title': 'updated_movie'},
                                  headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], movie.id)
        self.assertEqual(data['movie']['title'], 'updated_movie')

    def test_401_update_movie_casting_assistant(self):
        movie = Movie(title='first Name')
        movie.insert()
        res = self.client().patch('/movie/'+str(movie.id),
                                  json={'title': 'updated_movie'},
                                  headers=settingup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)


    def test_404_update_movie_fail(self):
        movie = Movie(title='first Name')
        movie.insert()

        res = self.client().patch('/movie/100000', json={},
                                  headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie_executive_producer(self):
        movie = Movie(title='first Name')
        movie.insert()
        res = self.client().delete('/movie/'+str(movie.id),
                                   headers=settingup_auth('executive_producer'))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(int(data['deleted']), movie.id)

    def test_delete_movie_casting_assistant(self):
        movie = Movie(title='first Name')
        movie.insert()

        res = self.client().delete('/movie/'+str(movie.id),
                                   headers=settingup_auth('casting_assistant'))
        self.assertEqual(res.status_code, 401)

    def test_401_delete_movie_casting_director(self):
        movie = Movie(title='first Name')
        movie.insert()

        res = self.client().delete('/movie/'+str(movie.id),
                                   headers=settingup_auth('casting_director'))
        self.assertEqual(res.status_code, 401)


    def test_401_delete_movie_fail(self):
        movie = Movie(title='first Name')
        movie.insert()

        res = self.client().delete('/movie/'+str(movie.id),
                                     headers=settingup_auth(''))
        self.assertEqual(res.status_code, 401)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()