import ipaddress
import logging
from fastapi import APIRouter, HTTPException


from transit.api.routers.vpc_transit_gateway_route.models.request import (
    CreateVPCTransitGatewayRoutesRequest,
)

from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)
from transit.database.repositories.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentRepository,
)
from transit.database.repositories.vpc_transit_gateway_route.vpc_transit_gateway_route import (
    VPCTransitGatewayRouteRepository,
)

from transit.worker.vpc_transit_gateway_route.tasks import (
    create_vpc_transit_gateway_route_task,
    delete_vpc_transit_gateway_route_task,
)

from transit.common import utils


router = APIRouter(
    prefix="/vpc_transit_gateway_routes", tags=["vpc_transit_gateway_routes"]
)


@router.get("/")
def get_vpc_transit_gateway_routes(vpc_id: str):
    try:
        vpc_tgw_routes = VPCTransitGatewayRouteRepository().get_by_vpc_id(vpc_id)
    except Exception as e:
        logging.error(f"Error getting vpc transit gateway routes: {e}")
        raise HTTPException(
            status_code=400,
            detail="Error getting vpc transit gateway routes",
        ) from e

    return vpc_tgw_routes


@router.delete("/{vpc_tgw_route_id}")
def delete_vpc_transit_gateway_route(vpc_tgw_route_id: str):
    vpc_tgw_route_repo = VPCTransitGatewayRouteRepository()

    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    tgw_repo = TransitGatewayRepository()

    try:
        vpc_tgw_route_repo.get(ident=vpc_tgw_route_id)
    except Exception as e:
        logging.error(f"Error deleting vpc transit gateway route: {e}")
        raise HTTPException(
            status_code=400,
            detail="Error deleting vpc transit gateway route",
        ) from e

    vpc_tgw_route = vpc_tgw_route_repo.get(ident=vpc_tgw_route_id)
    tgw_vpc_att = tgw_vpc_att_repo.get(ident=vpc_tgw_route.target)
    tgw = tgw_repo.get(ident=tgw_vpc_att.transit_gateway_id)

    delete_vpc_transit_gateway_route_task.delay(
        vpc_router_id=tgw_vpc_att.vpc_router_id,
        vpc_tgw_route_id=vpc_tgw_route_id,
        destination_cidr=vpc_tgw_route.destination,
        tgw_vpc_net_ip=tgw.vpc_net_ip,
    )

    return {"message": "VPC Transit Gateway Route deleted"}


@router.post("/")
def create_vpc_transit_gateway_routes(request: CreateVPCTransitGatewayRoutesRequest):
    if not utils.is_valid_subnet(request.destination_cidr):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination CIDR {request.destination_cidr}",
        )

    if not utils.is_private_subnet(request.destination_cidr):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination CIDR {request.destination_cidr}",
        )

    vpc_tgw_route_repo = VPCTransitGatewayRouteRepository()

    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    tgw_repo = TransitGatewayRepository()

    vpc_tgw_route = vpc_tgw_route_repo.create(
        vpc_id=request.vpc_id,
        destination_cidr=request.destination_cidr,
        transit_gateway_vpc_attachment_id=request.transit_gateway_vpc_attachment_id,
        status="PENDING",
    )

    tgw_vpc_att = tgw_vpc_att_repo.get(ident=request.transit_gateway_vpc_attachment_id)
    tgw = tgw_repo.get(ident=tgw_vpc_att.transit_gateway_id)

    create_vpc_transit_gateway_route_task.delay(
        vpc_router_id=tgw_vpc_att.vpc_router_id,
        destination_cidr=request.destination_cidr,
        tgw_vpc_net_ip=tgw.vpc_net_ip,
        vpc_tgw_route_id=vpc_tgw_route.id,
    )

    return vpc_tgw_route
