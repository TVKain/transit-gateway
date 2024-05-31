from flask import Blueprint, Response, json

from ..controllers.health_check_controllers import health_checks 


# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(health_checks, url_prefix="/health-checks")
