# ----------------------------------------------------------------------------#
# Imports.
# ----------------------------------------------------------------------------#
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from .api import create_app   # import the app=Flask(__name__) from api.py
from .database.models import setup_db, Actor  # import funtions and models from models.py

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

        self.database_name = "db_capstone2_tests"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)        
        setup_db(self.app, self.database_path)

        # self.database_filename = "database11_test.db"
        # self.project_dir = os.path.dirname(os.path.abspath(__file__))
        # self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))
        # setup_db(self.app)   #, self.database_path)

        self.prodexec_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR0SlNOMDFwLXR0VzJMbXZFbVV1ZSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUyLXRlbmFudC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDg2NDM0MmNmYmUwMDY5MGRhMTI2IiwiYXVkIjoiZnNuZC1jYXBzdG9uZTItYXBpLWlkZW50aWZpZXIiLCJpYXQiOjE2MzQ4NTE0NzYsImV4cCI6MTYzNDkzNzg3NiwiYXpwIjoiWkZQRDY1VlFHcGx3bUI3MEM2OG1KUklYRElXRWpvaWYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.QaicViLsXjD_vJFwmEvb7h5iQFCq3Wjtj47mO4ThZlGDjrMFTcblUJ0i2OgpCvtqX94q5iPhWLirmnB_0s3P90K2TDryXz9BXScmq6KG6U5CKIkZCNDJZQAkhjztwX8RX5LfOW2zlvskK8aFWOQbG5lUlUnmaPwFA-rs6kPIlmQArTcgLzsYHPBuvBnge1nckUbTHiwighoelNdBozUroeKLCYqhTHXzzKeILrNhU0s8f6YHuEkVgRj1we-iLSW3TchbzGrHPzN3n_rrcdng26lL8ugIx9twUqux-cT18W2WLPLfg_cQRxW23TvIyQy8ePwJTdAGqUnpOQhFjnz3GQ'


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # creates a new question object, to be used
        # in the POST question tests:
        self.new_actor = {
            'name': 'Titi?',
            'age': 40,
            'gender': 'Male', 
        }
        self.update_actor = {
            'name': 'actor3newname',
            'age': 100,
            'gender': 'Male', 
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






# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


