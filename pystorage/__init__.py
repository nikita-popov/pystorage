import os

from datetime import datetime
from flask import Flask

from config import Config


def get_current_year():
    return {'current_date': datetime.today().strftime('%Y')}


def create_app(conf: Config = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(conf)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from pystorage.routes import bp as bp_routes
    app.register_blueprint(bp_routes)

    from pystorage.routes_api import bp as bp_routes_api
    app.register_blueprint(bp_routes_api)

    app.add_url_rule("/", endpoint="index")

    # For footer
    app.context_processor(get_current_year)

    return app
