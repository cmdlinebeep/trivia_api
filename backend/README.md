# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run (for username "postgres"):
```bash
psql -U postgres trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

or in Windows:

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` program as the application. 


## Testing the Backend
To set up the database for the tests, run this the first time:
```bash
createdb -U postgres trivia_test
psql -U postgres trivia_test < trivia.psql
```

NOTE: This is for user name "postgres."  If you need to change the user name for your system, replace `postgres` above with your user name.  You will also need to Find + Replace every instance of `postgres` in the file `trivia.psql` and change it to your own user name.

And then to run the unit tests, just run:
```bash
python test_flaskr.py
```

If you ever mess up the test database somehow and need to restore it to a pristine state for testing, run the following.  Note that the current unit tests do not change the state of the database (e.g. any DB entries created for testing are cleaned up by the script too.)  So you shouldn't ever really need this:
```bash
dropdb trivia_test & createdb trivia_test
psql -U postgres trivia_test < trivia.psql
```

