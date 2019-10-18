Life Tracker
============

Deploy
------

This project can be deployed to a Docker container with gunicorn.

To build the image tagged with lifetracker (from the project root directory):
    $ docker build -f deploy/Dockerfile  -t lifetracker .

To run the lifetracker container:
    $ docker run -p 5000:5000 lifetracker

