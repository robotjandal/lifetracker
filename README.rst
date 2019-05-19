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

Run
---

::

    $ export FLASK_APP=lifetracker
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run


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
