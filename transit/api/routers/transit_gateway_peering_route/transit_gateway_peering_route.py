import os

import logging

import ipaddress
from typing import List

from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException

from transit.api.routers.transit_gateway_peering_attachment.models.request import (
    TransitGatewayPeeringAttachmentCreateRequest,
)
from transit.database.models.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentModel,
)
from transit.database.repositories.transit_gateway_peering_attachment.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentRepository,
)

from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)


from transit.drivers.vytransit.vytransit_driver import VyTransitDriver

load_dotenv()

router = APIRouter(
    prefix="/transit_gateway_peering_routes",
    tags=["transit_gateway_peering_routes"],
)


@router.post("/")
def create(request: TransitGatewayPeeringAttachmentCreateRequest):
    tgw_peer_attachment_repo = TransitGatewayPeeringAttachmentRepository()
    tgw_repo = TransitGatewayRepository()

    pass
