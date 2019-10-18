Life Tracker
============

This app tracks attributes of a person over time.


Install
-------

Installation of project::
    # clone the repository
    $ git clone <add later>
    $ cd lifetracker

Create a virtualenv and activate it::

    $ python3 -m venv venv
    $ . venv/bin/activate


Install Life Tracker::

    $ pip install -e .

Config
------

The config/ directory contains the default.py file which is always loaded in.
The instance/config.py file is used to override the configuration set in
default.py
The production.py, development.py and test.py are example configuration files
which can be copied to instance/config.py.
> Note: INSTANCE_FOLDER cannot be overridden.

Run
---

::

    $ export FLASK_APP=lifetracker
    $ export FLASK_ENV=development
    $ export LIFETRACKER_CONFIG=<full path to project folder>/instance/config.py
    # to initialise or clear db:
    $ flask init-db
    $ flask run
    # or using gunicorn
    $ gunicorn -b 0.0.0.0:5000 -e LIFETRACKER_CONFIG="<full path to project folder>/instance/config.py" wsgi:app


Open http://127.0.0.1:5000 in a browser.

Test
----

::

    $ pip install '.[test]'
    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
