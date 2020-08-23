# Casting Agency Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

## Project Motivation
The Casting Agency Project models a company that is responsible for creating movies and managing and assigning actors to those movies. The permissions in this project are created and managed on [Auth0](https://auth0.com). The project includes configuration files to deploy it on [Heroku](https://heroku.com).

## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.
* Secrets are stored as environment variables.


### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment


### Running Locally

#### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

# Virtual Environment (venv)
- Once you have your virtual environment setup,  
- To create virtual environment: 
```bash
   py -m venv env 
- to activate:
  source env/Scripts/activate
```
# PIP Dependecies
- Once you have your venv setup and running, install dependencies by navigating
to the root directory and running:
```bash
   pip3 install -r requirements.txt
```
- This will install all of the required packages included in the requirements.txt file.
# Local Testing
- To test your local installation, run the following command from the root folder:

python test_app.py
- If all tests pass, your local installation is set up correctly.
# Running the server
- From within the root directory, first ensure you're working with your created
venv. To run the server, execute the following:

export FLASK_APP=app
export FLASK_DEBUG=true
export FLASK_ENV=development
flask run


## Casting Agency Specifications

### Models

- Movies with attributes title and release date
- Actors with attributes name, age and gender

### Endpoints

- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/
  
### Roles

- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

### Tests

- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

#### Auth0 Setup


To create you own auth0 follow these steps:

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token

Environment variables needed: (setup.sh)

```bash
export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="capstone" # Create an API in Auth0
```

##### Roles

Create three roles for users under `Users & Roles` section in Auth0
 Create new API permissions:
    - `get:movie`
    - `post:movie`
    - `patch:movie`
    - `delete:movie`
    - `get:actor`
    - `post:actor`
    - `patch:actor`
    - `delete:actor`
    - `get:show`
    - `post:show`

 Create new roles for:
    - Casting Assistant
        - can `get:actor`
        - can `get:movie`
        - can `get:show`
    - Casting Director
        - can perform all Casting Assistant actions
        - can `add:actor`
        - can `delete:actor`
        - can `patch:actor`
        - can `patch:movie`
    - ExecutiveProducer
        - can perform all actions

# API Reference 

## Getting Started 

- **Base URL**: Base URL: Actually, this app can be run locally and it is hosted also as a base URL using heroku (the heroku URL is https://capstoneprojectapplication.herokuapp.com/). 

## Error Handling

Errors are returned as JSON object in the following format:

```json
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return four(04) error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not allowed
- 422: Not Processable
- 401: Unathurize User
- 403: Insufficient Permission
  
## Endpoints

- GET '/actor'
- GET '/movie'
- POST '/actor'
- POST '/movie'
- PATCH '/actor/{actor_id}'
- PATCH '/movie/{movie_id}'
- DELETE '/actor/{actor_id}'
- DELETE '/movie/{movie_id}'
#### We added this Endpoint
- GET '/show'
- POST '/show'


### GET /actor

- General:
    - Returns a list of actor objects, success value
    - It accessed only by user with permission 'get:actor'

```json
return jsonify({
        'success': True,
        'actor': actor
    })
```

### GET /movie

- General:
    - Returns a list of movie objects, success value
    - It accessed only by user with permission 'get:movie'
  
```json
return jsonify({
        'success': True,
        'movie': movie
    })
```

### POST /actor

- General:
    - Including a body that contains id, name, age, gender
    - Returns the new actor object and success value
    - It accessed only by user with permission 'post:actor'

Here is a returned sample fromat

```json
{
  "actor": [
    {
      "age": 26,
      "gender": "Female",
      "id": 2,
      "name": "reema"
    }
  ],
  "success": true
}
```

### POST /movie

    - Including a body that contains id,title, release_date

    - Returns the new movie object and success value
    - It accessed only by user with permission 'post:movie'

Here is a result sample format:

```json
{
  "movie": [
    {
      "id": 3,
      "release_date": "1992",
      "title": "Barbie"
    }
  ],
  "success": true
}
```


### PATCH /actor/<actor_id>

- Require the 'patch:actor' permission
- Update an existing row in the actor table
- Contain the actor.get_actor data representation
returns status code 200 and json `{"success": True, "actor": actor}` where actor an array containing only the updated actor
or appropriate status code indicating reason for failure

He is a sample for a  modified actor in a format:

```json
{
  "actor": [
    {
      "age": 25,
      "gender": "Male",
      "id": 2,
      "name": "Maohammed"
    }
  ],
  "success": true
}
```

### PATCH /movie/<movie_id>

- Require the `patch:movie` permission
returns status code 200 and json `{"success": True, "movie": movie}` where movie an array containing only the updated movie
or appropriate status code indicating reason for failure

Here is an example of the modified movie  in a format: 

```json
{
  "movie": [
    {
      "id": 2,
      "release_date": "2014",
      "title": "The superwomwn"
    }
  ],
  "success": true
}
```

### DELETE /actor/<actor_id>

- Require the `delete:actor` permission
- Delete the corresponding row for `<actor_id>` where `<actor_id>` is the existing model id
- Respond with a 404 error if `<actor_id>` is not found
- Returns status code 200 and json `{"success": True, "deleted": actor_id}` where id is the id of the deleted record
or appropriate status code indicating reason for failure

```json
return jsonify({
    "success": True,
    "deleted": actor_id
})
```

### DELETE /movie/<movie_id>

- Require the `delete:movie` permission
- Delete the corresponding row for `<movie_id>` where `<movie_id>` is the existing model id
- Respond with a 404 error if `<movie_id>` is not found
- Returns status code 200 and json `{"success": True, "deleted": id}` where id is the id of the deleted record
or appropriate status code indicating reason for failure

```json
return jsonify({
    "success": True,
    "deleted": movie_id
})
```


### GET /show
- the show table contains the relation between the actor and the movie "many to many"
- Require the `get:show` permission and returns a list of show
  
```json
return jsonify({
    "show": [
        {
            "actor_id": 2,
            "movie_id": 2
        }
      ],
    "success": true
    })
```

### POST /show

- Require the `post:show` permission
- Contain the actor_id and movie_id data representation
returns status code 200 and json `{"success": True, "new show":new show` where actor an array containing only the newly created actor or appropriate status code indicating reason for failure

Here is a returned sample fromat

```json
{
    "new show": [
        {
            "actor_id": 2,
            "movie_id": 3
        }
    ],
    "success": true
}
```
