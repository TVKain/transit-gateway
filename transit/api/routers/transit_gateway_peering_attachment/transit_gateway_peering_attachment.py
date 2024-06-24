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

from transit.database.repositories.transit_gateway_peering_route.transit_gateway_peering_route import (
    TransitGatewayPeeringRouteRepository,
)
from transit.worker.transit_gateway_peering_attachment.tasks import (
    create_transit_gateway_peering_attachment_task,
    delete_transit_gateway_peering_attachment_task,
)

from transit.drivers.vytransit.vytransit_driver import VyTransitDriver

load_dotenv()

router = APIRouter(
    prefix="/transit_gateway_peering_attachments",
    tags=["transit_gateway_peering_attachments"],
)


AVAILABLE_CIDRS = [f"169.254.{i}.0/30" for i in range(1, 11)]


@router.get("/available_cidr/{transit_gateway_id}")
def get_available_cidrs(transit_gateway_id: str):
    tgw_repo = TransitGatewayRepository()

    tgw = tgw_repo.get(transit_gateway_id)

    if not tgw:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway with ID {transit_gateway_id} does not exist",
        )

    tgw_peer_attachment_repo = TransitGatewayPeeringAttachmentRepository()

    tgw_peer_attachments = tgw_peer_attachment_repo.get_all(transit_gateway_id)

    cidrs = []

    for cidr in AVAILABLE_CIDRS:
        if not _check_overlap_cidr(cidr, tgw_peer_attachments):
            cidrs.append(cidr)

    return cidrs


@router.get("/is_quota_max/{transit_gateway_id}")
def get_is_quota_max(transit_gateway_id: str):
    tgw_peer_attachment_repo = TransitGatewayPeeringAttachmentRepository()

    tgw_peer_attachments = tgw_peer_attachment_repo.get_all(transit_gateway_id)

    print(tgw_peer_attachments)

    if len(tgw_peer_attachments) >= int(os.getenv("MAX_PEERING_PER_TRANSIT_GATEWAY")):
        return True

    return False


@router.post("/")
def create(request: TransitGatewayPeeringAttachmentCreateRequest):
    tgw_peer_attachment_repo = TransitGatewayPeeringAttachmentRepository()
    tgw_repo = TransitGatewayRepository()

    # Get transit gateway by ID from the request
    try:
        tgw = tgw_repo.get(request.transit_gateway_id)

        if not tgw:
            raise HTTPException(
                status_code=400,
                detail=f"Transit Gateway with ID {request.transit_gateway_id} does not exist",
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Error occurred while fetching Transit Gateway",
        ) from e

    # Get all tgw_peer_attachment_repo for the given transit_gateway_id
    tgw_peer_attachments = tgw_peer_attachment_repo.get_all(request.transit_gateway_id)

    if _check_overlap_remote_tgw(
        request.remote_transit_gateway_id, tgw_peer_attachments
    ):
        raise HTTPException(
            status_code=400,
            detail="Transit Gateway Peering Attachment with remote Transit Gateway already exists",
        )

    if _check_overlap_remote_tgw_ip(
        request.remote_tunnel_interface_ip, tgw_peer_attachments
    ):
        raise HTTPException(
            status_code=400,
            detail="Transit Gateway Peering Attachment with remote Tunnel Interface IP already exists",
        )

    if len(tgw_peer_attachments) >= int(os.getenv("MAX_PEERING_PER_TRANSIT_GATEWAY")):
        raise HTTPException(
            status_code=400,
            detail="Maximum number of Transit Gateway Peering Attachments reached",
        )

    if _check_tun_cidr(request.tun_cidr) is False:
        raise HTTPException(
            status_code=400,
            detail="Invalid Tunnel CIDR",
        )

    if _check_overlap_cidr(request.tun_cidr, tgw_peer_attachments):
        raise HTTPException(
            status_code=400,
            detail="Tun CIDR overlaps with existing Transit Gateway Peering Attachment",
        )

    if _check_tun_ip(request.tun_ip, request.tun_cidr, request.remote_tun_ip) is False:
        raise HTTPException(
            status_code=400,
            detail="Invalid Tunnel IP or Remote Tun IP",
        )

    if _check_overlap_tun_cidr(request.tun_cidr, tgw_peer_attachments):
        raise HTTPException(
            status_code=400,
            detail="Transit Gateway Peering Attachment with the same TUN CIDR already exists",
        )

    tun_next_num = _determine_tun_next_num(tgw_peer_attachments)

    try:
        tgw_peer_attachment = tgw_peer_attachment_repo.create(
            TransitGatewayPeeringAttachmentModel(
                transit_gateway_id=request.transit_gateway_id,
                remote_transit_gateway_id=request.remote_transit_gateway_id,
                name=request.name,
                status="PENDING",
                tunnel_interface_ip=tgw.peering_net_ip,
                remote_tunnel_interface_ip=request.remote_tunnel_interface_ip,
                tun_num=tun_next_num,
                tun_ip=request.tun_ip,
                tun_cidr=request.tun_cidr,
                remote_tun_ip=request.remote_tun_ip,
            )
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail="Error occurred while creating Transit Gateway Peering Attachment",
        ) from e

    create_transit_gateway_peering_attachment_task.delay(
        transit_gateway_peering_attachment_id=tgw_peer_attachment.id,
        tun_num=tun_next_num,
        tun_ip=request.tun_ip,
        tunnel_interface_ip=tgw.peering_net_ip,
        remote_tunnel_interface_ip=request.remote_tunnel_interface_ip,
        tgw_management_ip=tgw.management_ip,
    )

    return tgw_peer_attachment


@router.delete("/{transit_gateway_peering_attachment_id}")
def delete(transit_gateway_peering_attachment_id: str):
    tgw_peer_attachment_repo = TransitGatewayPeeringAttachmentRepository()

    try:
        tgw_peer_attachment = tgw_peer_attachment_repo.get(
            transit_gateway_peering_attachment_id
        )

        if not tgw_peer_attachment:
            raise HTTPException(
                status_code=400,
                detail=f"Transit Gateway Peering Attachment with ID {transit_gateway_peering_attachment_id} does not exist",
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Error occurred while fetching Transit Gateway Peering Attachment",
        ) from e

    tgw_peer_route_repo = TransitGatewayPeeringRouteRepository()

    tgw_peer_routes = tgw_peer_route_repo.get_all(tgw_peer_attachment.id)

    if len(tgw_peer_routes) > 0:
        raise HTTPException(
            status_code=400,
            detail="Transit Gateway Peering Attachment has associated routes",
        )

    tgw_repo = TransitGatewayRepository()

    tgw = tgw_repo.get(tgw_peer_attachment.transit_gateway_id)

    tgw_peer_attachment_repo.update(tgw_peer_attachment.id, "DELETING")

    delete_transit_gateway_peering_attachment_task.delay(
        transit_gateway_peering_attachment_id=transit_gateway_peering_attachment_id,
        tun_num=tgw_peer_attachment.tun_num,
        tgw_management_ip=tgw.management_ip,
    )

    return tgw_peer_attachment


@router.get("/")
def get_all(transit_gateway_id: str | None = None):
    tgw_peer_attachment_repo = TransitGatewayPeeringAttachmentRepository()

    try:
        tgw_peer_attachments = tgw_peer_attachment_repo.get_all(transit_gateway_id)
    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail="Error occurred while fetching Transit Gateway Peering Attachments",
        ) from e

    return tgw_peer_attachments


def _determine_tun_next_num(
    tgw_peer_attachments: List[TransitGatewayPeeringAttachmentModel],
):
    if not tgw_peer_attachments:
        return 0

    if len(tgw_peer_attachments) == 0:
        return 0

    vti_nums = [
        tgw_peer_attachment.tun_num for tgw_peer_attachment in tgw_peer_attachments
    ]

    return max(vti_nums) + 1


def _check_tun_cidr(tun_cidr):
    allowed_cidrs = [f"169.254.{i}.0/30" for i in range(1, 11)]

    if tun_cidr not in allowed_cidrs:
        return False

    return True


def _check_tun_ip(tun_ip, tun_cidr, remote_tun_ip):

    try:
        tun_ip_ip = ipaddress.ip_address(tun_ip)
        tun_cidr_ip = ipaddress.ip_network(tun_cidr)
        remote_tun_ip_ip = ipaddress.ip_address(remote_tun_ip)

        if tun_ip_ip not in tun_cidr_ip:

            return False

        if remote_tun_ip_ip not in tun_cidr_ip:
            return False

        if tun_ip_ip == remote_tun_ip_ip:

            return False

        return True

    except ValueError:
        return False


def _check_overlap_cidr(tun_cidr, tgw_peer_attachments):
    tun_cidr_ip = ipaddress.ip_network(tun_cidr)

    for tgw_peer_attachment in tgw_peer_attachments:
        tgw_peer_attachment_tun_cidr_ip = ipaddress.ip_network(
            tgw_peer_attachment.tun_cidr
        )

        if tun_cidr_ip.overlaps(tgw_peer_attachment_tun_cidr_ip):
            return True

    return False


def _check_overlap_remote_tgw(
    remote_tgw_id: str, tgw_peer_attachments: List[TransitGatewayPeeringAttachmentModel]
):
    for tgw_peer_attachment in tgw_peer_attachments:
        if tgw_peer_attachment.remote_transit_gateway_id == remote_tgw_id:
            return True

    return False


def _check_overlap_tun_cidr(
    tun_cidr, tgw_peer_attachments: List[TransitGatewayPeeringAttachmentModel]
):
    tun_cidr_ip = ipaddress.ip_network(tun_cidr)

    for tgw_peer_attachment in tgw_peer_attachments:
        tgw_peer_attachment_tun_cidr_ip = ipaddress.ip_network(
            tgw_peer_attachment.tun_cidr
        )

        if tun_cidr_ip == tgw_peer_attachment_tun_cidr_ip:
            return True

    return False


def _check_overlap_remote_tgw_ip(
    remote_tunnel_interface_ip: str,
    tgw_peer_attachments: List[TransitGatewayPeeringAttachmentModel],
):
    for tgw_peer_attachment in tgw_peer_attachments:
        if tgw_peer_attachment.remote_tunnel_interface_ip == remote_tunnel_interface_ip:
            return True

    return False
