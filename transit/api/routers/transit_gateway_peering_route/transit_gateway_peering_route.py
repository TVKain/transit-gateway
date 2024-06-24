from fastapi import APIRouter, HTTPException


from transit.database.repositories.transit_gateway_peering_attachment.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentRepository,
)

from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)


from transit.api.routers.transit_gateway_peering_route.models.request import (
    TransitGatewayPeeringAttachmentCreateRouteRequest,
)

from transit.api.routers.utils.check_tgw_route_overlap import check_tgw_route_overlap

from transit.common import utils
from transit.database.repositories.transit_gateway_peering_route.transit_gateway_peering_route import (
    TransitGatewayPeeringRouteRepository,
)

from transit.database.repositories.transit_gateway_vpc_route.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteRepository,
)
from transit.worker.transit_gateway_peering_route.tasks import (
    create_transit_gateway_vpc_attachment_task,
    delete_transit_gateway_peering_attachment_task,
)


router = APIRouter(
    prefix="/transit_gateway_peering_routes",
    tags=["transit_gateway_peering_routes"],
)


@router.post("/")
def create(request: TransitGatewayPeeringAttachmentCreateRouteRequest):
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

    tgw_peering_att_repo = TransitGatewayPeeringAttachmentRepository()

    try:
        tgw_peering_att = tgw_peering_att_repo.get(
            request.transit_gateway_peering_attachment_id
        )

        if not tgw_peering_att:
            raise Exception(
                f"Transit Gateway Peering Attachment {request.transit_gateway_peering_attachment_id} not found"
            )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}") from e

    try:
        tgw = tgw_repo.get(tgw_peering_att.transit_gateway_id)

        if not tgw:
            raise Exception(
                f"Transit Gateway not found for Peering Attachment {request.transit_gateway_peering_attachment_id}"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}") from e

    if check_tgw_route_overlap(tgw.id, request.destination_cidr):
        raise HTTPException(
            status_code=400,
            detail=f"Overlapping route for transit gateway {tgw.id}",
        )

    tgw_peering_route_repo = TransitGatewayPeeringRouteRepository()

    tgw_peering_route = tgw_peering_route_repo.create(
        transit_gateway_peering_attachment_id=request.transit_gateway_peering_attachment_id,
        destination_cidr=request.destination_cidr,
        status="PENDING",
    )

    create_transit_gateway_vpc_attachment_task.delay(
        destination_cidr=request.destination_cidr,
        tgw_management_ip=tgw.management_ip,
        remote_peering_interface_ip=tgw_peering_att.remote_tun_ip,
        tgw_peering_route_id=tgw_peering_route.id,
    )

    return tgw_peering_route


@router.get("/")
def get_transit_gateway_peering_routes(transit_gateway_id: str | None = None):
    tgw_repo = TransitGatewayRepository()
    if transit_gateway_id:
        try:
            tgw = tgw_repo.get(transit_gateway_id)

            if not tgw:
                raise Exception(
                    f"Transit Gateway not found for id {transit_gateway_id}"
                )

            return TransitGatewayPeeringRouteRepository().get_all_by_transit_gateway_id(
                transit_gateway_id
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{str(e)}") from e

    else:
        return TransitGatewayPeeringRouteRepository().get_all()


@router.delete("/{tgw_peering_route_id}")
def delete_transit_gateway_peering_route(tgw_peering_route_id: str):
    tgw_peering_route_repo = TransitGatewayPeeringRouteRepository()

    tgw_peering_att_repo = TransitGatewayPeeringAttachmentRepository()

    tgw_peering_route = tgw_peering_route_repo.get(tgw_peering_route_id)

    if not tgw_peering_route:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway Peering Route {tgw_peering_route_id} not found",
        )

    if tgw_peering_route.status == "DELETING":
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway Peering Route {tgw_peering_route_id} is already deleting",
        )

    if tgw_peering_route.status == "PENDING":
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway Peering Route {tgw_peering_route_id} is not yet created",
        )

    try:
        tgw_peering_route = tgw_peering_route_repo.get(tgw_peering_route_id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway Peering Route not found for id {tgw_peering_route_id}",
        ) from e

    try:
        tgw_peering_att = tgw_peering_att_repo.get(
            tgw_peering_route.transit_gateway_peering_attachment_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway Peering Attachment not found for id {tgw_peering_route.transit_gateway_peering_attachment_id}",
        ) from e

    try:
        tgw = TransitGatewayRepository().get(tgw_peering_att.transit_gateway_id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway not found for Peering Attachment {tgw_peering_att.id}",
        ) from e

    TransitGatewayPeeringRouteRepository().update(tgw_peering_route_id, "DELETING")

    delete_transit_gateway_peering_attachment_task(
        destination_cidr=tgw_peering_route.destination_cidr,
        tgw_management_ip=tgw.management_ip,
        remote_peering_interface_ip=tgw_peering_att.remote_tun_ip,
        tgw_peering_route_id=tgw_peering_route_id,
    )

    return {"message": "Transit Gateway Peering Route is being deleted"}
