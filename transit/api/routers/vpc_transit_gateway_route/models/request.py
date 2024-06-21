from sqlmodel import SQLModel


class CreateVPCTransitGatewayRoutesRequest(SQLModel):
    vpc_id: str
    destination_cidr: str
    transit_gateway_vpc_attachment_id: str
