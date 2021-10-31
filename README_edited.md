# Full Stack Nanodegree Capstone Project


## Casting Agency

The Casting Agency is responsible for creating movies and managing and assigning actors to those movies. As an Executive Producer within the company, you are creating a system (API only) to simplify and streamline your process.

The API does:
1. Get, post, update and delete actors in the database
2. Get, post, update and delete movies in the database

All backend code follows [PEP8 style guidelines] (https://www.python.org/dev/peps/pep-0008/)


## The API 

### API Base URL
The API is deployed on Heroku server. 
Base URL: https://fsnd-capstone2-heroku-app.herokuapp.com

### Authentication and Role-Based Access Control
There are two roles with different permissions:
- Casting Assistant. Allowed to:
    - view actors and movies.
- Executive Producer. Allowed to:
    - view, post, update and delete actors and movies.

The JWT for the Casting Assistant: see setup.sh
The JWT for the Executive Producer: see setup.sh

### Run the API locally
In order to run the API locally, navigate to the 'FSND_Capstone2' folder and run the following commands:
- Install virtual env:
'''
$ pip3 install virtualenv
$ python3 -m virtualenv venv
$ source venv/bin/activate
'''
- Install dependencies:
'''
$ pip3 install -r requirements.txt
'''
- Create Postgres database:
'''
$ createdb new_database_name
'''
- Update database name 'database_name' in models.py
- Run Flask app:
'''
$ export FLASK_APP=src.api.py
$ export FLASK_ENV=development
$ flask run
'''


### Tests
In order to run tests locally, 
- Duplicate the Postgres database:
'''
$ psql database_name
psql> \l
psql> CREATE DATABASE database_name_for_tests WITH TEMPLATE database_name;
'''
- Update database name 'database_name' in test_api.py
- Navigate to the 'FSND_Capstone2' folder and run the following commands:
'''
$ python3 -m src.test_api
'''


### Deploy the API on Heroku
In order to deploy the API on Heroku, navigate to the 'FSND_Capstone2' folder and run the following commands:
- Login Heroku:
'''
$ heroku login
'''
- Create the Heroku app:
'''
$ heroku create fsnd-capstone2-heroku-app
'''
- Create an Heroku database:
'''
$ heroku addons:create heroku-postgresql:hobby-dev
'''
- Deploy the app:
$ git add .
$ git commit -m 'comment'
$ git push heroku master
'''



## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
'''
{
    "success": False,
    "error": 400,
    "message": "bad request"
}

The API will return three error types when requests fail:
- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable


### Endpoints

#### GET /actors
- General:
    - Returns a list of actors names, age and gender, and a success value.

'''
[
    {
        "actors": [
            {
                "age": 55,
                "gender": "Male",
                "id": 1,
                "name": "Eddie Dean"
            },
            {
                "age": 35,
                "gender": "Male",
                "id": 2,
                "name": "Tim Pum"
            },
            {
                "age": 45,
                "gender": "Female",
                "id": 3,
                "name": "Ella Shu"
            },
            {
                "age": 30,
                "gender": "Female",
                "id": 4,
                "name": "Dina Gove"
            },
            {
                "age": 20,
                "gender": "Female",
                "id": 5,
                "name": "Ola Titi"
            }
        ],
        "success": true
    },
    200
]
'''

#### GET /movies
- General:
    - Returns the list of movies (title and release date) and a success value.

'''
[
    {
        "movies": [
            {
                "id": 1,
                "release_date": "Sun, 29 Oct 2000 00:00:00 GMT",
                "title": "James Bond 1"
            },
            {
                "id": 2,
                "release_date": "Wed, 03 Mar 2004 00:00:00 GMT",
                "title": "James Bond 2"
            },
            {
                "id": 3,
                "release_date": "Fri, 06 Jun 2008 00:00:00 GMT",
                "title": "James Bond 3"
            },
            {
                "id": 4,
                "release_date": "Sun, 01 Feb 1970 23:00:00 GMT",
                "title": "Alice in Wonderland"
            },
            {
                "id": 5,
                "release_date": "Fri, 02 Feb 2018 00:00:00 GMT",
                "title": "Upsy Daisy"
            }
        ],
        "success": true
    },
    200
]
'''

#### DELETE /actors/(actor_id)
- General:
    - Delete the actor with the id 'actor_id' if it exists. Returns a deleted value, the id of the deleted actor and a success value.

'''
[
    {
        "actor": {
            "age": 30,
            "gender": "Female",
            "id": 4,
            "name": "Dina Gove"
        },
        "success": true
    },
    200
]
'''

#### DELETE /movies/(movie_id)
- General:
    - Delete the movie with the id 'movie_id' if it exists. Returns a deleted value, the id of the deleted movie and a success value.

'''
[
    {
        "movie": {
            "id": 4,
            "release_date": "Sun, 01 Feb 1970 23:00:00 GMT",
            "title": "Alice in Wonderland"
        },
        "success": true
    },
    200
]
'''

#### POST /actors
- General:
    - Creates a new actor (name, age and gender). 
    Returns a created value, the id of the created actor and a success value.

'''
[
    {
        "actor": {
            "age": 70,
            "gender": "Male",
            "id": 6,
            "name": "Didier Nala"
        },
        "success": true
    },
    200
]
'''

#### POST /movies
- General:
    - Creates a new movie (title and release_date). 
    Returns a created value, the id of the created movie and a success value.

'''
[
    {
        "movie": {
            "id": 6,
            "release_date": "Mon, 07 Jul 1980 00:00:00 GMT",
            "title": "Happy Ferry"
        },
        "success": true
    },
    200
]
'''

#### PATCH /actors/(actor_id)
- General:
    - Updates the actor with the id 'actor_id' if it exists (name, age and gender). 
    Returns a created value, the id of the updated actor and a success value.

'''[
    {
        "actor": {
            "age": 99,
            "gender": "Female",
            "id": 2,
            "name": "Filipa"
        },
        "success": true
    },
    200
]
'''

#### PATCH /movies/(movie_id)
- General:
    - Updates the movie with the id 'movie_id' if it exists (title and release_date). 
    Returns a created value, the id of the updated movie and a success value.

'''
[
    {
        "movie": {
            "id": 2,
            "release_date": "Wed, 01 Jan 2003 00:00:00 GMT",
            "title": "James Bond 2"
        },
        "success": true
    },
    200
]
'''


## Deployment 
Deployed on Heroku - see above base URL and endpoints.

# Authors
Vincent Moutel, with lots of help and parts copied from the Udacity Full-stack Nanodegree.

# Acknowledgements
Udacity and everybody on the Udacity forum


