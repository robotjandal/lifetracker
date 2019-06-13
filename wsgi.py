"""
    Running the flask application through a WSGI server gunicorn.
"""
from lifetracker import create_app

app = create_app()
