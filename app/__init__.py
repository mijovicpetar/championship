"""Root package."""

import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy


# Initialize extensions.
# For database and ORM:
DB = SQLAlchemy()


def create_app(config_type):
    """App factory.

    Args:
        config_type: Name of the config file without extension.
    Returns:
        App object.
    """
    # Create app with specified configuration.
    app = FlaskAPI(__name__)

    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')
    app.config.from_pyfile(configuration)

    # Initialize extensions for current app.
    DB.init_app(app)

    # Import and register blueprints.
    from app.championship import data_management
    app.register_blueprint(data_management)

    return app
