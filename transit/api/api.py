from flask import Blueprint

from transit.api.routes.transit_gateway import transit_gateway_bp

# main blueprint to be registered with application
api = Blueprint("api", __name__)

# register user with api blueprint
# api.register_blueprint(images, url_prefix="/images")
api.register_blueprint(transit_gateway_bp, url_prefix="/transit-gateways")
