import os

import logging

from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException

from transit.api.routers.transit_gateway_vpc_attachment.models.request import (
    CreateTransitGatewayVPCAttachmentRequest,
)
from transit.database.repositories.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentRepository,
)

from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)

from transit.database.repositories.transit_gateway_vpc_attachment.models.input import (
    TransitGatewayVPCAttachmentCreateInput,
    TransitGatewayVPCAttachmentUpdateInput,
)

from transit.database.repositories.transit_gateway_vpc_route.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteRepository,
)
from transit.database.repositories.vpc_transit_gateway_route.vpc_transit_gateway_route import (
    VPCTransitGatewayRouteRepository,
)
from transit.worker.transit_gateway_vpc_attachment.tasks import (
    create_transit_gateway_vpc_attachment_task,
    delete_transit_gateway_vpc_attachment_task,
)

load_dotenv()

router = APIRouter(
    prefix="/transit_gateway_vpc_attachments", tags=["transit_gateway_vpc_attachments"]
)


@router.post("/")
def create_transit_gateway_vpc_attachment(
    request: CreateTransitGatewayVPCAttachmentRequest,
):
    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()
    tgw_repo = TransitGatewayRepository()

    tgw_vpc_att = tgw_vpc_att_repo.get_by_vpc_id(request.vpc_id)

    logging.info(f"Get Transit Gateway VPC Attachment by VPC ID {request.vpc_id}")

    if tgw_vpc_att:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway VPC Attachment already exists for VPC ID {request.vpc_id}",
        )

    tgw_vpc_atts = tgw_vpc_att_repo.get_all(request.transit_gateway_id)

    logging.info("Get all Transit Gateway VPC Attachments")

    if len(tgw_vpc_atts) >= int(os.getenv("MAX_VPC_PER_TRANSIT_GATEWAY")):
        raise HTTPException(
            status_code=400,
            detail="Maximum number of VPCs per Transit Gateway reached",
        )

    try:

        result = tgw_vpc_att_repo.create(
            TransitGatewayVPCAttachmentCreateInput(
                transit_gateway_id=request.transit_gateway_id,
                name=request.name,
                vpc_id=request.vpc_id,
                vpc_router_id=request.vpc_router_id,
                vpc_cidr=request.vpc_cidr,
                status="PENDING",
            )
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    logging.info(f"Create Transit Gateway VPC Attachment {result.id}")

    tgw = tgw_repo.get(request.transit_gateway_id)

    logging.info(f"Get Transit Gateway {request.transit_gateway_id}")

    create_transit_gateway_vpc_attachment_task.delay(
        tgw_vpc_att_id=result.id,
        transit_gateway_id=request.transit_gateway_id,
        vpc_id=request.vpc_id,
        vpc_router_id=request.vpc_router_id,
        vpc_cidr=request.vpc_cidr,
        tgw_vpc_net_id=tgw.vpc_net_id,
        tgw_vpc_net_ip=tgw.vpc_net_ip,
        tgw_management_ip=tgw.management_ip,
    )

    logging.info(f"Create Transit Gateway VPC Attachment Task {result.id}")

    return result


@router.get("/")
def get_transit_gateway_vpc_attachments(transit_gateway_id: str | None = None):
    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    result = tgw_vpc_att_repo.get_all(transit_gateway_id)

    return result


@router.delete("/{transit_gateway_vpc_attachment_id}")
def delete_transit_gateway_vpc_attachment(transit_gateway_vpc_attachment_id: str):
    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()

    vpc_tgw_route_repo = VPCTransitGatewayRouteRepository()

    tgw_repo = TransitGatewayRepository()

    try:
        tgw_vpc_att = tgw_vpc_att_repo.get(transit_gateway_vpc_attachment_id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway VPC Attachment not found for id {transit_gateway_vpc_attachment_id}",
        ) from e

    tgw_vpc_routes = tgw_vpc_route_repo.get_all_by_tgw_att_id(
        transit_gateway_vpc_attachment_id
    )

    if len(tgw_vpc_routes) > 0:
        raise HTTPException(
            status_code=400,
            detail="Transit Gateway has routes associate with this VPC Attachment",
        )

    vpc_tgw_routes = vpc_tgw_route_repo.get_all_by_tgw_vpc_attachment_id(
        transit_gateway_vpc_attachment_id
    )

    if len(vpc_tgw_routes) > 0:
        raise HTTPException(
            status_code=400,
            detail="VPC has routes associate with this VPC Attachment",
        )

    tgw = tgw_repo.get(tgw_vpc_att.transit_gateway_id)

    tgw_vpc_att_repo.update(
        TransitGatewayVPCAttachmentUpdateInput(
            id=transit_gateway_vpc_attachment_id, status="DELETING"
        ),
    )

    delete_transit_gateway_vpc_attachment_task.delay(
        tgw_vpc_att_id=transit_gateway_vpc_attachment_id,
        vpc_router_id=tgw_vpc_att.vpc_router_id,
        tgw_vpc_net_id=tgw.vpc_net_id,
    )

    return {"message": "Transit Gateway VPC Attachment deleted"}
