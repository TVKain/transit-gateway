from pydantic import BaseModel
from pydantic import conlist


class TransitGatewayVPCModel(BaseModel):
    vpc_id: str
    subnet_ids: conlist(item_type=str, min_length=1)  # type: ignore


class TransitGatewayAttachVPCRequest(BaseModel):
    vpc: TransitGatewayVPCModel
    transit_gateway_id: str


class TransitGatewayAttachVPCResponse(BaseModel):
    transit_gateway_id: str
    vpcs: list[TransitGatewayVPCModel]
