from flask import Blueprint
from src.controllers.user_controller import users
from src.controllers.device_controller import devices

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(users, url_prefix="/users")
api.register_blueprint(devices, url_prefix="/devices")