from flask import Blueprint, jsonify

from flask_pydantic import validate

from transit.api.controllers.transit_gateway import TransitGatewayController

from transit.api.routes.dtos.transit_gateway import (
    RequestTransitGatewayPost,
    RequestTransitGatewayPatch,
)

transit_gateway_bp = Blueprint("transit_gateways", __name__)

transit_controller = TransitGatewayController()


@transit_gateway_bp.post("/")
@validate(body=RequestTransitGatewayPost)
def post(body: RequestTransitGatewayPost):
    try:
        transit_gateway = transit_controller.create(**vars(body))
        return jsonify(transit_gateway)
    except Exception as e:
        return jsonify(e), 500


@transit_gateway_bp.get("/<uuid>")
def get(uuid):
    try:
        transit_gateway = transit_controller.get(uuid)
    except Exception as e:
        return jsonify(str(e)), 404

    return jsonify(transit_gateway)


@transit_gateway_bp.get("/")
def get_all():
    transit_gateways = transit_controller.get_all()

    return jsonify(transit_gateways)


@transit_gateway_bp.patch("/<uuid>")
@validate(body=RequestTransitGatewayPatch)
def update(uuid, body: RequestTransitGatewayPatch):
    transit_gateway = transit_controller.update(uuid=uuid, **vars(body))

    return jsonify(transit_gateway)
