import os
import logging
from flask import Flask


def create_app(test_config=None):
    """Create and configure Flask application for life tracking."""
    app = Flask(__name__, instance_relative_config=True)
    # self.logger = logging.getLogger('my_flask_ext_logger')
    app.logger.setLevel(logging.DEBUG)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "lifetracker.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
