import oslo_messaging as messaging

from fastapi import APIRouter

from transit.old_api.routers.transit_gateway.models.transit_gateway_attach_vpc import (
    TransitGatewayAttachVPCRequest,
)
from transit.old_api.routers.transit_gateway.models.transit_gateway_get import (
    TransitGatewayGetResponse,
)

from transit.old_api.routers.transit_gateway.models.transit_gateway_create import (
    TransitGatewayCreateRequest,
    TransitGatewayCreateResponse,
)

from transit.old_api.routers.transit_gateway.models.transit_gateway_update import (
    TransitGatewayUpdateRequest,
    TransitGatewayUpdatetResponse,
)

from transit.old_database.repositories.transit_gateway.models.transit_gateway_get import (
    TransitGatewayGetInput,
)

from transit.old_database.repositories.transit_gateway.models.transit_gateway_create import (
    TransitGatewayCreateInput,
)

from transit.old_database.repositories.transit_gateway.models.transit_gateway_update import (
    TransitGatewayUpdateInput,
)
from transit.old_database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)


import transit.common.constants.rpc as rpc_consts

from transit.common import rpc


router = APIRouter(prefix="/transit-gateways", tags=["transit-gateways"])


transit_gateway_repo = TransitGatewayRepository()

target = messaging.Target(
    topic=rpc_consts.TOPIC,
)

rpc_client = rpc.get_client(target)


@router.get("/", response_model=list[TransitGatewayGetResponse])
def get_all():
    get_output = transit_gateway_repo.get_all()

    return [TransitGatewayCreateResponse.model_validate(x) for x in get_output]


@router.get("/{uuid}", response_model=TransitGatewayGetResponse)
def get(uuid: str):

    get_output = transit_gateway_repo.get(TransitGatewayGetInput(id=uuid))

    return TransitGatewayGetResponse.model_validate(get_output)


@router.post("/", response_model=TransitGatewayCreateResponse)
def create(create_request: TransitGatewayCreateRequest):
    create_output = transit_gateway_repo.create(
        TransitGatewayCreateInput(
            name=create_request.name, user_id=create_request.user_id
        )
    )

    transit_gateway = TransitGatewayCreateResponse.model_validate(create_output)

    payload = {"transit_gateway": transit_gateway.model_dump()}
    # Fire and forget
    rpc_client.cast({}, "create_transit_gateway", **payload)

    return transit_gateway


@router.patch("/{uuid}", response_model=TransitGatewayUpdatetResponse)
def update(uuid: str, update_request: TransitGatewayUpdateRequest):
    update_output = transit_gateway_repo.update(
        TransitGatewayUpdateInput(id=uuid, name=update_request.name)
    )

    return TransitGatewayUpdatetResponse.model_validate(update_output)


@router.patch("/{uuid}")
def attach_vpc(uuid: str, attach_network_request: TransitGatewayAttachVPCRequest):
    pass
