"""Auth package."""

from flask import Blueprint

data_management = Blueprint(
    'data_management', __name__, template_folder="templates")

from app.championship import routes
