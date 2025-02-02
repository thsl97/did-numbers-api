import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register blueprints
    from did_numbers import did_numbers_api
    app.register_blueprint(did_numbers_api.bp)

    # closes database connection when app session ends
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from did_numbers.database import db_session
        db_session.remove()

    # register commands
    from did_numbers import database
    database.init_db()

    return app
