# Full Stack Nanodegree Capstone Project


## Casting Agency

The Casting Agency is responsible for creating movies and managing and assigning actors to those movies. As an Executive Producer within the company, you are creating a system (API only) to simplify and streamline your process.

The API does:
1. Get, post, update and delete actors in the database
2. Get, post, update and delete movies in the database

#################################### TODO ####################################
All backend code follows [PEP8 style guidelines] (https://www.python.org/dev/peps/pep-0008/)


## The API 

### API Base URL
The API is deployed on Heroku server. 
Base URL: #################################### TODO ####################################

### Authentication and Role-Based Access Control
There are two roles with different permissions:
- Casting Assistant. Allowed to:
    - view actors and movies.
- Executive Producer. Allowed to:
    - view, post, update and delete actors and movies.

The JWT for the Casting Assistant:
#################################### TODO ####################################


The JWT for the Executive Producer:
#################################### TODO ####################################
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR0SlNOMDFwLXR0VzJMbXZFbVV1ZSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY2Fwc3RvbmUyLXRlbmFudC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3MDg2NDM0MmNmYmUwMDY5MGRhMTI2IiwiYXVkIjoiZnNuZC1jYXBzdG9uZTItYXBpLWlkZW50aWZpZXIiLCJpYXQiOjE2MzU0NTYxMDQsImV4cCI6MTYzNTU0MjUwNCwiYXpwIjoiWkZQRDY1VlFHcGx3bUI3MEM2OG1KUklYRElXRWpvaWYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.czBWcSJTsKVQHEYb232LJEtxJTSM2OXFJU0pAK7GDpCvZvjmCp4EcjqGdNQgHC5Xk5S67bQ3LHGTKw_Cz864o-xnXFwAbWQtYyo534nGy3RoHYLrGcNqvH0BzK5s30ArM3r1hwqBO5wUzdh7SZQ36bpzTJPU1QK8FBB8_WuElys41QT9R7pCsGPrKdFmn3-dCoB-I0ydzr8iaGFDxoSge16cGDysvr74mjp2ykYIQrG2H8DeEzWhdVs_CKJ676Yd5r5fFIBauLpeBN2zWg3Z0q2fYS_N5WcfzEX5bZKyaTj3JrZcyYM_W5pz2M-3JitU5iqwQMzfjIjt43YCh_y8ug


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
- Sample: curl http://127.0.0.1:5000/actors

'''
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
'''


#### GET /questions
- General:
    - Returns the list of categories, the list of questions, the total number of questions and a success value.
    - The list of questions returned is paginated in groups of 10. 
- Sample: curl http://127.0.0.1:5000/questions

'''
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "In England", 
      "category": 3, 
      "difficulty": 1, 
      "id": 30, 
      "question": "Where is London?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ], 
  "success": true, 
  "total_questions": 23
}
'''


#### DELETE /questions/(question_id)
- General:
    - Delete the question with the id 'question_id' if it exists. Returns a deleted value, the id of the deleted question and a success value.
- Sample: curl http://127.0.0.1:5000/questions/5 -X DELETE

'''
{
  "deleted": true, 
  "question_deleted_id": 5, 
  "success": true
}
'''

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. 
    Returns a created value, the id of the created question and a success value.
- Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Who is Ted?", "answer": "the teacher", "category": 2, "difficulty": 1}' 

'''
{
  "created": true, 
  "created_question_id": 32, 
  "success": true
}
'''

#### POST /searched_questions
- General:
    - Searches a question that includes the searchTerm. 
    Returns the list of questions that contain the searchTerm, the total number of questions found and a success value.
- Sample: curl http://127.0.0.1:5000/searched_questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"heav"}' 

'''
{
  "current_category": "", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
'''


#### GET /categories/(category_id)/questions
- General:
    - Get all the questions for category 'category_id'
    Returns the category, the list of questions in that category, the total number of questions in the category and a success value.
- Sample: curl http://127.0.0.1:5000/categories/6/questions

'''
{
  "current_category": 6, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
'''


#### POST /quizzes
- General:
    - Get all the questions for category 'category_id'
    Returns the category, the list of questions in that category, the total number of questions in the category and a success value.
- Sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography", "id":"3"}, "previous_questions":[]}' 

'''
{
  "previousQuestions": [
    30
  ], 
  "question": {
    "answer": "In England", 
    "category": 3, 
    "difficulty": 1, 
    "id": 30, 
    "question": "Where is London?"
  }, 
  "success": true
}
'''


## Deployment 
Deployed on Heroku - see above base URL and endpoints.

# Authors
Vincent Moutel, with lots of help and parts copied from the Udacity Full-stack Nanodegree.

# Acknowledgements
Udacity and everybody on the Udacity forum


