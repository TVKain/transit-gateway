import ipaddress
from fastapi import APIRouter, HTTPException

from transit.api.routers.transit_gateway_vpc_route.models.request import (
    CreateTransitGatewayVPCRoutesRequest,
)
from transit.database.repositories.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentRepository,
)
from transit.database.repositories.transit_gateway_vpc_route.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteRepository,
)

from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)

from transit.drivers.vytransit.vytransit_driver import VyTransitDriver

from transit.worker.transit_gateway_vpc_route.tasks import (
    create_transit_gateway_vpc_route_task,
    delete_transit_gateway_vpc_route_task,
)

from transit.common import utils


router = APIRouter(
    prefix="/transit_gateway_vpc_routes", tags=["transit_gateway_vpc_routes"]
)


def _check_tgw_vpc_route_overlap(tgw_id: str, destination_cidr: str):

    tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()

    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    tgw_vpc_atts = tgw_vpc_att_repo.get_all(tgw_id)

    destination_cidr_ip = ipaddress.ip_network(destination_cidr)
    for tgw_vpc_att in tgw_vpc_atts:
        tgw_vpc_routes = tgw_vpc_route_repo.get_all_by_tgw_att_id(tgw_vpc_att.id)

        for tgw_vpc_route in tgw_vpc_routes:
            if ipaddress.ip_network(tgw_vpc_route.destination).overlaps(
                destination_cidr_ip
            ):
                return True

    return False


@router.post("/")
def create_transit_gateway_vpc_routes(request: CreateTransitGatewayVPCRoutesRequest):
    if not utils.is_valid_subnet(request.destination_cidr):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid destination CIDR {request.destination_cidr}",
        )

    if not utils.is_private_subnet(request.destination_cidr):
        raise HTTPException(
            status_code=400,
            detail=f"Destination CIDR {request.destination_cidr} not in private address range",
        )

    tgw_repo = TransitGatewayRepository()

    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    try:
        tgw_vpc_att = tgw_vpc_att_repo.get(request.vpc_attachment_id)

        if not tgw_vpc_att:
            raise Exception(
                f"Transit Gateway VPC Attachment not found for id {request.vpc_attachment_id}"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}") from e

    try:
        tgw = tgw_repo.get(tgw_vpc_att.transit_gateway_id)

        if not tgw:
            raise Exception(
                f"Transit Gateway not found for VPC Attachment {request.vpc_attachment_id}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}",
        ) from e

    if _check_tgw_vpc_route_overlap(tgw.id, request.destination_cidr):
        raise HTTPException(
            status_code=400, detail=f"Overlapping route for transit gateway {tgw.id}"
        )

    tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()

    tgw_vpc_route = tgw_vpc_route_repo.create(
        vpc_attachment_id=request.vpc_attachment_id,
        destination_cidr=request.destination_cidr,
        status="PENDING",
    )

    create_transit_gateway_vpc_route_task.delay(
        tgw_vpc_route_id=tgw_vpc_route.id,
        tgw_vpc_att_id=request.vpc_attachment_id,
        destination_cidr=request.destination_cidr,
    )

    return tgw_vpc_route


@router.get("/")
def get_transit_gateway_vpc_routes(transit_gateway_id: str | None = None):
    tgw_repo = TransitGatewayRepository()
    if transit_gateway_id:
        try:
            tgw = tgw_repo.get(transit_gateway_id)

            if not tgw:
                raise Exception(
                    f"Transit Gateway not found for id {transit_gateway_id}"
                )

            return TransitGatewayVPCRouteRepository().get_all_by_tgw_id(
                transit_gateway_id
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{str(e)}") from e

    else:
        return TransitGatewayVPCRouteRepository().get_all()


@router.delete("/{tgw_vpc_route_id}")
def delete_transit_gateway_vpc_routes(tgw_vpc_route_id: str):
    tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()

    try:
        tgw_vpc_route = tgw_vpc_route_repo.get(tgw_vpc_route_id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway VPC Route not found for id {tgw_vpc_route_id}",
        ) from e

    try:
        tgw_vpc_att = TransitGatewayVPCAttachmentRepository().get(tgw_vpc_route.target)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway VPC Attachment not found for id {tgw_vpc_route.target}",
        ) from e

    try:
        tgw = TransitGatewayRepository().get(tgw_vpc_att.transit_gateway_id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway not found for VPC Attachment {tgw_vpc_att.id}",
        ) from e

    TransitGatewayVPCRouteRepository().update(tgw_vpc_route_id, "DELETING")

    delete_transit_gateway_vpc_route_task.delay(
        tgw_vpc_route_id=tgw_vpc_route.id,
        vpc_net_ip=tgw_vpc_att.vpc_net_ip,
        tgw_management_ip=tgw.management_ip,
        destination_cidr=tgw_vpc_route.destination,
    )

    return {"message": "Transit Gateway VPC Route deletion in progress"}
