# FSND-Capstone-Project

This project is the final project of the Udacity Full Stack Developer Nano Degree Program. The goal of this project is to deploy a Flask application with Heroku/PostgreSQL and enable Role Based Authentication and roles-based access control (RBAC) with Auth0 (third-party authentication systems).

I have impelemented a Roommate Finder, an API that collects information on tenants and potential roommates to match them up to rentable properties. Tenants and Landlords may put properties up for rent, and Roommates may contact either of the above through the website to set up lodging.

## Getting Started

Auth0 Login URL: https://still-butterfly-7094.us.auth0.com/authorize?audience=udacityfinal&response_type=token&client_id=MAber3rpaDvIGkAtTP8pQVd5ttmR0xOs&redirect_uri=http://localhost:8080

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for the platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
$ pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Running the server

first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

Sourcing `setup.sh` sets some environment variables used by the app.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the this file to find the application.

## Models:

- **Rentals** model defined with attributes Address and Rent
- **Renters** model defined with attributes Name, Age and Gender

You can find the models in `models.py` file. Local Postgres **DATABASE** details are available in `setup.sh` file for reference.

## Endpoints:

```python
GET /actors &  /movies
DELETE /actors/<int:id> & /movies/<int:id>
POST /actors & /movies
PATCH /actors/<int:id> & /movies/<int:id>
```

All below Endpoints have been created, please refer `app.py` file.

## Auth0 Setup:

**AUTH0_DOMAIN**, **ALGORITHMS** and **API_AUDIENCE** are all available in the `setup.sh` file for reference.
Json Web Tokens: You can find **JWTs** for each role in the `setup.sh` file to run the app locally.

**Roles**: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

- **Landlord** \* get:actors and get:movies
- **Tenant**
  _ All permissions a Landlord has and
  _ post:actors and delete:actors \* patch:actors and patch:movies
- **Roommate**
  _ All permissions a Tenant has and
  _ post:movies and delete:movies

## Deployment Details:

- App is deployed to [Heroku](https://harsh-casting-agency.herokuapp.com/ "Heroku").
- Heroku Postgres **DATABASE** details are available in `setup.sh` file for reference.

Use the above stated endpoints and append to this link above to execute the app either thru CURL or Postman.
For example:

```bash
$ curl -X GET https://harsh-casting-agency.herokuapp.com//actors?page=1
$ curl -X POST https://harsh-casting-agency.herokuapp.com//actors
$ curl -X PATCH https://harsh-casting-agency.herokuapp.com//actors/1
$ curl -X DELETE https://harsh-casting-agency.herokuapp.com//actors/1
```

Similarly, you can build these for /movies endpoints too.

## Testing:

We can run our entire test case by running the following command at command line

```python
$ dropdb castagency
$ createdb castagency
$ psql castagency < db.psql
$ python test_app.py
```

### Thank You!