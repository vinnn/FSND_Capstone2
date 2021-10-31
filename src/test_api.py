# ----------------------------------------------------------------------------#
# Imports.
# ----------------------------------------------------------------------------#
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from .api import create_app   # import the app=Flask(__name__) from api.py
from .database.models import setup_db, Actor, Movie  # import funtions and models from models.py


# ----------------------------------------------------------------------------#
# Test Class.
# ----------------------------------------------------------------------------#
class CastingTestCase(unittest.TestCase):
    """This class represents the Casting test case"""

    # Setup.
    # ----------------------------------------#
    def setUp(self):
        """Executed before each test. 
        Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client

        #  POSTGRES DATABASE SETUP  ###################################
        self.database_name = "db_capstone2_tests"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)        
        setup_db(self.app, self.database_path)

        #  SQLITE DATABASE SETUP  ###################################
        # self.database_filename = "database11_test.db"
        # self.project_dir = os.path.dirname(os.path.abspath(__file__))
        # self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))
        # setup_db(self.app)   #, self.database_path)

        # JWT
        self.prodexec_jwt = os.environ.get('ExecutiveProducer_jwt')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # creates a new actor and movie object, to be used
        # in the POST and PATCH tests:
        self.new_actor = {
            'name': 'Tititutu?',
            'age': 40,
            'gender': 'Male', 
        }
        self.update_actor = {
            'name': 'actor3newname',
            'age': 100,
            'gender': 'Male', 
        }
        self.new_movie = {
            'title': 'SuperPupsitu',
            'release_date': "9-9-2009"
        }
        self.update_movie = {
            'title': 'movie3newtitle',
            'release_date': "1-1-1990" 
        }

    # Teardown.
    # ----------------------------------------#    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test. [GET NON-EXISTENT URL => ERROR ]
    # ----------------------------------------#    
    def test_404_nonexistent_url(self):
        # Get response by making client make the GET request:    
        res = self.client().get('/actors2',
            headers={'Authorization':'Bearer'+ self.prodexec_jwt}
            )
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test. [GET ACTORS => OK ]
    # ----------------------------------------#    
    def test_200_get_actors(self):
        # Get response by making client make the GET request:
        res = self.client().get('/actors',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}
            )
        
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)
        self.assertTrue(data[0]['actors'])  # check the result contains 'actors' dictionary


    # Test. [POST ACTOR id => OK ]
    # ----------------------------------------#    
    def test_200_post_actor(self):
        # Get response by making client make the 
        # POST request (new_question is defined above):
        res = self.client().post('/actors', 
            json=self.new_actor,
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)


    # Test. [POST ACTOR WITH NO INFO => ERROR ]
    # ----------------------------------------#    
    def test_422_post_wrong_actor_info(self):
        # Get response by making client make the 
        # POST request, without json input info:
        res = self.client().post('/actors', 
            json='wrongactor',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test. [PATCH ACTOR id => OK ]
    # ----------------------------------------#    
    def test_200_patch_actor(self):
        # Get response by making client make the 
        # PATCH request (update_actor is defined above):
        res = self.client().patch('/actors/3', 
            json=self.update_actor,
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )

        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)


    # Test. [PATCH ACTOR WITH NO INFO => ERROR ]
    # ----------------------------------------#    
    def test_422_patch_no_patchdata(self):
        # Get response by making client make the 
        # PATCH request, without json input info:
        res = self.client().patch('/actors/3', 
            json='wrongpatch',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )

        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Test. [DELETE ACTOR id => OK ]
    # ----------------------------------------#    
    # def test_200_delete_actor(self):
        # Get response by making client make the DELETE request:
        # res = self.client().delete('/actors/8',
        #     headers={'Authorization':'Bearer '+ self.prodexec_jwt}
        #     )        

        # # Load the data using json.loads:
        # data = json.loads(res.data)

        # # check responses:
        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(data[0]['success'], True)


    # Test. [DELETE NON-EXISTENT ACTOR => ERROR ]
    # ----------------------------------------#    
    def test_404_delete_nonexistent_actor(self):
        # Get response by making client make the GET request:
        res = self.client().delete('/actors/2000',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}
            )                
        # Load the data using json.loads:
        data = json.loads(res.data)

        # print("DATA : ")
        # print(data)

        # check responses:
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

















    # Test. [GET MOVIES => OK ]
    # ----------------------------------------#    
    def test_200_get_movies(self):
        # Get response by making client make the GET request:
        res = self.client().get('/movies',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}
            )
        
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)
        self.assertTrue(data[0]['movies'])  # check the result contains 'actors' dictionary


    # Test. [POST MOVIE id => OK ]
    # ----------------------------------------#    
    def test_200_post_movie(self):
        # Get response by making client make the 
        # POST request (new_movie is defined above):
        res = self.client().post('/movies', 
            json=self.new_movie,
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)


    # Test. [POST MOVIE WITH NO INFO => ERROR ]
    # ----------------------------------------#    
    def test_422_post_wrong_movie_info(self):
        # Get response by making client make the 
        # POST request, without json input info:
        res = self.client().post('/movies', 
            json='wrongmovie',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )
        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test. [PATCH ACTOR id => OK ]
    # ----------------------------------------#    
    def test_200_patch_movie(self):
        # Get response by making client make the 
        # PATCH request (update_actor is defined above):
        res = self.client().patch('/movies/3', 
            json=self.update_movie,
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )

        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['success'], True)


    # Test. [PATCH MOVIE WITH NO INFO => ERROR ]
    # ----------------------------------------#    
    def test_422_patch_no_patchdata(self):
        # Get response by making client make the 
        # PATCH request, without json input info:
        res = self.client().patch('/movies/3', 
            json='wrongpatch',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}            
            )

        # Load the data using json.loads:
        data = json.loads(res.data)

        # check responses:
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    # Test. [DELETE MOVIE id => OK ]
    # ----------------------------------------#    
    # def test_200_delete_movie(self):
        # Get response by making client make the DELETE request:
        # res = self.client().delete('/movies/8',
        #     headers={'Authorization':'Bearer '+ self.prodexec_jwt}
        #     )        

        # # Load the data using json.loads:
        # data = json.loads(res.data)

        # # check responses:
        # self.assertEqual(res.status_code, 200)
        # self.assertEqual(data[0]['success'], True)


    # Test. [DELETE NON-EXISTENT MOVIE => ERROR ]
    # ----------------------------------------#    
    def test_404_delete_nonexistent_movie(self):
        # Get response by making client make the GET request:
        res = self.client().delete('/movies/2000',
            headers={'Authorization':'Bearer '+ self.prodexec_jwt}
            )                
        # Load the data using json.loads:
        data = json.loads(res.data)

        # print("DATA : ")
        # print(data)

        # check responses:
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

























# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


