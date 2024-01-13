## Notes

Hey there, nice to async meet y'all! This was my first time using Flask and the first time I've touched Python in a while. I got through appt creation and fetching all appointments in time. I was a little stuck on getting the first available appointment, but I got it - albeit about 30 minutes late. Following the honor code ¯\\\_(ツ)\_/¯

Improvements:

- Would like to dockerize the setup & configure real DB persistence
- I guess if the doctors were booked out for months then `/appts/first_available` could run for a long time

Configurations have been included to debug the app via the VSCode debugger & to run the test suite. Otherwise, the app runs with the default instructions below.

## Setup

1. After cloning this repository, cd into it.
2. Set up virtual environment via `python3 -m venv env`
3. Activate the virtual environment via `source env/bin/activate`
4. If it's properly set up, `which python` should point to a python under api-skeleton/env.
5. Install dependencies via `pip install -r requirements.txt`

## Starting local flask server

Under api-skeleton/src, run `flask run --host=0.0.0.0 -p 8000`

By default, Flask runs with port 5000, but some MacOS services now listen on that port.

## Running unit tests

All the tests can be run via `pytest` under api-skeleton directory.

## Code Structure

This is meant to be barebones.

- src/app.py contains the code for setting up the flask app.
- src/endpoints.py contains all the code for enpoints.
- src/models.py contains all the database model definitions.
- src/extensions.py sets up the extensions (https://flask.palletsprojects.com/en/2.0.x/extensions/)
