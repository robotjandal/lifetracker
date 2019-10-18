import os
import logging
from flask import Flask


def create_app(test_config=None, instance_path=None):
    """Create and configure Flask application for life tracking."""

    app = Flask(__name__)

    # Load the default configuration
    app.config.from_object("config.default")
    app.instance_path = app.config["INSTANCE_FOLDER"]

    if not os.environ.get("LIFETRACKER_CONFIG"):
        raise FileNotFoundError("LIFETRACKER_CONFIG not found")
    app.config.from_envvar("LIFETRACKER_CONFIG", silent=True)

    # Set debug level
    if app.config["DEBUG_LEVEL"] == "CRITICAL":
        app.logger.setLevel(logging.CRITICAL)
    elif app.config["DEBUG_LEVEL"] == "ERROR":
        app.logger.setLevel(logging.ERROR)
    elif app.config["DEBUG_LEVEL"] == "WARNING":
        app.logger.setLevel(logging.WARNING)
    elif app.config["DEBUG_LEVEL"] == "INFO":
        app.logger.setLevel(logging.INFO)
    elif app.config["DEBUG_LEVEL"] == "DEBUG":
        app.logger.setLevel(logging.DEBUG)

    logging.basicConfig(
        filename=app.instance_path + "/lifetracker.log", level=logging.DEBUG
    )
    # set database
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "lifetracker.sqlite")
    )

    if app.config["TESTING"]:
        # load the test config if passed in
        app.config.update(test_config)
        app.config.from_object("config.test")
    else:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)
        app.config.from_envvar("LIFETRACKER_CONFIG", silent=True)
        # app.config.from_object(config, silent=True)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from lifetracker import db

    db.init_app(app)
    # db.init_app(app)

    # apply the blueprints to the app
    from lifetracker import auth, goals, progress

    app.register_blueprint(auth.bp)
    app.register_blueprint(goals.bp)
    app.register_blueprint(progress.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
