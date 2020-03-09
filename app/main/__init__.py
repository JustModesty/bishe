from flask import Blueprint

main_handler = Blueprint('main_handler', __name__)

from . import views
