## Notes

Hey there, nice to async meet y'all! This was my first time using Flask and the first time I've touched Python in a while. I got through appt creation and fetching all appointments. I've been kind of stuck on getting the first available appointment, so I wanted to walk through my thinking here:

1. Find doctors scheduled at time
2. If there are no doctors scheduled, set time to 8am next day, & goto 1
3. Get appointments of doctors scheduled at time
4. If there are any doctors without an appointment, return that doctor
5. Set time to end of soonest ending appointment
6. Goto 1

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
