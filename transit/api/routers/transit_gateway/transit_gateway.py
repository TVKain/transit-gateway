from fastapi import APIRouter, HTTPException

from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)

from transit.database.repositories.transit_gateway.models.input import (
    TransitGatewayUpdateInput,
)

from transit.api.routers.transit_gateway.models.request import (
    TransitGatewayCreateRequest,
)

from transit.database.repositories.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentRepository,
)
from transit.worker.transit_gateway.tasks import (
    create_transit_gateway_task,
    delete_transit_gateway_task,
)

router = APIRouter(prefix="/transit_gateways", tags=["transit_gateways"])


@router.get("/")
def get_transit_gateways():
    transit_repo = TransitGatewayRepository()

    return transit_repo.get_all()


@router.get("/{transit_gateway_id}")
def get_transit_gateway(transit_gateway_id: str):
    transit_repo = TransitGatewayRepository()

    return transit_repo.get(ident=transit_gateway_id)


@router.post("/")
def create_transit_gateway(request: TransitGatewayCreateRequest):
    transit_repo = TransitGatewayRepository()

    try:
        transit_gateway = transit_repo.create(request.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    create_transit_gateway_task.delay(transit_gateway.id)

    return transit_gateway


@router.put("/{transit_gateway_id}")
def update_transit_gateway(transit_gateway_id: str, name: str):
    transit_repo = TransitGatewayRepository()

    return transit_repo.update(
        TransitGatewayUpdateInput(id=transit_gateway_id, name=name)
    )


@router.delete("/{transit_gateway_id}")
def delete_transit_gateway(transit_gateway_id: str):
    transit_repo = TransitGatewayRepository()

    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    tgw = transit_repo.get(transit_gateway_id)

    if not tgw:
        raise HTTPException(
            status_code=404,
            detail=f"Transit Gateway {transit_gateway_id} not found",
        )

    tgw_vpc_atts = tgw_vpc_att_repo.get_all(transit_gateway_id)

    if len(tgw_vpc_atts) > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway {transit_gateway_id} has VPC attachments",
        )

    if tgw.status == "DELETING":
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway {transit_gateway_id} is already deleting",
        )

    if tgw.status == "BUILD":
        raise HTTPException(
            status_code=400,
            detail=f"Transit Gateway {transit_gateway_id} is still creating",
        )

    transit_repo.update(
        TransitGatewayUpdateInput(id=transit_gateway_id, status="DELETING")
    )

    delete_transit_gateway_task.delay(
        transit_gateway_id=transit_gateway_id,
        compute_id=tgw.compute_id,
        vpc_net_id=tgw.vpc_net_id,
    )

    return {"message": "Transit Gateway delete in process"}
